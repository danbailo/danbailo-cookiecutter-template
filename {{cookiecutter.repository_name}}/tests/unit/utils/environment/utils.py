from unittest.mock import Mock

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.environment.backends import BaseBackend
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.environment.enums import EnvironmentNameEnum


class DictBackend(BaseBackend):
    def __init__(self, vars: dict):
        super().__init__(logger=Mock())
        self.vars = vars

    def load_environment_variables(self, env_name: EnvironmentNameEnum) -> dict:
        return self.vars

    def get_secret(self, name):
        return self.vars[name]
