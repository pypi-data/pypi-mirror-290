import json
import logging
import socket
import sys
from contextlib import suppress
from typing import Dict, List, Optional

import amqp
from amqp.exceptions import MessageNacked
from strenum import StrEnum

from ssec_amqp.__about__ import __version__
from ssec_amqp._defs import (
    AMQP_EXCHANGE_ID_FORMAT,
    DEFAULT_EXCHANGE,
    DEFAULT_PASS,
    DEFAULT_PORT,
    DEFAULT_RECONNECT_INTERVAL,
    DEFAULT_RECONNECT_WINDOW,
    DEFAULT_ROUTE_KEY,
    DEFAULT_USER,
    DEFAULT_VHOST,
    AMQPConnectionError,
    StateError,
)
from ssec_amqp._utils import LazyRetry, catch_amqp_errors

LOG = logging.getLogger("ssec_amqp")


__all__ = [
    "AmqpExchange",
    "AmqpClient",
    "DeliveryStatus",
    "ConnectionStatus",
]


class DeliveryStatus(StrEnum):
    """Enum for status of messages being delivered"""

    # Message was acknowledged by the server.
    DELIVERED = "DELIVERED"
    # Message was dropped due to reconnection.
    DROPPED = "DROPPED"
    # Message was rejected by the server.
    REJECTED = "REJECTED"


class ConnectionStatus(StrEnum):
    """Enum for status of exchange's connection"""

    # Exchange is connected to the server
    CONNECTED = "CONNECTED"

    # Exchange is reconnecting to the server
    RECONNECTING = "RECONNECTING"

    # Exchange is disconnected from the server
    DISCONNECTED = "DISCONNECTED"


class AmqpExchange:
    """Abstraction of an exchange on a AMQP server."""

    def __init__(
        self,
        host: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        exchange: Optional[str] = None,
        vhost: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        """Initialize the AmqpExchange.

        Args:
            host (str): where the exchange is
            user (str): user to connect with
            password (str): password to connect with
            exchange (Optional[str], optional): name of the exchange. Defaults to None.
            vhost (Optional[str], optional): vhost of the exchange. Defaults to None.
            port (Optional[int], optional): port to connect with. Defaults to None.
        """
        self.host = host
        self.user = user or DEFAULT_USER
        self.vhost = vhost or DEFAULT_VHOST
        self.port = port or DEFAULT_PORT
        self.exchange = exchange or DEFAULT_EXCHANGE
        self.__password = password or DEFAULT_PASS

        # Ignore types for amqp module, as it is untyped itself.
        self.__conn = self._amqp_connection_factory()
        self.__chan = None  # type: ignore
        self.__chan_id = None

    @property
    def connected(self) -> bool:
        status = self.__conn.connected
        if status is None:
            return False
        return status

    @property
    def identifier(self) -> str:
        return str(self)

    def _channel_open(self) -> bool:
        if not self.connected:
            return False
        return self.__chan is not None and self.__chan.is_open

    def _amqp_connection_factory(self) -> amqp.Connection:
        """Factory method for creating an amqp connection."""
        return amqp.Connection(
            f"{self.host}:{self.port}",
            userid=self.user,
            password=self.__password,
            virtual_host=self.vhost,
            confirm_publish=True,
            connect_timeout=0.25,
            client_properties={
                "product": "QuickMQ Python Client Library",
                "product_version": __version__,
                "platform": "Python {}".format(".".join(map(str, sys.version_info[:3]))),
            },
        )

    @catch_amqp_errors
    def connect(self) -> None:
        """Connects the object to the AMQP exchange using the parameters supplied in constructor."""
        if self.connected:
            LOG.debug("%s - connect() called, but already connected...", str(self))
            return

        LOG.info("%s - attempting connection...", str(self))
        if self.__conn.channels is None:
            # Connection previously closed.
            LOG.info("%s - creating new amqp object", str(self))
            self.__conn = self._amqp_connection_factory()
        self.__conn.connect()  # type: ignore [attr-defined]
        LOG.info("%s - connected", str(self))
        self.__chan = self.__conn.channel(channel_id=self.__chan_id)  # type: ignore [attr-defined]
        self.__chan_id = self.__chan.channel_id  # type: ignore [attr-defined]

    @catch_amqp_errors
    def produce(self, content_dict, route_key: Optional[str] = None) -> bool:
        """Produce a message to the exchange

        Args:
            content_dict (JSON): The body of the message to produce.
            key (Optional[str], optional): key to send with. Defaults to None.

        Raises:
            AmqpConnectionError: If there is a problem with the connection when publishing.

        Returns:
            bool: Was the message delivered?
        """
        self.refresh()
        content_json = json.dumps(content_dict)
        route_key = route_key or DEFAULT_ROUTE_KEY
        try:
            self.__chan.basic_publish(  # type: ignore [attr-defined]
                msg=amqp.Message(
                    body=content_json,
                    content_type="application/json",
                    content_encoding="utf-8",
                ),
                exchange=self.exchange,
                routing_key=route_key,
                timeout=5,
            )
        except MessageNacked:
            LOG.exception("%s - message nacked!", str(self))
            return False
        except socket.timeout:
            LOG.exception("%s - publish timeout!", str(self))
            raise  # This will get caught by @catch_amqp_errors
        else:
            return True
        finally:
            if not self._channel_open():  # type: ignore [attr-defined]
                self.__chan = self.__conn.channel(channel_id=self.__chan_id)  # type: ignore [attr-defined]

    @catch_amqp_errors
    def refresh(self) -> None:
        """Refresh the AMQP connection, assure that it is still connected.

        Raises:
            StateError: If the exchange is not connected.
        """
        if self.__conn.connected is None:
            raise StateError(action="refresh", state_info="call connect()")
        try:
            self.__conn.heartbeat_tick()
        except amqp.ConnectionForced:
            LOG.info("%s - missed heartbeat, trying reconnect", str(self))
            self.connect()  # Try again on heartbeat misses

    @catch_amqp_errors
    def close(self) -> None:
        """Closes the connection to the AMQP exchange."""
        self.__conn.collect()

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __repr__(self) -> str:
        return AMQP_EXCHANGE_ID_FORMAT.format(
            user=self.user,
            host=self.host,
            port=self.port,
            vhost=self.vhost,
            exchange=self.exchange,
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return False
        return (
            __value.host == self.host
            and __value.exchange == self.exchange
            and __value.user == self.user
            and __value.port == self.port
            and __value.vhost == self.vhost
        )


class AmqpClient:
    """Client that manages multiple AmqpExchanges at once."""

    def __init__(
        self,
        max_reconnect_time: Optional[float] = None,
        time_between_reconnects: Optional[float] = None,
        name: Optional[str] = None,
    ) -> None:
        """Initialize an AmqpClient.

        Args:
            reconnect_window (Optional[float], optional): How long an AmqpExchange
            has to reconnect before an error is raised. Negative for infinite time.
            Defaults to -1.
            time_between_reconnects (Optional[float], optional): Time to wait between
            reconnect attempts. It is not recommended to use a small value bc of
            negative performance side-effects.
            name (Optional[str], optional): A name to give this client, it isn't
            used within the class itself, but can help differentiate when
            logging.
        """
        self.reconnect_window = max_reconnect_time or DEFAULT_RECONNECT_WINDOW
        self.reconnect_interval = time_between_reconnects or DEFAULT_RECONNECT_INTERVAL
        self._name = name or str(id(self))

        self._connected_pool: List[AmqpExchange] = []
        self._reconnect_pool: Dict[AmqpExchange, LazyRetry] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def connections(self) -> Dict[str, str]:
        self.refresh_pools()
        d = {exch.identifier: ConnectionStatus.CONNECTED for exch in self._connected_pool}
        d.update({exch.identifier: ConnectionStatus.RECONNECTING for exch in self._reconnect_pool})
        return d

    def connect(self, exchange: AmqpExchange) -> None:
        """Connect this AmqpClient to an AmqpExchange

        Args:
            exchange (AmqpExchange): The AmqpExchange to connect to.

        Raises:
            ConnectionError: If it cannot connect to the exchange.
        """
        LOG.debug("%s - attempting to connect to %s", str(self), str(exchange))

        if exchange in self._connected_pool:
            LOG.debug("%s - already connected to %s, skipping...", str(self), str(exchange))
            return

        if exchange.connected:
            LOG.debug("%s - %s pre-connected, refreshing...", str(self), str(exchange))
            exchange.refresh()
            self._to_connected(exchange)
            return

        try:
            exchange.connect()
        except AMQPConnectionError:
            LOG.info(
                "%s - initial connection attempt to %s failed, reconnecting",
                str(self),
                str(exchange),
            )
            self._to_reconnect(exchange)
        else:
            LOG.info("%s - successfully connected to %s", str(self), str(exchange))
            self._to_connected(exchange)

        self.refresh_pools()  # Could raise a timeout error!

    def publish(self, message, route_key: Optional[str] = None) -> Dict[str, str]:
        """Publish an AMQP message to all exchanges connected to this client.

        Args:
            message (JSONable): A JSON-able message to publish
            route_key (Optional[str], optional): the route key to publish with. Defaults to None.

        Returns:
            Dict[str, DeliveryStatus]: The status of the publish to all exchanges connected to this client.
        """
        status = {}
        self.refresh_pools()
        for exchange in self._connected_pool:
            try:
                routable = exchange.produce(message, route_key)
            except AMQPConnectionError:
                LOG.exception("%s - error publishing to %s!", str(self), str(exchange))
                self._to_reconnect(exchange)
            else:
                LOG.debug(
                    "%s - published message to %s to %s",
                    str(self),
                    str(exchange),
                    route_key or "default route",
                )
                status[exchange.identifier] = DeliveryStatus.DELIVERED if routable else DeliveryStatus.REJECTED

        # Set status as dropped for all reconnecting exchanges
        status.update({exchange.identifier: DeliveryStatus.DROPPED for exchange in self._reconnect_pool})
        return status

    def disconnect(self, exchange: Optional[AmqpExchange] = None) -> None:
        """Disconnect this AmqpClient from one or all exchanges.

        Args:
            exchange (Optional[AmqpExchange], optional): A specific exchange to disconnect from.
            If none, disconnect from all exchanges. Defaults to None.
        """
        if exchange is not None:
            exch_str = str(exchange)
            if exchange in self._reconnect_pool:
                LOG.debug("%s - removing %s from reconnect pool for disconnect", str(self), exch_str)
                del self._reconnect_pool[exchange]
            elif exchange in self._connected_pool:
                LOG.debug("%s - removing %s from conncted pool for disconnect", str(self), exch_str)
                self._connected_pool.remove(exchange)
            else:
                err_msg = f"Not connected to {exch_str}"
                raise ValueError(err_msg)
            LOG.info("%s - disconnecting from %s", str(self), exch_str)
            with suppress(AMQPConnectionError):
                exchange.close()
            return

        LOG.info("%s - disconnecting from everything", str(self))
        for exchange in self._connected_pool:
            with suppress(AMQPConnectionError):
                exchange.close()
        for exchange in self._reconnect_pool:
            with suppress(AMQPConnectionError):
                exchange.close()
        self._reconnect_pool.clear()
        self._connected_pool.clear()

    def _to_reconnect(self, exchange: AmqpExchange) -> None:
        """Move an exchange to reconnecting pool.

        Args:
            exchange (AmqpExchange): AmqpExchange to move.
        """
        if exchange in self._connected_pool:
            self._connected_pool.remove(exchange)
        LOG.debug("%s - moving %s to reconnect pool", str(self), str(exchange))
        with suppress(AMQPConnectionError):
            exchange.close()
        self._reconnect_pool[exchange] = LazyRetry(
            exchange.connect,
            AMQPConnectionError,
            max_retry_duration=self.reconnect_window,
            retry_interval=self.reconnect_interval,
        )

    def _to_connected(self, exchange: AmqpExchange) -> None:
        """Move an exchange to connected pool.

        Args:
            exchange (AmqpExchange): AmqpExchange to move.
        """
        if exchange in self._reconnect_pool:
            del self._reconnect_pool[exchange]
        LOG.debug("%s - moving %s to connected pool", str(self), str(exchange))
        self._connected_pool.append(exchange)

    def refresh_pools(self) -> None:
        """Refresh this client's pools. Checks if exchanges can reconnect."""
        LOG.debug("%s - refreshing pools", str(self))
        for exchange, reconnect_attempt in self._reconnect_pool.copy().items():
            if not reconnect_attempt.retry_ready:
                continue
            result = reconnect_attempt()
            if result is LazyRetry.NOT_YET:
                continue
            if result is LazyRetry.FAILED_ATTEMPT:
                LOG.info("%s - %s failed to reconnect", str(self), str(exchange))
            else:
                LOG.info("%s - %s has reconnected!", str(self), str(exchange))
                self._to_connected(exchange)
        for exchange in self._connected_pool:
            try:
                exchange.refresh()
            except AMQPConnectionError:
                LOG.warning("%s - %s has lost connection!", str(self), str(exchange))
                self._to_reconnect(exchange)

    def __repr__(self) -> str:
        return f"AmqpClient<{self._name}>"
