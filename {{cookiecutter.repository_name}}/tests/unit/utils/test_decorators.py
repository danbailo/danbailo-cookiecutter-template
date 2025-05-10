import asyncio
import os
import pickle
import time
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from legalops_commons.utils.decorators import (
    async_timeit,
    coro,
    deprecated,
    pickle_cache,
    timeit,
    timeout,
)


def test_coro_decorator():
    @coro
    async def async_function():
        return 'async mocked result'

    result = async_function()
    assert result == 'async mocked result'


@patch('legalops_commons.utils.decorators.logger')
def test_async_timeit_decorator(mock_logger):
    @async_timeit
    async def async_function():
        await asyncio.sleep(0.1)
        return 'async mocked result'

    result = async_function()
    assert result == 'async mocked result'
    assert mock_logger.debug.called
    assert 'time elapsed to run "async_function"' in mock_logger.debug.call_args[0][0]


@patch('legalops_commons.utils.decorators.logger')
def test_timeit_decorator(mock_logger):
    @timeit
    def sync_function():
        time.sleep(0.1)
        return 'sync result'

    result = sync_function()
    assert result == 'sync result'
    assert mock_logger.debug.called
    assert 'time elapsed to run "sync_function"' in mock_logger.debug.call_args[0][0]


def test_timeout_decorator():
    @timeout(1)
    def long_running_function():
        time.sleep(2)
        return 'result'

    with pytest.raises(
        TimeoutError,
        match='The function "long_running_function" is taking more than 1 seconds to run!',
    ):
        long_running_function()


def test_deprecated_decorator():
    @deprecated('This function is deprecated')
    def old_function():
        return 'old function result'

    with pytest.warns(DeprecationWarning, match='This function is deprecated'):
        result = old_function()
        assert result == 'old function result'


def test_pickle_cache_decorator(tmp_path: Path):
    file_path = tmp_path / 'test.pkl'

    class TestClass:
        @pickle_cache(file_path)
        def compute(self, x: int):
            return x * 2

    test_instance = TestClass()

    result = test_instance.compute(5)
    assert result == 10
    assert os.path.exists(file_path)

    with open(file_path, 'rb') as f:
        saved_result = pickle.load(f)
    assert saved_result == 10

    result = test_instance.compute(5)
    assert result == 10

    os.remove(file_path)


def test_pickle_cache_decorator_format_path(tmp_path: Path):
    @pickle_cache(tmp_path / 'test_{year}_{day}.pkl')
    def day_of_year(year: int, day: int):
        return date(year, 1, 1) + timedelta(days=day - 1)

    result = day_of_year(2025, 32)
    expected_result = date(2025, 2, 1)
    expected_path = tmp_path / 'test_2025_32.pkl'

    assert result == expected_result
    assert os.path.exists(expected_path)

    with open(expected_path, 'rb') as f:
        saved_result = pickle.load(f)
    assert saved_result == expected_result

    os.remove(expected_path)
