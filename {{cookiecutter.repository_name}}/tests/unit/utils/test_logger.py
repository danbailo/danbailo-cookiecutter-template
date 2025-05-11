import logging
import os
from unittest.mock import MagicMock, patch

import structlog
from pytest import mark
from pytest_mock import MockerFixture
from structlog.testing import capture_logs

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import Logger, LoggerFactory, LoggerNameEnum

# TODO: improve tests


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
    LOGGER_NAME = os.getenv('LOGGER_NAME') or 'PROD'

    if LOGGER_NAME == 'PROD':
        assert LoggerFactory.get_logger_name() == LoggerNameEnum.PROD
        assert LoggerFactory.get_logger_level() == logging.INFO
        for renderer in LoggerFactory.get_logger_renderer():
            assert isinstance(
                renderer,
                (structlog.processors.EventRenamer, structlog.processors.JSONRenderer),
            )

        configs = LoggerFactory.get_logger_configs()
        assert configs['cache_logger_on_first_use'] is False
        assert configs['context_class'] is dict
        assert isinstance(configs['logger_factory'], structlog.PrintLoggerFactory)
        assert len(configs['processors']) == 8

    elif LOGGER_NAME == 'LOCAL':
        assert LoggerFactory.get_logger_level() == logging.DEBUG
        for renderer in LoggerFactory.get_logger_renderer():
            assert isinstance(renderer, structlog.dev.ConsoleRenderer)

        configs = LoggerFactory.get_logger_configs()
        assert configs['cache_logger_on_first_use'] is False
        assert configs['context_class'] is dict
        assert isinstance(configs['logger_factory'], structlog.PrintLoggerFactory)
        assert len(configs['processors']) == 7

    else:
        raise Exception('LOGGER_NAME is different of `prod` or `local`')


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
            LoggerNameEnum.PROD,
            [
                {'event': 'testeee', 'foo': 'foo', 'log_level': 'info'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'deu erro!', 'exc_info': True, 'log_level': 'error'},
                {'event': 'testeee', 'foo': 'bar', 'log_level': 'info'},
                {'event': 'testeee', 'log_level': 'warning', 'lorem': 'lorem'},
            ],
        ),
        (
            LoggerNameEnum.LOCAL,
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
    ids=('PROD', 'LOCAL'),
)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.getenv')
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory.is_configured', lambda: False)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory._logger_name', None)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory._logger_renderers', [])
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory._logger_configs', None)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory._logger_level', None)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger.LoggerFactory._is_local', None)
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
