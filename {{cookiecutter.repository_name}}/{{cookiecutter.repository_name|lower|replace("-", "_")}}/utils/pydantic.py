from pydantic import BaseModel, ValidationError


def get_fields_from_validation_error(validation_error: ValidationError) -> list[str]:
    errors: list[str] = []
    for error in validation_error.errors():
        error_field: str = error['loc'][0]
        errors.append(error_field)
    return errors


def validate_data_and_get_error_fields(data: dict, model: type[BaseModel]) -> list[str]:
    try:
        model(**data)
        return []

    except ValidationError as validation_error:
        return get_fields_from_validation_error(validation_error)
