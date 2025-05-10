from pathlib import Path
from typing import Any

from legalops_commons.enums import LegalOpsClientsEnum
from legalops_commons.factories.logger import Logger, LoggerFactory
from legalops_commons.utils.environment.backends.base import BaseBackend
from legalops_commons.utils.environment.backends.local_file import (
    LocalFileBackend,
)
from legalops_commons.utils.environment.backends.secret_manager import (
    SecretManagerBackend,
)
from legalops_commons.utils.environment.enums import EnvironmentNameEnum


class LocalSecretManagerBackend(BaseBackend):
    """
    Backend que carrega variáveis de ambiente de um arquivo local e segredos
    do Secret Manager do GCP.
    """

    def __init__(
        self,
        path: Path | str,
        project_name: LegalOpsClientsEnum,
        service_account: Path | str | None = None,
        logger: Logger = LoggerFactory.new(),
    ) -> None:
        super().__init__(logger)
        self._local_file_backend = LocalFileBackend(path, logger)
        self._secret_manager_backend = SecretManagerBackend(
            project_name, service_account, logger
        )

    def load_environment_variables(
        self, env_name: EnvironmentNameEnum
    ) -> dict[str, Any]:
        return self._local_file_backend.load_environment_variables(env_name)

    def get_secret(self, name) -> Any:
        return self._secret_manager_backend.get_secret(name)
