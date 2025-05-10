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


from unittest.mock import MagicMock, patch

import structlog
from pytest import mark
from pytest_mock import MockerFixture
from structlog.testing import capture_logs

from legalops_commons.factories.logger import Logger, LoggerFactory, LoggerNameEnum


def _emulate_division_by_zero_error(logger: Logger):
    logger.info('testeee', foo='foo')

    try:
        1 / 0
    except Exception:
        logger.error('deu erro!', exc_info=True)
        logger.exception('deu erro!')

    logger.info('testeee', foo='bar')
    logger.warning('testeee', lorem='lorem')
    logger.debug('testeee', cnj='123', pasta=123)


@mark.parametrize(
    ('environment', 'captured_logs'),
    (
        (
            LoggerNameEnum.prod,
            [
                {'event': 'testeee', 'foo': 'foo', 'log_level': 'info'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'testeee', 'foo': 'bar', 'log_level': 'info'},
                {'event': 'testeee', 'log_level': 'warning', 'lorem': 'lorem'},
            ],
        ),
        (
            LoggerNameEnum.local,
            [
                {'event': 'testeee', 'foo': 'foo', 'log_level': 'info'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'testeee', 'foo': 'bar', 'log_level': 'info'},
                {'event': 'testeee', 'log_level': 'warning', 'lorem': 'lorem'},
                {'event': 'testeee', 'log_level': 'debug', 'cnj': '123', 'pasta': 123},
            ],
        ),
    ),
    ids=('prod', 'local'),
)
@patch('legalops_commons.factories.logger.getenv')
@patch('legalops_commons.factories.logger.LoggerFactory.is_configured', lambda: False)
@patch('legalops_commons.factories.logger.LoggerFactory._logger_name', None)
@patch('legalops_commons.factories.logger.LoggerFactory._logger_renderers', [])
@patch('legalops_commons.factories.logger.LoggerFactory._logger_configs', None)
@patch('legalops_commons.factories.logger.LoggerFactory._logger_level', None)
@patch('legalops_commons.factories.logger.LoggerFactory._is_local', None)
def test_logger_level(getenv_mock: MagicMock, environment: str, captured_logs: dict):
    getenv_mock.return_value = environment
    logger = LoggerFactory.new()

    with capture_logs() as cap_logs:
        _emulate_division_by_zero_error(logger)

    assert cap_logs == captured_logs


@patch('structlog._config._CONFIG.is_configured', False)
def test_configure_logger_just_once(mocker: MockerFixture):
    logger_factory_configure_spy = mocker.spy(LoggerFactory, 'configure')
    structlog_configure_spy = mocker.spy(structlog, 'configure')

    LoggerFactory.new()
    LoggerFactory.new()

    assert logger_factory_configure_spy.call_count == 2
    assert structlog_configure_spy.call_count == 1
