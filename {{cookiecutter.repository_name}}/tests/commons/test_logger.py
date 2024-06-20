import logging
import os

import structlog

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.commons.logger import LoggerFactory, LoggerNameEnum


def calling_loggers():
    logger = LoggerFactory.new()
    logger.info('some teeeest', foo='foo')

    try:
        1 / 0
    except Exception:
        logger.error('got error!', exc_info=True)
        logger.exception('got error!')

    logger.info('some teeeest', foo='bar')
    logger.warning('some teeeest', lorem='lorem')
    logger.debug('some teeeest', cnj='123', pasta=123)


def test_logger(log):
    calling_loggers()

    assert log.events == [
        {'event': 'some teeeest', 'foo': 'foo', 'log_level': 'info'},
        {'event': 'got error!', 'exc_info': True, 'log_level': 'error'},
        {'event': 'got error!', 'exc_info': True, 'log_level': 'error'},
        {'event': 'some teeeest', 'foo': 'bar', 'log_level': 'info'},
        {'event': 'some teeeest', 'log_level': 'warning', 'lorem': 'lorem'},
        {'cnj': '123', 'event': 'some teeeest', 'log_level': 'debug', 'pasta': 123},
    ]


def test_logger_factory():
    LOGGER_NAME = os.getenv('LOGGER_NAME') or 'prod'

    if LOGGER_NAME == 'prod':
        assert LoggerFactory.logger_name() == LoggerNameEnum.prod
        assert LoggerFactory.logger_level() == logging.INFO
        for renderer in LoggerFactory.logger_renderer():
            assert isinstance(
                renderer,
                (structlog.processors.EventRenamer, structlog.processors.JSONRenderer),
            )

        configs = LoggerFactory.logger_configs()
        assert configs['cache_logger_on_first_use'] is False
        assert configs['context_class'] is dict
        assert isinstance(configs['logger_factory'], structlog.PrintLoggerFactory)
        assert len(configs['processors']) == 8

    elif LOGGER_NAME == 'local':
        assert LoggerFactory.logger_level() == logging.DEBUG
        for renderer in LoggerFactory.logger_renderer():
            assert isinstance(renderer, structlog.dev.ConsoleRenderer)

        configs = LoggerFactory.logger_configs()
        assert configs['cache_logger_on_first_use'] is False
        assert configs['context_class'] is dict
        assert isinstance(configs['logger_factory'], structlog.PrintLoggerFactory)
        assert len(configs['processors']) == 7

    else:
        raise Exception('LOGGER_NAME is different of `prod` or `local`')
