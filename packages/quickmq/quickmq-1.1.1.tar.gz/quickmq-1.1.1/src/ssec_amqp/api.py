"""
ssec_amqp.api
~~~~~~~~~~~~~

This module implements the quickmq API.
"""

import atexit
from typing import Dict, Optional

from ssec_amqp import AmqpClient, AmqpExchange
from ssec_amqp._defs import DEFAULT_RECONNECT_INTERVAL, DEFAULT_RECONNECT_WINDOW

__CLIENT = AmqpClient(name="API_CLIENT")

atexit.register(__CLIENT.disconnect)


def configure(reconnect_window: Optional[float] = None, reconnect_interval: Optional[float] = None) -> None:
    """Configure the current client.

    Args:
        reconnect_window (Optional[float], optional): How long to wait until a reconnecting exchange will throw an
        error. Defaults to None.
        reconnect_interval (Optional[float], optional): How long to wait between reconnect attempts. Not recomended
        to use a small value.
    """
    __CLIENT.reconnect_window = reconnect_window or DEFAULT_RECONNECT_WINDOW
    __CLIENT.reconnect_interval = reconnect_interval or DEFAULT_RECONNECT_INTERVAL


def connect(
    host: str,
    *hosts: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    exchange: Optional[str] = None,
    port: Optional[int] = None,
    vhost: Optional[str] = None,
) -> None:
    """Connect to one or more AMQP exchanges.

    Args:
        host (str): hostname of server to connect to.
        user (Optional[str], optional): User to connect with. Defaults to None.
        password (Optional[str], optional): Password to connect with. Defaults to None.
        exchange (Optional[str], optional): Exchange to connect to. Defaults to None.
        port (Optional[int], optional): Port to connect to. Defaults to None.
        vhost (Optional[str], optional): Vhost to connect to. Defaults to None.
    """
    exchanges = [AmqpExchange(dest, user, password, exchange, vhost, port) for dest in (host, *hosts)]
    for exch in exchanges:
        __CLIENT.connect(exch)


def status() -> Dict[str, str]:
    """Get the status of all current connections.

    Returns:
        Dict[str, str]: A dictionary containing all of the current connections
        and there status: either 'connected' or 'reconnecting'.
    """
    return __CLIENT.connections


def publish(message, route_key: Optional[str] = None) -> Dict[str, str]:
    """Publish a message to all currently connected AMQP exchanges.

    Args:
        message (Any): The message to publish, must be json-able.
        route_key (Optional[str], optional): The key to publish the message with. Defaults to None.

    Raises:
        RuntimeError: If not connected to any AMQP exchanges currently.

    Returns:
        Dict[str, DeliveryStatus]: The delivery status to all of the currently connected AMQP exchanges.
    """
    return __CLIENT.publish(message, route_key=route_key)


def disconnect():
    """Disconnect from all AMQP exchanges."""
    __CLIENT.disconnect()
