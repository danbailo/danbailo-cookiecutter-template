import asyncio
import signal
import time
from functools import wraps
from math import ceil

from commons.logger import Logger

logger = Logger().get_logger()


def coro(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return asyncio.run(function(*args, **kwargs))

    return wrapper


def async_timeit(function):
    @wraps(function)
    def _async_timeit(*args, **kwargs):
        start = time.monotonic()
        try:
            return asyncio.run(function(*args, **kwargs))
        finally:
            logger.info(
                f'time elapsed to run "{function.__name__}" - '
                f'{time.monotonic() - start:0.2f}s',
            )

    return _async_timeit


def timeit(function):
    @wraps(function)
    def _timeit(*args, **kwargs):
        start = time.monotonic()
        try:
            return function(*args, **kwargs)
        finally:
            logger.info(
                f'time elapsed to run "{function.__name__}" - '
                f'{time.monotonic() - start:0.2f}s',
            )

    return _timeit


def timeout(seconds):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeoutError(
                    f'The function "{function.__name__}" is taking more than '
                    f'{seconds} seconds to run! '
                )

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(ceil(seconds))

            result = function(*args, **kwargs)

            signal.alarm(0)
            return result

        return wrapper

    return decorator
