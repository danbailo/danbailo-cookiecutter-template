import logging
from enum import StrEnum
from os import getenv

import structlog
from dotenv import load_dotenv

load_dotenv()

Logger = structlog.types.FilteringBoundLogger


class LoggerNameEnum(StrEnum):
    prod = 'prod'
    local = 'local'


class LoggerFactory:
    is_configured: bool = False

    _logger_name: str = None
    _logger_renderers: list = []
    _logger_configs: dict | None = None
    _logger_level: int = None
    _is_local: bool = None

    @classmethod
    def logger_name(cls) -> str:
        if cls._logger_name is not None:
            return cls._logger_name

        cls._logger_name = getenv('LOGGER_NAME', LoggerNameEnum.prod).lower()
        return cls._logger_name

    @classmethod
    def is_local(cls) -> bool:
        if cls._is_local is not None:
            return cls._is_local

        cls._is_local = cls.logger_name() == LoggerNameEnum.local
        return cls._is_local

    @classmethod
    def logger_level(cls) -> int:
        if cls._logger_level is not None:
            return cls._logger_level

        if cls.is_local():
            cls._logger_level = logging.DEBUG
        else:
            cls._logger_level = logging.INFO

        return cls._logger_level

    @classmethod
    def logger_renderer(cls) -> list:
        if cls._logger_renderers:
            return cls._logger_renderers

        if cls.is_local():
            cls._logger_renderers.append(structlog.dev.ConsoleRenderer())
        else:
            cls._logger_renderers.append(structlog.processors.EventRenamer('message'))
            cls._logger_renderers.append(structlog.processors.JSONRenderer())

        return cls._logger_renderers

    @classmethod
    def logger_configs(cls):
        if cls._logger_configs:
            return cls._logger_configs

        cls._logger_configs = {
            'processors': [
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.ExceptionRenderer(),
                structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S', utc=False),
                structlog.processors.CallsiteParameterAdder(
                    [
                        structlog.processors.CallsiteParameter.PATHNAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    ]
                ),
                *cls.logger_renderer(),
            ],
            'wrapper_class': structlog.make_filtering_bound_logger(cls.logger_level()),
            'context_class': dict,
            'logger_factory': structlog.PrintLoggerFactory(),
            'cache_logger_on_first_use': False,
        }
        return cls._logger_configs

    @classmethod
    def configure(cls):
        if not cls.is_configured:
            structlog.configure_once(**cls.logger_configs())
            cls.is_configured = True

    @classmethod
    def new(cls) -> Logger:
        cls.configure()
        return structlog.get_logger()
