import re
from datetime import date
import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError

from app.validations import validate_cpf, validate_phone, validate_required, validate_date, \
    validate_unique
from app.exceptions import ValidationException
from app.constants import ValidationMessages

fake = Faker(["pt_BR"])


def test_validate_cpf_when_valid_cpf_should_return_none():
    """
    Must be return none if cpf is valid
    """
    field = "cpf"
    result = validate_cpf(field, {field: fake.cpf()})
    assert not result
    result = validate_cpf(field, {field: fake.ssn()})
    assert not result


def test_validate_cpf_when_invalid_cpf_should_return_validation_result():
    """
    Must be return none if cpf is invalid
    """
    field = "cpf"
    assert validate_cpf(
        field, {field: ""}) == ValidationMessages.INVALID_CPF.format(field)
    assert validate_cpf(field,
                        {field: "111.111.111-12"
                         }) == ValidationMessages.INVALID_CPF.format(field)


def test_validate_cpf_should_remove_cpf_mask():
    """
    Should remove cpf mask
    """
    field = "cpf"
    payload = {field: fake.cpf()}
    validate_cpf(field, payload)
    assert not re.match(r"\D", payload[field])


def test_validate_phone_when_valid_phone_number_should_return_none():
    """
    Must be return none if phone number is valid
    """
    field = "phone"
    assert not validate_phone(
        field,
        {field: fake.cellphone_number().replace("+55", "").replace("(0", "")})
    assert not validate_phone(field, {field: fake.msisdn()[-10:]})


def test_validate_phone_when_invalid_phone_number_should_return_validation_message(
):
    """
    Must be return validation message if phone number is invalid
    """
    field = "phone"
    assert validate_phone(
        field, {field: ""}) == ValidationMessages.INVALID_PHONE.format(field)
    assert validate_phone(
        field,
        {field: "86173880"}) == ValidationMessages.INVALID_PHONE.format(field)
    assert validate_phone(field,
                          {field: "(86) 9173-880"
                           }) == ValidationMessages.INVALID_PHONE.format(field)


def test_validate_phone_should_remove_phone_number_mask():
    """
    Should remove phone number mask
    """
    field = "phone"
    payload = {field: fake.cellphone_number().replace("+55", "")}
    validate_phone(field, payload)
    assert not re.match(r"\D", payload[field])


def test_validate_required_should_return_none_if_fields_are_in_body():
    """
    Should return none if field is in payload
    """
    field = "other_field"
    payload = {"some_field": "some data", "other_field": "other some data"}

    result = validate_required(field, payload)
    assert not result


def test_validate_required_should_return_validation_result_if_field_not_body():
    """
    Should return none if field not in payload
    """

    field = "some_field_not_in_payload"
    result = validate_required(field, {})

    assert result == ValidationMessages.REQUIRED_FIELD.format(field)


def test_validate_date_should_return_none_if_fields_has_date():
    """
    Should return none if field has a date
    """
    field = "birthdate"
    result = validate_date(field, {field: fake.date_between()})
    assert not result
    result = validate_date(field, {field: fake.date_between().isoformat()})
    assert not result


def test_validate_date_should_return_validation_result_if_field_not_body():
    """
    Should return none if field not in payload
    """

    field = "birthdate"
    result = validate_date(field, {field: "not is a date"})

    assert result == ValidationMessages.INVALID_DATE.format(field)


def test_validate_date_should_convert_iso_date_to_object_date_if_valid():
    """
    Should convert iso date to object date if valid
    """
    field = "birthdate"
    payload = {field: fake.date_between().isoformat()}
    validate_date(field, payload)
    assert isinstance(payload[field], date)


def test_validate_unique_should_not_raise_exception_if_unique_not_in_message():
    """
    Should not raise exception if UNIQUE not in exception
    """
    integrity_error = IntegrityError(
        None, None, Exception("Something related to FOREIGN KEY"))
    validate_unique(integrity_error,
                    {"some_field": "Some very describable message"})


def test_validate_unique_should_not_raise_exception_if_none_field_in_message():
    """
    Should not raise exception if UNIQUE not in exception
    """
    integrity_error = IntegrityError(
        None, None,
        Exception("UNIQUE constraint failed: table_name.field_name"))
    validate_unique(
        integrity_error, {
            "some_field": "Some very describable message",
            "other_field": "Other very describable message",
        })


def test_validate_unique_should_raise_when_field_unique_message():
    """
    Should not raise exception if UNIQUE not in exception
    """
    field_name = "some_field"
    integrity_error = IntegrityError(
        None, None,
        Exception(f"UNIQUE constraint failed: table_name.{field_name}"))
    fields_messages = {
        field_name: "Some very describable message",
        "other_field": "Other very describable message",
    }

    with pytest.raises(ValidationException) as e_info:
        validate_unique(integrity_error, fields_messages)

    validation_error = e_info.value
    assert field_name in validation_error.errors
    assert validation_error.errors[field_name] == fields_messages[field_name]
