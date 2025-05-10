import json
from pathlib import Path
from sys import exit

from google.api_core.exceptions import (
    DeadlineExceeded,
    FailedPrecondition,
    PermissionDenied,
)
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import (
    SecretManagerServiceClient,
)
from google.cloud.secretmanager_v1.types.resources import SecretVersion
from google.cloud.secretmanager_v1.types.service import AccessSecretVersionResponse

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.clients.secret_manager.enums import SortingOrderEnum
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.clients.secret_manager.exceptions import SecretDisabledException
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.clients.secret_manager.types import SecretVersionItem
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.factories.logger import Logger, LoggerFactory


class SecretManagerClient:
    """Referência - https://cloud.google.com/secret-manager/docs/reference/libraries"""

    TIMEOUT: int = 10

    def __init__(
        self,
        service_account: Path | str | None = None,
        logger: Logger = LoggerFactory.new(),
    ):
        self.logger = logger
        if service_account:
            if isinstance(service_account, str):
                service_account = Path(service_account)
            self.client = SecretManagerServiceClient.from_service_account_json(
                service_account  # type: ignore[call-arg]
            )
        else:
            try:
                self.client = SecretManagerServiceClient()
            except DefaultCredentialsError:
                self.logger.warning(
                    'Renove seu token através do comando "gcloud auth application-default login" e tente novamente!'
                )
                exit(1)
        self.logger.debug('Client instanciado com sucesso!')

    def _build_name(
        self,
        secret: str,
        version: str = 'latest',
        project_id: str = 'digestojud',
    ) -> str:
        """Constrói o nome completo do secret como o manager o manipula no GCP.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        return f'projects/{project_id}/secrets/{secret}/versions/{version}'

    def _build_parent(
        self,
        secret: str,
        project_id: str = 'digestojud',
    ) -> str:
        """Constrói o diretório do secret como o manager manipula no GCP.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        return f'projects/{project_id}/secrets/{secret}'

    def _build_project_parent(
        self,
        project_id: str = 'digestojud',
    ) -> str:
        """Constrói o diretório do projeto de como o manager manipula no GCP.

        Args:
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        return f'projects/{project_id}'

    def _access_version(
        self,
        secret: str,
        version: str = 'latest',
        project_id: str = 'digestojud',
        raise_exc: bool = True,
    ) -> AccessSecretVersionResponse | None:
        """Constrói o nome completo do secret como o manager o manipula no GCP.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
            raise_exc (bool): flag indicando se deve lançar exception caso ocorra alguma.

        Raises:
            DeadlineExceeded: Erro causado pela invalidação do token do GCP.
            SecretDisabledException: Versão do secret desativada.
            PermissionDenied: Sem permissão de acesso ao secret.
            Exception: Erro inesperado.
        """
        name = self._build_name(secret, version, project_id)
        logger = self.logger.bind(
            secret=secret,
            version=version,
            project_id=project_id,
            raise_exc=raise_exc,
        )
        logger.debug('Pegando secret do Secret Manager...')
        try:
            response = self.client.access_secret_version(
                request={'name': name}, timeout=self.TIMEOUT
            )
            return response

        except DeadlineExceeded:
            logger.warning(
                'Renove seu token através do comando "gcloud auth application-default login" e tente novamente!'
            )
            exit(1)

        except FailedPrecondition:
            raise SecretDisabledException(secret, version, project_id)

        except PermissionDenied:
            if raise_exc is False:
                logger.debug(
                    'Renove seu token através do comando "gcloud auth application-default login" e tente novamente!',
                )
                return
            raise

        except Exception:
            if raise_exc is False:
                logger.warning(
                    'Não foi possível pegar o secret!',
                    exc_info=True,
                )
                return
            raise

    def _add_version(self, secret: str, value: str) -> SecretVersion:
        """Adiciona uma nova versão ao secret.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            value (str): valor que será adicionado ao secret.

        Returns:
            SecretVersion: resposta da requisição realizada a API do GCP.
        """
        parent = self._build_parent(secret)
        secret_version = self.client.add_secret_version(
            request={'parent': parent, 'payload': {'data': value.encode('UTF-8')}}
        )
        return secret_version

    def get(
        self,
        secret: str,
        version: str = 'latest',
        project_id: str = 'digestojud',
        force_value_as_string: bool = False,
        raise_exc: bool = True,
    ) -> str | dict:
        """Acessa o secret e retorna seu conteúdo. Por padrão, sempre irá apontar para
        a última versão do secret e se desejado, pode ser especificado a versão desse
        secret também, sendo a versão do secret um número como string.

        Caso essa varíavel seja apontada como um "json", é retornado um dict.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
            force_value_as_string (bool): flag indicando se o valor deve ser retornado como string.
            raise_exc (bool): flag indicando se deve lançar exception caso ocorra alguma.

        Returns:
            str | dict: valor do secret requisitado de acordo com a versão especificada.
        """
        response = self._access_version(secret, version, project_id, raise_exc)
        if response is None:
            self.logger.warning(
                'Secret não encontrado!',
                secret=secret,
                version=version,
                project_id=project_id,
                force_value_as_string=force_value_as_string,
                raise_exc=raise_exc,
            )
            return
        value = response.payload.data.decode('UTF-8')

        if force_value_as_string is False:
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                self.logger.debug(
                    'Não foi possível converter o valor para dict! Retornando como string...',
                )

        self.logger.info(
            'Secret obtido com sucesso!',
            secret=secret,
            version=version,
            project_id=project_id,
            force_value_as_string=force_value_as_string,
            raise_exc=raise_exc,
        )
        return value

    def enable(
        self,
        secret: str,
        version: str,
        project_id: str = 'digestojud',
    ) -> SecretVersion:
        """Habilita a versão do secret no GCP.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.

        Returns:
            SecretVersion: resposta da requisição realizada a API do GCP.
        """
        name = self._build_name(secret, version, project_id)
        secret_version = self.client.enable_secret_version(
            request={'name': name}, timeout=self.TIMEOUT
        )
        self.logger.info(
            'Secret habilitado com sucesso!',
            secret=secret,
            version=version,
            project_id=project_id,
        )
        return secret_version

    def disable(
        self,
        secret: str,
        version: str = 'latest',
        project_id: str = 'digestojud',
    ) -> SecretVersion | None:
        """Desabilita a versão do secret no GCP.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.

        Returns:
            SecretVersion | None: resposta da requisição realizada a API do GCP.
        """
        try:
            response = self._access_version(secret, version, project_id, raise_exc=True)
        except SecretDisabledException:
            self.logger.warning(
                'O secret já estava desabilitado!',
                secret=secret,
                version=version,
                project_id=project_id,
            )
            return

        secret_version = self.client.disable_secret_version(
            name=response.name, timeout=self.TIMEOUT
        )
        self.logger.info(
            'Secret desabilitado com sucesso!',
            secret=secret,
            version=version,
            project_id=project_id,
        )
        return secret_version

    def update(
        self,
        secret: str,
        value: str | dict,
        disable_latest_version: bool = True,
        version: str = 'latest',
        project_id: str = 'digestojud',
    ):
        """Atualiza o valor do secret no GCP, adicionando uma nova versão do secret no Manager.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            value (str | dict): valor que será adicionado a nova versão do secret.
            disable_latest_version (bool): flag indicando se deve desabilitar a última versão do secret.
            version (str): número da versão do secret, "latest" por padrão.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        if disable_latest_version is True:
            self.disable(secret, version, project_id)

        if isinstance(value, dict):
            value = json.dumps(value)

        self._add_version(secret, value)
        self.logger.info(
            'Secret atualizado com sucesso!',
            secret=secret,
            disable_latest_version=disable_latest_version,
            version=version,
            project_id=project_id,
        )

    def list_versions(
        self, secret: str, project_id: str = 'digestojud'
    ) -> list[SecretVersionItem]:
        """Lista todas as versões de um secret.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        parent = self._build_parent(secret, project_id)
        return [
            SecretVersionItem(version=item.name.split('/')[-1], status=item.state)
            for item in self.client.list_secret_versions(request={'parent': parent})
        ]

    def get_enabled_version(
        self,
        secret: str,
        project_id: str = 'digestojud',
        sorting: SortingOrderEnum = SortingOrderEnum.LATEST,
    ) -> SecretVersionItem | None:
        """Retona a versão habilitada do secret de acordo com a ordenação no parâmetro `sorting`.

        Args:
            secret (str): nome do secret no manager, ex: LEGALOPS_CLIENTS_ZOHO_VAULT.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
            sorting (SortingOrderEnum): formato que deverá retornar a ordenação das versões.
        """
        versions = self.list_versions(secret, project_id)
        if sorting == SortingOrderEnum.FIRST:
            versions.reverse()
        for version in versions:
            if version.status == 1:
                return version

    def list(
        self,
        filter: str = 'LEGALOPS',
        project_id: str = 'digestojud',
    ) -> list[str]:
        """Lista todas os secrets do GCP de acordo com o filtro indicado no parâmetro `filter`.

        Args:
            filter (str): valor que será filtrado os secrets para serem retornados.
            project_id (str): ID do projeto, podendo ser o nome por extenso ou valor numérico.
        """
        parent = self._build_project_parent(project_id)
        return [
            item.name.split('/')[-1]
            for item in self.client.list_secrets(
                request={'parent': parent, 'filter': filter}
            )
        ]

    # DEPRECATED
    def access_secret_version(
        self,
        secret: str,
        project_id: str = 'digestojud',
        version: str = 'latest',
        is_json: bool = False,
        raise_exc: bool = True,
    ):
        self.logger.warning(
            'Método depreciado! Utilize o método `get` em vez de `access_secret_version`!'
        )
        return self.get(
            secret,
            version,
            project_id,
            raise_exc,
        )
