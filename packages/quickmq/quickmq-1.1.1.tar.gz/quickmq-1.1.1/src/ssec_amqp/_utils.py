"""
ssec_amqp._utils
~~~~~~~~~~~~~~~~

Internal utility classes/functions.
"""

import itertools
import time
from enum import IntEnum, auto
from functools import partial
from typing import Callable, Generic, Optional, Type, TypeVar, Union

from amqp import Connection

from ssec_amqp._defs import AMQPConnectionError, RetryError

_T = TypeVar("_T")
ErrType = Type[BaseException]


class RetrySentinel(IntEnum):
    FAILED_ATTEMPT = auto()
    NOT_YET = auto()


class LazyRetry(Generic[_T]):
    _smallest_interval = 0.0000001

    # Sentinel return values for retry_action()
    NOT_YET = RetrySentinel.NOT_YET
    FAILED_ATTEMPT = RetrySentinel.FAILED_ATTEMPT

    def __init__(
        self,
        action: Callable[..., _T],
        *expected_errors: ErrType,
        retry_interval: Optional[float] = None,
        max_retry_attempts: Optional[int] = None,
        max_retry_duration: Optional[float] = None,
        **action_kwargs,
    ) -> None:
        """Non-blocking, single-threaded, lazy solution to call an error-prone action until
        success or user-defined failure.

        *Note: as a lazy solution, the honess on when to call retry_action() is on the user.

        Args:
            action (Callable[..., _T]): Error-prone callable to retry.
            *expected_errors (Exception): The errors that action is expected to raise.
            retry_interval (Optional[float], optional): Amount of time to 'wait' before
            another retry attempt can be made. If an attempt is made before the interval is up,
            NOT_YET is returned. Not recommended to be a very small number Defaults to 1.0.
            max_retry_attempts (Optional[int], optional): The maximum number of retry attempts to
            make before the action is considered failed and RetryError is raised. Defaults to infinite.
            max_retry_duration (Optional[float], optional): The maximum amount of time to attempt
            retries for before action is considered failed and RetryError is raised. Defaults to infinite.
            **action_kwargs (Any): key word arguments passed to the action during retry attempts.

        Raises:
            ValueError: retry_interval is too small.
            ValueError: max_retry_attempts <= 0.
            ValueError: max_retry_duration == 0
            ValueError: action is not callable.
        """
        if retry_interval is not None and retry_interval <= LazyRetry._smallest_interval:
            # really small float values lead to funky results
            raise ValueError("retry_interval must be positive")  # noqa: TRY003, EM101

        if max_retry_attempts is not None and max_retry_attempts <= 0:
            raise ValueError("max_retry_attempts must be positive")  # noqa: TRY003, EM101

        if max_retry_duration is not None and max_retry_duration == 0:
            raise ValueError("max_retry_duration cannot be 0, use negative number for infinite time.")  # noqa: TRY003, EM101

        if not callable(action):
            raise TypeError("action needs to be callable")  # noqa: TRY003, EM101

        init_time = time.time()

        self._action = partial(action, **action_kwargs)
        self._errors = expected_errors
        self._retry_attempts = 0
        self._max_retry_attempts = max_retry_attempts or float("inf")

        retry_interval = retry_interval or 1

        # gets the next time to try
        self._get_next_retry_time = partial(next, itertools.count(init_time, retry_interval))
        self._next_retry_time = self._get_next_retry_time()

        if max_retry_duration is None or max_retry_duration < 0:
            self._time_of_last_retry = float("inf")
        else:
            self._time_of_last_retry = init_time + max_retry_duration

    @property
    def attempts(self) -> int:
        """Number of attempts made so far to retry action."""
        return self._retry_attempts

    @property
    def retry_ready(self) -> bool:
        """retry_action() will not return NOT_YET"""
        return time.time() >= self._next_retry_time

    def retry_action(self) -> Union[_T, RetrySentinel]:
        """Attempt to call the action.

        Raises:
            RetryError: Action didn't succeed in enough time and/or attempts.

        Returns:
            LazyRetry.FAILED_ATTEMPT if action raised an expected error.
            LazyRetry.NOT_YET if not ready to retry the action.
            _T: action's return value if action succeeded.
        """
        return self.__call__()

    def __call__(self) -> Union[_T, RetrySentinel]:
        """Retry the action."""
        current_time = time.time()

        if current_time < self._next_retry_time:
            return LazyRetry.NOT_YET

        # make sure next_action_time is updated
        while True:
            possible_next_time = self._get_next_retry_time()
            if current_time < possible_next_time:
                self._next_retry_time = possible_next_time
                break

        self._retry_attempts += 1
        try:
            return self._action()
        except self._errors as e:
            if current_time >= self._time_of_last_retry or self._retry_attempts >= self._max_retry_attempts:
                raise RetryError from e
            return LazyRetry.FAILED_ATTEMPT


def catch_amqp_errors(func):
    """Utility decorator to catch all of Pika's AMQPConnectionError and
    raise them as built-in ConnectionError

    Args:
        func (Callable): Function to decorate
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Connection.recoverable_connection_errors as e:
            raise AMQPConnectionError from e

    return wrapper
