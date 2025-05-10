from enum import StrEnum


class EnvironmentNameEnum(StrEnum):
    """Nomes identificadores dos ambientes de desenvolvimento.

    TEST: Ambiente de teste, sem acesso a serviços externos.

    LOCAL: Execução utilizando recursos locais, com acesso a segredos externos.

    LOCAL_PROD: Execução local com acesso a recursos do ambiente de produção.

    HOMOLOG: Execução local com acesso a recursos do ambiente de homologação.

    PROD: Ambiente exclusivo para produção.
    """

    TEST = 'TEST'
    LOCAL = 'LOCAL'
    LOCAL_PROD = 'LOCAL_PROD'
    HOMOLOG = 'HOMOLOG'
    PROD = 'PROD'
