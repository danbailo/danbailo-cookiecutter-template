from pathlib import Path
from typing import Any

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.clients.secret_manager.client import SecretManagerClient
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.enums import LegalOpsClientsEnum
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.factories.logger import Logger, LoggerFactory
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.environment.backends import BaseBackend
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.environment.enums import EnvironmentNameEnum


class SecretManagerBackend(BaseBackend):
    """
    Backend que carrega variáveis de ambiente e segredos do Secret Manager do GCP.
    """

    def __init__(
        self,
        project_name: LegalOpsClientsEnum,
        service_account: Path | str | None = None,
        logger: Logger = LoggerFactory.new(),
    ) -> None:
        self.project_name = project_name.upper()
        self.client = SecretManagerClient(service_account, logger)
        super().__init__(logger)

    def load_environment_variables(
        self, env_name: EnvironmentNameEnum
    ) -> dict[str, Any]:
        env_name = env_name.upper()
        secret_name = f'LEGALOPS_CLIENTS_{self.project_name}_{env_name}_ENV'
        logger = self.logger.bind(
            ambiente=env_name, projeto=self.project_name, secret_name=secret_name
        )

        logger.debug('Carregando variáveis do Secret Manager...')
        data = self.client.get(secret_name)
        logger.info('Variáveis de ambiente carregadas!')

        return data

    def get_secret(self, name: str) -> Any:
        secret_value = self.client.get(name)
        return secret_value
