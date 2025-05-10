from abc import ABC, abstractmethod
from typing import Any

from legalops_commons.factories.logger import Logger, LoggerFactory
from legalops_commons.utils.environment.enums import EnvironmentNameEnum


class BaseBackend(ABC):
    """
    Classe abstrata que define o comportamento de um backend de variáveis.
    Um backend deve ser capaz de carregar variáveis de ambiente e segredos.

    Variáveis de ambiente são valores que são fixos dentro de um ambiente, que
    sofrem poucas alterações. Exemplo: URL de uma API

    Segredos são variáveis com conteúdo sensível e/ou que precisam ser sempre
    recarregadas com o valor atualizado, se sua fonte for um serviço externo.
    Exemplo: credenciais de acesso
    """

    def __init__(self, logger: Logger = LoggerFactory()):
        self.logger = logger
        self.logger.debug(
            'Backend inicializado com sucesso!', backend=self.__class__.__name__
        )

    @abstractmethod
    def load_environment_variables(
        self, env_name: EnvironmentNameEnum
    ) -> dict[str, Any]:
        """
        Carrega todas as variáveis de um determinado ambiente e as retorna em
        formato de dicionário
        """
        pass

    @abstractmethod
    def get_secret(self, name: str) -> Any:
        """
        Obtém o valor de um determinado segredo
        """
        pass
