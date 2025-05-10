from unittest.mock import MagicMock, patch

import pytest

from legalops_commons.utils.environment import (
    get_environment,
)
from legalops_commons.utils.environment.enums import EnvironmentNameEnum

TEST_CASES = {
    'prod-1': (['lorem', 'ipsum', 'prod'], EnvironmentNameEnum.PROD),
    'prod-2': ('prod', EnvironmentNameEnum.PROD),
    'prod-3': ('PROD', EnvironmentNameEnum.PROD),
    'homolog-1': ('homolog', EnvironmentNameEnum.HOMOLOG),
    'homolog-2': ('HOMOLOG', EnvironmentNameEnum.HOMOLOG),
    'homolog-3': (['homolog', 'prod', 'local'], EnvironmentNameEnum.HOMOLOG),
    'test-1': ('test', EnvironmentNameEnum.TEST),
    'test-2': ('TEST', EnvironmentNameEnum.TEST),
    'test-3': (['TeSt', 'prod', 'local'], EnvironmentNameEnum.TEST),
    'local_prod-1': ('local_prod', EnvironmentNameEnum.LOCAL_PROD),
    'local-2': ('local', EnvironmentNameEnum.LOCAL),
    'local-3': (['local', 'foo', None], EnvironmentNameEnum.LOCAL),
    'valida-valor-default-local-1': ('hm', EnvironmentNameEnum.TEST),
    'valida-valor-default-local-2': ('prd', EnvironmentNameEnum.TEST),
    'valida-valor-default-local-3': ('producao', EnvironmentNameEnum.TEST),
    'valida-valor-default-local-4': ('PRODUCAO', EnvironmentNameEnum.TEST),
    'valida-valor-default-local-5': ('HOMOLOGACAO', EnvironmentNameEnum.TEST),
    'valida-valor-default-local-6': (
        ['lorem', 'ipsum', 'tst'],
        EnvironmentNameEnum.TEST,
    ),
    'valida-valor-default-local-7': ('foo', EnvironmentNameEnum.TEST),
}


@pytest.mark.parametrize(
    'input_data, expected_data',
    TEST_CASES.values(),
    ids=TEST_CASES.keys(),
)
@patch('legalops_commons.factories.logger.LoggerFactory.new')
def test_get_environment(
    mocked_logger: MagicMock, input_data: str, expected_data: EnvironmentNameEnum
):
    assert get_environment(input_data) == expected_data
    mocked_logger.return_value.info.assert_called_once_with(
        f'Detectado ambiente "{expected_data}"'
    )
