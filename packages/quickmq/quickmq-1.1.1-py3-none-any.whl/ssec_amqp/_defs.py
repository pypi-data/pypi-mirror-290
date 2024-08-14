"""
ssec_amqp._defs
~~~~~~~~~~~~~~~

Definitions that are used in ssec_amqp.
"""

from typing import Optional

# Inspired by the AMQP URI format, and adds the exchange to the end
AMQP_EXCHANGE_ID_FORMAT = "amqp://{user:s}@{host:s}:{port:d}{vhost:s}/{exchange:s}"

# Default AmqpExchange values
DEFAULT_USER = "guest"
DEFAULT_PASS = "guest"  # noqa: S105
DEFAULT_PORT = 5672
DEFAULT_VHOST = "/"
DEFAULT_EXCHANGE = ""
DEFAULT_ROUTE_KEY = ""

# Default AmqpClient values
DEFAULT_RECONNECT_WINDOW = -1.0  # reconnects forever
DEFAULT_RECONNECT_INTERVAL = 15  # wait 15 seconds before another attempt


# Exceptions that are used within ssec_amqp
class StateError(Exception):
    """Wrong state to perform an action."""

    def __init__(self, action: str, state_info: Optional[str]) -> None:
        msg = f"Cannot perform {action} in this state"
        if state_info is None:
            msg += "!"
        else:
            msg += f"({state_info})!"
        super().__init__(msg)


class RetryError(TimeoutError):
    """Reconnect retrying timed out."""


class AMQPConnectionError(ConnectionError):
    """All purpose error for any problems with the AMQP connection."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        msg = "AMQPConnectionError"
        if self.__cause__ is not None:
            msg += f" from {self.__cause__.__class__} ({self.__cause__})"
        return msg
