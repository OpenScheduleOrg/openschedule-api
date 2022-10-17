import re
from datetime import date
from faker import Faker

from app.validations import validate_cpf, validate_phone, validate_required, validate_date, \
    validate_length, validate_cnpj, validate_enum, validate_email
from app.constants import ValidationMessages
from app.models import ClinicType

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


def test_validate_cnpj_when_valid_cnpj_should_return_none():
    """
    Must be return none if cnpj is valid
    """
    field = "cnpj"
    result = validate_cnpj(field, {field: fake.cnpj()})
    assert not result
    result = validate_cnpj(field, {field: fake.company_id()})
    assert not result


def test_validate_cnpj_when_invalid_cnpj_should_return_validation_result():
    """
    Must be return none if cnpj is invalid
    """
    field = "cnpj"
    assert validate_cnpj(
        field, {field: ""}) == ValidationMessages.INVALID_CNPJ.format(field)
    assert validate_cnpj(field,
                         {field: "10.270.561/1234-54"
                          }) == ValidationMessages.INVALID_CNPJ.format(field)


def test_validate_cnpj_should_remove_cnpj_mask():
    """
    Should remove cnpj mask
    """
    field = "cnpj"
    payload = {field: fake.cnpj()}
    validate_cnpj(field, payload)
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


def test_validate_phone_should_remove_phone_number_mask_and_9():
    """
    Should remove phone number mask and 9
    """
    field = "phone"
    payload = {field: "(86) 98767-8978"}
    validate_phone(field, payload)
    assert payload[field] == "8687678978"


def test_validate_email_when_valid_email_should_return_none():
    """
    Must be return none if email is valid
    """
    field = "email"
    assert not validate_email(field, {field: fake.email()})


def test_validate_email_should_return_validation_message_email_invalid():
    """
    Must be return validation message if email is invalid
    """
    field = "email"
    assert validate_email(
        field, {field: "notaemail@really"}) == ValidationMessages.INVALID_EMAIL
    assert validate_email(
        field, {field: "not a email"}) == ValidationMessages.INVALID_EMAIL


def test_validate_required_should_return_none_if_fields_are_in_body():
    """
    Should return none if field is in payload
    """
    field = "other_field"
    payload = {"some_field": "some data", "other_field": False}

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


def test_validate_length_should_return_none_if_string_has_correct_size():
    """
    Shold return None if string has correct size
    """
    field = "any_field"
    value = "Some quote"
    payload = {field: value}

    result = validate_length(field, payload, min_len=0, max_len=255)
    assert not result

    result = validate_length(field, payload, min_len=0, max_len=len(value))
    assert not result

    value = "four"
    payload[field] = value
    result = validate_length(field, payload, min_len=4, max_len=len(value))
    assert not result


def test_validate_length_should_return_validation_message_if_string_is_out_of_bounds(
):
    """
    Shold return validation message if string is out of bounds
    """
    field = "any_field"
    value = "Some quote"
    payload = {field: value}

    max_len = len(value) - 3
    result = validate_length(field, payload, min_len=0, max_len=max_len)
    assert result == ValidationMessages.MOST_CHARACTERS.format(field, max_len)

    min_len = len(value) + 3
    result = validate_length(field, payload, min_len=min_len, max_len=max_len)
    assert result == ValidationMessages.LEAST_CHARACTERS.format(field, min_len)


def test_validate_enum_should_return_none_if_number_match_with_enum():
    """
    Should return None if number match with enum
    """
    field = "any_field"
    value = ClinicType.PEDIATRIC.value
    payload = {field: value}

    result = validate_enum(field, payload, ClinicType)
    assert not result


def test_validate_length_should_return_validation_message_if_number_is_not_in_enum(
):
    """
    Shold return validation message if number is not in enum
    """
    field = "any_field"
    value = 0
    payload = {field: value}

    result = validate_enum(field, payload, ClinicType)
    assert result == ValidationMessages.NOT_IN_ENUM.format(
        value, ClinicType.__qualname__)
