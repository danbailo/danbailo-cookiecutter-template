from types import NoneType, UnionType
from typing import Any, Union, get_args, get_origin


def is_union(type_: type) -> bool:
    origin = get_origin(type_)
    return origin is Union or origin is UnionType


def get_types(type_: type) -> list[type]:
    types = get_args(type_) if is_union(type_) else [type_]
    return list(types)


def cast_value(value: Any, types: list[type]) -> Any:
    """Faz a conversão do valor para um dos tipos passados em :types. Caso não seja
    possível fazer a conversão, uma exceção será lançada.
    """
    if value is None:
        if NoneType in types:
            return None
        types_name = ', '.join([t.__name__ for t in types])
        raise ValueError(f'O valor não pode ser nulo! Tipos permitidos: {types_name}.')

    for type_ in types:
        try:
            cast_value = type_(value)
            return cast_value
        except Exception:
            continue

    types_name = ', '.join([t.__name__ for t in types])
    raise ValueError(
        f'Não foi possível fazer a conversão do valor para os tipos: {types_name}. '
        f'Tipo do valor: {type(value).__name__}.'
    )


def get_type_names_from_object(object: type) -> list:
    """
    Retorna uma lista com os nomes das classes de um typing.
    """
    if isinstance(object, UnionType):
        return [t.__name__ for t in object.__args__]
    return [object.__name__]
