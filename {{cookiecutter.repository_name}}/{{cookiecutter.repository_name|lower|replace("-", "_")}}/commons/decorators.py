import asyncio
import signal
import time
from functools import wraps
from math import ceil

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.commons.logger import Logger, LoggerFactory

logger: Logger = LoggerFactory.new()


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
            logger.debug(
                f'Time elapsed to run "{function.__name__}" - '
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
            logger.debug(
                f'Time elapsed to run "{function.__name__}" - '
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
