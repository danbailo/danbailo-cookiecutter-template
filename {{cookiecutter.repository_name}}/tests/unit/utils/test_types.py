from typing import Any, Optional, Union

from pytest import mark, raises

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.types import (
    cast_value,
    get_type_names_from_object,
    get_types,
    is_union,
)


class ExampleObject: ...


@mark.parametrize(
    'type_, expected_result',
    [
        (int, False),
        (str, False),
        (dict, False),
        (dict[str, int], False),
        (type(None), False),
        (list, False),
        (tuple, False),
        (Any, False),
        (Optional[Any], True),
        (Optional[int], True),
        (Union[int, str], True),
    ],
)
def test_is_union(type_: type, expected_result: bool):
    assert is_union(type_) == expected_result


@mark.parametrize(
    'type_, expected_result',
    [
        (int, [int]),
        (str, [str]),
        (dict, [dict]),
        (dict[str, int], [dict[str, int]]),
        (type(None), [type(None)]),
        (list, [list]),
        (tuple, [tuple]),
        (Any, [Any]),
        (Optional[Any], [Any, type(None)]),
        (Optional[int], [int, type(None)]),
        (Union[int, str], [int, str]),
    ],
)
def test_get_types(type_: type, expected_result: list[type]):
    assert get_types(type_) == expected_result


@mark.parametrize(
    'value, types, expected_result',
    [
        (1, [int], 1),
        ('1', [int], 1),
        (1, [float], 1.0),
        ('1', [int, str], 1),
        ('abc', [int, str], 'abc'),
        ('1', [str, int], '1'),
        ('1', [str], '1'),
        (1, [str], '1'),
        (1, [str, int], '1'),
        (1, [int, type(None)], 1),
        (1, [type(None), int], 1),
        (None, [str, type(None)], None),
        (None, [type(None)], None),
        (set(), [set], set()),
        (dict(), [dict], dict()),
        (list(), [list], list()),
        (dict(), [list], list()),
        (set(), [dict], dict()),
        (dict(), [set], set()),
        ('abc', [list], ['a', 'b', 'c']),
        ({1: 2, 3: 4}, [list], [1, 3]),
        ({1: 2, 3: 4}, [set], set([1, 3])),
        (1, [set, dict, list, type(None), int], 1),
    ],
)
def test_cast_value(value: Any, types: list[type], expected_result: Any):
    assert cast_value(value, types) == expected_result


def test_cast_value_error_cannot_be_none():
    with raises(
        ValueError, match='O valor não pode ser nulo! Tipos permitidos: int, str'
    ):
        cast_value(None, [int, str, dict, list, float])


@mark.parametrize(
    'value, types',
    [
        ('abc', [int]),
        ('abc', [dict, float, int, type(None)]),
        (1, [set, dict, list, type(None)]),
    ],
)
def test_cast_value_error_cannot_cast(value: Any, types: list[type]):
    types_name = ', '.join([t.__name__ for t in types])
    value_type_name = type(value).__name__

    with raises(
        ValueError,
        match=(
            'Não foi possível fazer a conversão do valor para os tipos: '
            f'{types_name}. Tipo do valor: {value_type_name}.'
        ),
    ):
        cast_value(value, types)


@mark.parametrize(
    ('typing', 'expected'),
    [
        (str, ['str']),
        (str | int, ['str', 'int']),
        (ExampleObject, ['ExampleObject']),
        (ExampleObject | str, ['ExampleObject', 'str']),
    ],
)
def test_get_type_names_from_object(typing: type, expected: list[str]):
    assert get_type_names_from_object(typing) == expected
