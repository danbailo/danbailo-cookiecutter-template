import os

from typing import Any

from dotenv import load_dotenv

from .logger import logger

load_dotenv()

ENV_VAR = {}


def set_env_var(key: Any, value: Any) -> Any:
    ENV_VAR[key] = value
    return value


def get_env_var(key: str, raise_exception: bool = True) -> str | None:
    value = os.environ.get(key) or ENV_VAR.get(key)
    if value is None and raise_exception is True:
        raise ValueError(f'The variable "{key}" is not declared!')
    if value is None and raise_exception is False:
        logger.warning(f'variable is not declared - {key.upper()}')
    return value

asd