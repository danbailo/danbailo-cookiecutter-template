from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel, ValidationError, model_validator

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.dict import force_all_keys_exist
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.pydantic import (
    get_fields_from_validation_error,
    validate_data_and_get_error_fields,
)


def test_get_fields_from_validation_error():
    class MyModel(BaseModel):
        field1: str
        field2: int
        field3: list

    result = []
    try:
        MyModel(**{})
    except ValidationError as validation_error:
        result = get_fields_from_validation_error(validation_error)

    assert result == ['field1', 'field2', 'field3']


@patch('{{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.pydantic.get_fields_from_validation_error')
def test_validate_data_and_get_error_fields_when_failure_exception(
    mock_get_fields_from_validation_error: MagicMock,
):
    with pytest.raises(Exception, match='mocked-exception'):
        validate_data_and_get_error_fields(
            data=dict(), model=MagicMock(side_effect=Exception('mocked-exception'))
        )
    mock_get_fields_from_validation_error.assert_not_called()


@pytest.mark.parametrize(
    'input_data, input_keys_to_validate, expected_result',
    [
        pytest.param(
            {
                'field2': 'value2',
                'field4': 'value4',
            },
            ['field1', 'field2', 'field3'],
            ['field1', 'field2', 'field3'],
            id='valida-erro-de-validacao-com-dependencia-1',
        ),
        pytest.param(
            {
                'field1': 'value1',
                'field2': 'value2',
                'field4': 'value4',
            },
            ['field2', 'field3'],
            ['field2', 'field3'],
            id='valida-erro-de-validacao-com-dependencia-2',
        ),
        pytest.param(
            {
                'field1': 'value1',
                'field2': 'value2',
                'field4': 'value4',
            },
            [],
            ['field3'],
            id='valida-erro-de-validacao-sem-dependencia-1',
        ),
        pytest.param(
            {
                'field1': 'value1',
                'field2': 'value2',
                'field3': 'value3',
                'field4': 'value4',
            },
            ['field1', 'field2', 'field3'],
            [],
            id='valida-sucesso',
        ),
    ],
)
def test_validate_data_and_get_error_fields_parametrized(
    input_data: dict,
    input_keys_to_validate: list[str],
    expected_result,
):
    """
    Teste de integração que valida o funcionamento de um modelo Pydantic ao realizarmos
    o input de um dicionário de dados com uma regra de negócio com campos dependentes implementados.
    """

    class MyModel(BaseModel):
        field1: str
        field2: str
        field3: str
        field4: str

        @model_validator(mode='before')
        def validate_dependent_fields(cls, root: dict) -> dict:
            # Configuração necessária para rodar os testes e injetar valores parametrizados.
            root = force_all_keys_exist(root, *input_keys_to_validate)
            return root

    result = validate_data_and_get_error_fields(input_data, MyModel)

    assert result == expected_result


def test_validate_data_and_get_error_fields_with_various_dependent_fields():
    """
    Teste de integração que valida o funcionamento de um modelo Pydantic ao realizarmos
    o input de um dicionário de dados com uma regra de negócio com campos dependentes implementados.
    """

    class MyModel(BaseModel):
        field1: str
        field2: str
        field3: str
        field4: str
        field5: str
        field6: str
        field7: str
        field8: str

        @model_validator(mode='before')
        def validate_dependent_fields(cls, root: dict) -> dict:
            root = force_all_keys_exist(root, 'field1', 'field2', 'field3')
            root = force_all_keys_exist(root, 'field3', 'field5')
            root = force_all_keys_exist(root, 'field7', 'field8')
            return root

    result = validate_data_and_get_error_fields(
        {
            'field1': 'mock',
            'field2': 'mock',
            'field4': 'mock',
            'field5': 'mock',
            'field6': 'mock',
            'field7': 'mock',
        },
        MyModel,
    )

    assert result == ['field1', 'field2', 'field3', 'field5', 'field7', 'field8']
