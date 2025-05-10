import json
from pathlib import Path
from typing import Any

from legalops_commons.factories.logger import Logger, LoggerFactory
from legalops_commons.utils.environment.backends import BaseBackend
from legalops_commons.utils.environment.enums import EnvironmentNameEnum


class LocalFileBackend(BaseBackend):
    """
    Backend que carrega variáveis de ambiente e segredos de um arquivo local.
    O arquivo deve estar no formato JSON e seguir a seguinte estrutura:
    ```
    {
        "ENVIRONMENT_VARIABLES": {
            "VAR1": "value1",
            "VAR2": "value2",
            ...
        },
        "SECRETS": {
            "SECRET1": "secret_value1",
            "SECRET2": "secret_value2",
            ...
        }
    }
    ```
    """

    def __init__(
        self,
        path: Path | str,
        logger: Logger = LoggerFactory.new(),
    ) -> None:
        if isinstance(path, str):
            path = Path(path)
        super().__init__(logger)
        try:
            self.data = json.loads(path.read_bytes())
        except Exception as e:
            raise ValueError(
                f'Erro ao carregar variáveis de ambiente do arquivo {path}'
            ) from e

    def load_environment_variables(
        self, env_name: EnvironmentNameEnum
    ) -> dict[str, Any]:
        return self.data['ENVIRONMENT_VARIABLES']

    def get_secret(self, name) -> Any:
        return self.data['SECRETS'][name]
