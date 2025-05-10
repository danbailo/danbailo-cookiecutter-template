from dataclasses import dataclass
from typing import Any, get_type_hints

from legalops_commons.utils.environment.backends import BaseBackend
from legalops_commons.utils.environment.enums import EnvironmentNameEnum
from legalops_commons.utils.types import (
    cast_value,
    get_types,
)


@dataclass(slots=True)
class Field:
    name: str


class BaseVariables:
    """Classe base para variáveis de ambiente e secrets. O objetivo dessa classe
    é mapear os campos declarados na classe filha, armazenando sua tipagem e nome
    real (alias). Apenas mapeia os campos que são instâncias de Field.

    Por exemplo, uma classe instanciada assim:
    ```python
    class MyVar(BaseVariables):
        foo: str = Field('FOO')
        bar: int | None = Field('BAR')
    ```

    Terá os campos mapeados da seguinte forma:
    ```python
    self._types = {'foo': [str], 'bar': [int, NoneType]}
    self._field_names = {'FOO': 'foo', 'BAR': 'bar'}
    ```

    Na prática, essa classe não deve ser instanciada ou herdada diretamente.
    Deve-se herdar das classes `BaseEnvironmentVariables` ou `BaseSecrets`.
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseVariables:
            raise TypeError('Classe não pode ser instanciada diretamente')
        return super().__new__(cls)

    def __init__(self):
        # Inicializa o _types primeiro para ele ser reconhecido no
        # __getattribute__ sobrescrito no BaseSecrets
        self._types = {}
        self._types, self._field_names = self._map_fields()

    def _map_fields(self):
        """Constrói o dicionário de tipos e nomes dos campos"""
        types: dict[str, list[type]] = {}
        field_names: dict[str, str] = {}
        for var_name, type_hint in get_type_hints(self.__class__).items():
            field = getattr(self, var_name, None)
            if not isinstance(field, Field):
                continue
            types[var_name] = get_types(type_hint)
            field_names[field.name] = var_name
        return types, field_names

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(self._types.keys())})'


class BaseEnvironmentVariables(BaseVariables):
    """Classe base que implementa a lógica de carregamento das variáveis de ambiente.
    Ao instanciar a classe, ela irá carregar as variáveis de ambiente do backend
    selecionado e preencher os campos mapeados.

    Para utilizar, basta criar uma classe que herda de `BaseEnvironmentVariables` e
    definir os campos que deseja mapear para variáveis de ambiente.

    Exemplo:
    ```python
    class MyEnvironmentVariables(BaseEnvironmentVariables):
        camunda_url: str = Field('CAMUNDA_URL_ENGINE')
        oauth_token_url: str = Field('OAUTH_TOKEN_URL')


    ENV = MyEnvironmentVariables(backend, EnvironmentNameEnum.HOMOLOG)
    ```
    """

    def __init__(self, backend: BaseBackend, environment_name: EnvironmentNameEnum):
        super().__init__()
        # Carrega as variáveis de ambiente
        variables = backend.load_environment_variables(environment_name)
        fields_set = set()
        for name, value in variables.items():
            # Ignora campo que não está presente na classe
            field_name = self._field_names.get(name)
            if not field_name:
                continue
            value = cast_value(value, self._types[field_name])
            setattr(self, field_name, value)
            fields_set.add(name)
        # Lança exceção se a classe não foi totalmente preenchida
        if remaining_fields := self._field_names.keys() - fields_set:
            raise ValueError(f'Há campos que não foram preenchidos: {remaining_fields}')


class BaseSecrets(BaseVariables):
    """Classe base que implementa a lógica de obtenção dos secrets.
    Ao ler um campo mapeado pela classe, ela irá buscar o valor do secret no backend.

    Para utilizar, basta criar uma classe que herda de `BaseSecrets` e definir os campos
    que deseja mapear para secrets.

    Exemplo:
    ```python
    class MySecrets(BaseSecrets):
        password: int = Field('PASSWORD')
        api_key: str = Field('API_KEY')


    SECRETS = MySecrets(backend)"""

    def __init__(self, backend: BaseBackend):
        super().__init__()
        self._backend = backend

    def __getattribute__(self, name: str) -> Any:
        # Verifica se o atributo lido é um Field mapeado
        field_types = super().__getattribute__('_types').get(name)
        if not field_types:
            return super().__getattribute__(name)
        # Busca o valor do secret no backend
        field_name = object.__getattribute__(self, name).name
        value = self._backend.get_secret(field_name)
        value = cast_value(value, field_types)
        return value
