import sys
from os import getenv

from dotenv import load_dotenv

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.factories.logger import Logger, LoggerFactory
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils import string as string_utils
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.environment.enums import EnvironmentNameEnum

load_dotenv()


def get_environment(
    values: str | EnvironmentNameEnum | list[str] | None = None,
) -> EnvironmentNameEnum:
    """Retorna o ambiente de desenvolvimento que será utilizado de acordo com o valor
    existente no parâmetro :values. Além disso carrega valores do `sys.argv`, ou seja,
    do cli, e também irá carregar a variável de ambiente `ENVIRONMENT`.

    Caso não exista nada, retorna o ambiente `TEST` por padrão.

    O usuário ainda tem a opção de passar parâmetros para escolher o ambiente direto
    na construção do objeto.

    Exemplo:
        ```python
        get_environment()  # TEST
        get_environment('local')  # LOCAL
        get_environment('prod')  # PROD
        get_environment('homolog')  # HOMOLOG
        ```
    """
    logger: Logger = LoggerFactory.new()
    if not values:
        values = []
    if not isinstance(values, list):
        values = [values]

    default_values = sys.argv + [getenv('ENVIRONMENT', EnvironmentNameEnum.TEST)]
    values = values + default_values

    for value in filter(None, values):
        value = string_utils.clean_string(value).upper()
        if value in iter(EnvironmentNameEnum):
            enviroment = EnvironmentNameEnum(value)
            break
    else:
        enviroment = EnvironmentNameEnum.TEST

    logger.info(f'Detectado ambiente "{enviroment}"')
    return enviroment
