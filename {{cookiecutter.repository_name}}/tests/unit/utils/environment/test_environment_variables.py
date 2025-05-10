import pytest

from legalops_commons.utils.environment import (
    BaseEnvironmentVariables,
    Field,
)
from legalops_commons.utils.environment.enums import EnvironmentNameEnum
from tests.utils.environment.utils import DictBackend


class MockedEnv(BaseEnvironmentVariables):
    my_user: str = Field('MY_USER')
    my_password: int = Field('MY_PASSWORD')


def test_environment_variables_init():
    vars = {'MY_USER': 'user', 'MY_PASSWORD': '123456', 'FOO': 'bar'}
    backend = DictBackend(vars=vars)

    TEST_ENV = MockedEnv(backend, EnvironmentNameEnum.TEST)

    assert TEST_ENV.my_user == 'user'
    assert TEST_ENV.my_password == 123456
    assert 'FOO' not in TEST_ENV._field_names


def test_environment_variables_incomplete_throws_error():
    vars = {'MY_USER': 'user'}
    backend = DictBackend(vars=vars)

    with pytest.raises(
        ValueError, match="Há campos que não foram preenchidos: {'MY_PASSWORD'}"
    ):
        _ = MockedEnv(backend, EnvironmentNameEnum.TEST)
