import asyncio
import functools
import inspect
import os
import pickle
import signal
import time
import warnings
from functools import wraps
from math import ceil
from typing import Callable, TypeVar

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import Logger, LoggerFactory

logger: Logger = LoggerFactory.new()

T = TypeVar('T')


def coro(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return asyncio.run(function(*args, **kwargs))

    return wrapper


def async_timeit(function):
    @wraps(function)
    def async_timeit_(*args, **kwargs):
        start = time.monotonic()
        try:
            return asyncio.run(function(*args, **kwargs))
        finally:
            logger.debug(
                f'time elapsed to run "{function.__name__}" - '
                f'{time.monotonic() - start:0.2f}s',
            )

    return async_timeit_


def timeit(function):
    @wraps(function)
    def timeit_(*args, **kwargs):
        start = time.monotonic()
        try:
            return function(*args, **kwargs)
        finally:
            logger.debug(
                f'time elapsed to run "{function.__name__}" - '
                f'{time.monotonic() - start:0.2f}s',
            )

    return timeit_


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


# TODO: usar o decorator do Python 3.13 após atualizar versão
def deprecated(message: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter('default', DeprecationWarning)
            return function(*args, **kwargs)

        return wrapper

    return decorator


def pickle_cache(file_path: str):
    """
    Decorator que salva o objeto python retornado por uma função em um arquivo pickle.
    É possível passar um caminho de arquivo com placeholders para serem preenchidos com os argumentos da função.
    Exemplo:

    ```python
    # compute(5) salva o resultado em 'result_5.pkl'
    @pickle_cache('result_{x}.pkl')
    def compute(x):
        return x * 2
    ```
    """

    def decorator(function: Callable[..., T]):
        signature = inspect.signature(function)

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal file_path

            bound_args = signature.bind(*args, **kwargs)
            file_path = str(file_path).format(**bound_args.arguments)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    cached_result: T = pickle.load(f)
                    return cached_result

            result = function(*args, **kwargs)
            with open(file_path, 'wb') as f:
                pickle.dump(result, f)
            return result

        return wrapper

    return decorator
