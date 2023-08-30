import asyncio

from functools import wraps

import time

from .logger import logger


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


def async_timeit(f):
    @wraps(f)
    def _async_timeit(*args, **kwargs):
        start = time.monotonic()
        try:
            return asyncio.run(f(*args, **kwargs))
        finally:
            logger.info(
                'time elapsed to run "%s" - %ss',
                f.__name__, f'{time.monotonic() - start:0.2f}'
            )
    return _async_timeit


def timeit(f):
    @wraps(f)
    def _timeit(*args, **kwargs):
        start = time.monotonic()
        try:
            return f(*args, **kwargs)
        finally:
            logger.info(
                'time elapsed to run "%s" - %ss',
                f.__name__, f'{time.monotonic() - start:0.2f}'
            )
    return _timeit
