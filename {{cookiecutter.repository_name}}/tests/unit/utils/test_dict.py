from unittest.mock import MagicMock, patch

import pytest

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.dict import (
    force_all_keys_exist,
    invert_dict,
    merge_dicts,
    update_data_from_objects,
)


@pytest.mark.parametrize(
    'input_data1, input_data2, expected_data',
    [
        pytest.param(
            {'foo': 'bar', 'test': 'variable'},
            [
                {'foo': 'bar', 'dg_event_object_data__origem': 'teste'},
                {'lorem': 'ipsum', 'aaaa': 'bbb'},
            ],
            {
                'foo': 'bar',
                'dg_event_object_data__origem': 'teste',
                'lorem': 'ipsum',
                'aaaa': 'bbb',
                'test': 'variable',
            },
            id='validate-data2-list-1',
        ),
        pytest.param(
            {
                'dg_event_object_url': 'https://foo',
                'dg_event_object_data__origem': 'email',
            },
            [
                {'foo': 'bar', 'dg_event_object_data__origem': 'teste'},
                {'lorem': 'ipsum', 'aaaa': 'bbb'},
            ],
            {
                'foo': 'bar',
                'dg_event_object_data__origem': 'email',
                'lorem': 'ipsum',
                'aaaa': 'bbb',
                'dg_event_object_url': 'https://foo',
            },
            id='validate-data2-list-2',
        ),
        pytest.param(
            {'foo': 'bar', 'test': 'variable'},
            {'foo': 'bar', 'lorem': 'ipsum', 'dg_event_object_data__origem': 'teste'},
            {
                'foo': 'bar',
                'lorem': 'ipsum',
                'dg_event_object_data__origem': 'teste',
                'test': 'variable',
            },
            id='validate-data1-data2-dict-1',
        ),
        pytest.param(
            {'right': 'data'},
            {'left': 'data'},
            {
                'left': 'data',
                'right': 'data',
            },
            id='validate-data1-data2-dict-2',
        ),
        pytest.param(
            {},
            {'left': 'data'},
            {
                'left': 'data',
            },
            id='empty-data-1',
        ),
        pytest.param(
            {'right': 'data'},
            {},
            {
                'right': 'data',
            },
            id='empty-data-2',
        ),
        pytest.param(
            {},
            {},
            {},
            id='empty-data-3',
        ),
    ],
)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.dict.LoggerFactory.new')
def test_update_data_from_objects(
    mocked_logger: MagicMock,
    input_data1: dict,
    input_data2: dict | list,
    expected_data: dict,
):
    assert update_data_from_objects(input_data1, input_data2) == expected_data
    if isinstance(input_data2, list):
        has_calls = 0
        for call in mocked_logger.return_value.debug.call_args_list:
            if 'Atualizando objeto de retorno...' in call.args:
                has_calls += 1
        assert has_calls, 'Logger not called!'
    mocked_logger.return_value.debug.assert_called_with(
        'Criado novo objeto!', to_return=expected_data
    )


@pytest.mark.parametrize(
    'input_data1, input_data2, expected_data',
    [
        pytest.param(
            {'test': 'variable'},
            [
                {'foo': 'bar', 'dg_event_object_data__origem': 'teste'},
                {'lorem': 'ipsum', 'aaaa': 'bbb'},
                {'some': 'field'},
            ],
            [
                {
                    'foo': 'bar',
                    'dg_event_object_data__origem': 'teste',
                    'test': 'variable',
                },
                {'lorem': 'ipsum', 'aaaa': 'bbb', 'test': 'variable'},
                {'some': 'field', 'test': 'variable'},
            ],
            id='validate-data2-list-1',
        ),
        pytest.param(
            {
                'dg_event_object_url': 'https://foo',
                'dg_event_object_data__origem': 'email',
                'my': 'field',
            },
            [
                {'foo': 'bar', 'dg_event_object_data__origem': 'teste'},
                {'lorem': 'ipsum', 'aaaa': 'bbb'},
            ],
            [
                {
                    'dg_event_object_data__origem': 'teste',
                    'dg_event_object_url': 'https://foo',
                    'foo': 'bar',
                    'my': 'field',
                },
                {
                    'aaaa': 'bbb',
                    'dg_event_object_data__origem': 'email',
                    'dg_event_object_url': 'https://foo',
                    'lorem': 'ipsum',
                    'my': 'field',
                },
            ],
            id='validate-data2-list-2',
        ),
        pytest.param(
            {},
            [
                {'foo': 'bar', 'dg_event_object_data__origem': 'teste'},
                {'lorem': 'ipsum', 'aaaa': 'bbb'},
            ],
            [
                {
                    'foo': 'bar',
                    'dg_event_object_data__origem': 'teste',
                },
                {
                    'lorem': 'ipsum',
                    'aaaa': 'bbb',
                },
            ],
            id='empty-data-1',
        ),
        pytest.param(
            {
                'dg_event_object_url': 'https://foo',
                'dg_event_object_data__origem': 'email',
                'my': 'field',
            },
            [
                {},
                {},
            ],
            [
                {
                    'dg_event_object_url': 'https://foo',
                    'dg_event_object_data__origem': 'email',
                    'my': 'field',
                },
                {
                    'dg_event_object_url': 'https://foo',
                    'dg_event_object_data__origem': 'email',
                    'my': 'field',
                },
            ],
            id='empty-data-2',
        ),
        pytest.param(
            {},
            [
                {},
            ],
            [
                {},
            ],
            id='empty-data-3',
        ),
    ],
)
@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.dict.LoggerFactory.new')
def test_update_data_from_objects_inside_list(
    mocked_logger: MagicMock, input_data1: dict, input_data2: list, expected_data: list
):
    """Injeta os dados do `input_data1` em cada objeto dentro da lista `input_data2`"""
    for index, item in enumerate(input_data2):
        input_data2[index] = update_data_from_objects(item, input_data1)
        mocked_logger.return_value.debug.assert_called_with(
            'Criado novo objeto!', to_return=input_data2[index]
        )
    for call in mocked_logger.return_value.debug.call_args_list:
        assert 'Atualizando objeto de retorno...' not in call.args
    assert input_data2 == expected_data


def test_invert_dict():
    input_dict = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
    }
    result = invert_dict(input_dict)

    assert result == {
        'value1': 'key1',
        'value2': 'key2',
        'value3': 'key3',
    }


@pytest.mark.parametrize(
    'input_data, input_keys, expected_result',
    [
        pytest.param(
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            ['key1', 'key2', 'key3'],
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            id='validate-subset-1',
        ),
        pytest.param(
            {1: 'value1', 2: 'value2', 3: 'value3'},
            [1, 2, 3],
            {1: 'value1', 2: 'value2', 3: 'value3'},
            id='validate-subset-2',
        ),
        pytest.param(
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            ['key2'],
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            id='validate-subset-3',
        ),
        pytest.param(
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            ['is-not-subset-key'],
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            id='validate-subset-4',
        ),
        pytest.param(
            {'key1': 'value1', 'key3': 'value3'},
            ['key1', 'key2', 'key3'],
            {},
            id='validate-not-subset-1',
        ),
        pytest.param(
            {1: 'value1', 2: 'value2'}, [1, 2, 3], {}, id='validate-not-subset-3'
        ),
        pytest.param(
            {'key2': 'value2', 'key3': 'value3', 'key4': 'value4', 'key5': 'value5'},
            ['key1', 'key3'],
            {'key2': 'value2', 'key4': 'value4', 'key5': 'value5'},
            id='validate-not-subset-3',
        ),
        pytest.param(
            {'key1': None, 'key2': 'value2', 'key3': 'value3'},
            ['key1', 'key2', 'key3'],
            {},
            id='validate-none-values',
        ),
    ],
)
def test_force_all_keys_exist(
    input_data: dict, input_keys: list, expected_result: dict
):
    result = force_all_keys_exist(input_data, *input_keys)

    assert result == expected_result


@pytest.mark.parametrize(
    'input_dict1, input_dict2, expected_result',
    [
        pytest.param(
            {'a': 1, 'b': 2},
            {'b': 3, 'c': 4},
            {'a': 1, 'b': 2, 'c': 4},
            id='basic_merge',
        ),
        pytest.param(
            {'a': 1, 'b': 2},
            {'b': 3, 'c': 4, 'd': ['lorem']},
            {'a': 1, 'b': 2, 'c': 4, 'd': ['lorem']},
            id='basic_merge_with_complex_data',
        ),
        pytest.param(
            {'a': None, 'b': 2},
            {'a': 1, 'c': 4},
            {'a': 1, 'b': 2, 'c': 4},
            id='none_value_in_dict1',
        ),
        pytest.param(
            {'a': 1, 'b': False},
            {'b': True, 'c': 4},
            {'a': 1, 'b': True, 'c': 4},
            id='boolean_values',
        ),
        pytest.param(
            {'a': 1, 'b': None},
            {'b': False, 'c': 4},
            {'a': 1, 'b': False, 'c': 4},
            id='boolean_and_none_values',
        ),
        pytest.param(
            {'a': [], 'b': 2},
            {'a': [1, 2], 'c': 4},
            {'a': [1, 2], 'b': 2, 'c': 4},
            id='empty_list_in_dict1',
        ),
        pytest.param({'a': 1, 'b': 2}, {}, {'a': 1, 'b': 2}, id='empty_dict2'),
        pytest.param({}, {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, id='empty_dict1'),
        pytest.param({}, {}, {}, id='both_empty_dicts'),
    ],
)
def test_merge_dicts(input_dict1: dict, input_dict2: dict, expected_result: dict):
    result = merge_dicts(input_dict1, input_dict2)
    assert result == expected_result
