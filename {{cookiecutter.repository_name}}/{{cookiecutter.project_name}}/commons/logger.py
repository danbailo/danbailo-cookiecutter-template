import logging
from os import getenv

import structlog


class LoggerContext:
    @staticmethod
    def bind(**kwargs):
        structlog.contextvars.bind_contextvars(**kwargs)

    @staticmethod
    def clear():
        structlog.contextvars.clear_contextvars()


class Logger:
    LOCAL_LOGGER = 'local'
    is_configured = False

    _logger_name: str = None
    _is_local: bool = None
    _logger_renderers: list = []
    _logger_level: str = None

    def __init__(self):
        self._configure()

    @property
    def logger_name(self) -> str:
        if self._logger_name is not None:
            return self._logger_name

        self._logger_name = getenv('LOGGER_NAME', self.LOCAL_LOGGER)
        return self._logger_name

    @property
    def is_local(self) -> str:
        if self._is_local is not None:
            return self._is_local

        self._is_local = self.logger_name == self.LOCAL_LOGGER
        return self._is_local

    @property
    def logger_level(self) -> int:
        if self._logger_level is not None:
            return self._logger_level

        if self.is_local:
            self._logger_level = logging.DEBUG
        else:
            self._logger_level = logging.INFO

        return self._logger_level

    @property
    def logger_renderer(self) -> list:
        if self._logger_renderers:
            return self._logger_renderers

        if self.is_local:
            self._logger_renderers.append(structlog.dev.ConsoleRenderer())
        else:
            self._logger_renderers.append(structlog.processors.EventRenamer('message'))
            self._logger_renderers.append(structlog.processors.JSONRenderer())

        return self._logger_renderers

    def _configure(self):
        if not self.is_configured:
            structlog.configure_once(
                processors=[
                    structlog.contextvars.merge_contextvars,
                    structlog.processors.add_log_level,
                    structlog.processors.StackInfoRenderer(),
                    structlog.dev.set_exc_info,
                    structlog.processors.TimeStamper(
                        fmt='%Y-%m-%d %H:%M:%S', utc=False
                    ),
                    structlog.processors.CallsiteParameterAdder(
                        [
                            structlog.processors.CallsiteParameter.PATHNAME,
                            structlog.processors.CallsiteParameter.FUNC_NAME,
                            structlog.processors.CallsiteParameter.LINENO,
                        ],
                    ),
                    *self.logger_renderer,
                ],
                wrapper_class=structlog.make_filtering_bound_logger(self.logger_level),
                context_class=dict,
                logger_factory=structlog.PrintLoggerFactory(),
                cache_logger_on_first_use=False,
            )
            self.is_configured = True

    def get_logger(self):
        return structlog.get_logger()
