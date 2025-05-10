from typing import Any

from typer import BadParameter


class DictTyper:
    """Implementa o tipo `dict` para ser utilizado via cli.

    Exemplo:
        python -m main --option "{'test': 1}"

    Onde a opção `option` recebe um valor que será parseado num dict Python.
    """

    @classmethod
    def parse_value(cls, value: Any) -> dict[Any, Any]:
        try:
            to_return = eval(value)
        except Exception:
            raise Exception(
                f'Não foi possível converter o valor num objeto! - valor: {value}'
            )

        if not isinstance(to_return, dict):
            raise BadParameter(f'O valor passado não é um dicionário! - valor: {value}')

        return to_return
