from typing import Any

import pytest

from legalops_commons.utils.environment import BaseSecrets, Field

from .utils import DictBackend


class MockedSecrets(BaseSecrets):
    api_key: str = Field('API_KEY')
    account: dict[str, Any] = Field('ACCOUNT')


def test_secrets_init():
    vars = {
        'API_KEY': '<KEY>',
        'ACCOUNT': {'username': 'user', 'password': 123456},
        'FOO': 'bar',
    }
    backend = DictBackend(vars=vars)

    TEST_SECRET = MockedSecrets(backend)

    assert TEST_SECRET.api_key == '<KEY>'
    assert TEST_SECRET.account == {'username': 'user', 'password': 123456}
    assert 'FOO' not in TEST_SECRET._field_names


def test_secrets_incomplete_throws_error():
    vars = {'API_KEY': '<KEY>'}
    backend = DictBackend(vars=vars)

    TEST_SECRET = MockedSecrets(backend)

    with pytest.raises(KeyError, match='ACCOUNT'):
        _ = TEST_SECRET.api_key
        _ = TEST_SECRET.account


def test_secrets_always_loads_from_backend():
    call_count = 0

    class CountDictBackend(DictBackend):
        def get_secret(self, name):
            nonlocal call_count
            call_count += 1
            return super().get_secret(name)

    vars = {'API_KEY': '<KEY>', 'ACCOUNT': {'username': 'user', 'password': 123456}}
    backend = CountDictBackend(vars=vars)

    TEST_SECRET = MockedSecrets(backend)

    assert call_count == 0
    _ = TEST_SECRET.api_key
    assert call_count == 1
    _ = TEST_SECRET.account
    assert call_count == 2
