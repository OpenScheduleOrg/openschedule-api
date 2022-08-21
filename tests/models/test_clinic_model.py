import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError

from factory import ClinicBuilder

from app.models import session, Clinic, ClinicType
from app.exceptions import ValidationException
from app.validations import validate_payload
from app.constants import ValidationMessages

fake = Faker(["pt_BR"])


def test_should_raise_exception_when_clinic_cnpj_already_in_use(app):
    """
    Should raise a exception when cnpj is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*clinics.cnpj"):
        with app.app_context():
            cnpj = fake.company_id()
            session.add(ClinicBuilder().with_cnpj(cnpj).build_object())
            session.add(
                ClinicBuilder().complete().with_cnpj(cnpj).build_object())
            session.flush()


def test_should_raise_exception_when_clinic_phone_already_in_use(app):
    """
    Should raise a exception when phone is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*clinics.phone"):
        with app.app_context():
            phone = fake.msisdn()[-10:]
            session.add(ClinicBuilder().with_phone(phone).build_object())
            session.add(
                ClinicBuilder().complete().with_phone(phone).build_object())
            session.flush()


def test_should_not_raise_exception_if_payload_is_valid():
    """
    Should not raise exception if payload is valid
    """
    payload = ClinicBuilder().build()
    validate_payload(payload, Clinic.validators)

    payload = ClinicBuilder().complete().build()
    validate_payload(payload, Clinic.validators)


def test_should_raise_exception_when_validation_payload_fails():
    """
    Should raise a exception if payload validation fails
    """
    payload = {}
    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Clinic.validators)

    errors = e_info.value.errors
    assert len(errors) == 5
    assert "name" in errors and errors[
        "name"] == ValidationMessages.REQUIRED_FIELD.format("name")
    assert "cnpj" in errors and errors[
        "cnpj"] == ValidationMessages.REQUIRED_FIELD.format("cnpj")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.REQUIRED_FIELD.format("phone")
    assert "type" in errors and errors[
        "type"] == ValidationMessages.REQUIRED_FIELD.format("type")
    assert "address" in errors and errors[
        "address"] == ValidationMessages.REQUIRED_FIELD.format("address")

    payload = ClinicBuilder().with_name(fake.pystr(
        min_chars=1, max_chars=1)).with_cnpj("not a cnpj").with_phone(
            "not a phone number").with_latitude(-91).with_longitude(
                181).with_type(0).build()

    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Clinic.validators)

    errors = e_info.value.errors
    assert len(errors) == 6
    assert "name" in errors and "name" in errors["name"] and "least" in errors[
        "name"] and "2" in errors["name"]
    assert "cnpj" in errors and errors[
        "cnpj"] == ValidationMessages.INVALID_CNPJ.format("cnpj")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.INVALID_PHONE.format("phone")
    assert "type" in errors and errors[
        "type"] == ValidationMessages.NOT_IN_ENUM.format(
            0, ClinicType.__qualname__)
    assert "latitude" in errors and errors[
        "latitude"] == ValidationMessages.INVALID_LATITUDE
    assert "longitude" in errors and errors[
        "longitude"] == ValidationMessages.INVALIDE_LONGITUDE

    payload = ClinicBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).with_latitude(
            "not a number").with_longitude("not a number").build()

    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Clinic.validators)

    errors = e_info.value.errors
    assert len(errors) == 3
    assert "name" in errors and "name" in errors["name"] and "most" in errors[
        "name"] and "255" in errors["name"]
    assert "latitude" in errors and errors[
        "latitude"] == ValidationMessages.NOT_A_NUMBER
    assert "longitude" in errors and errors[
        "longitude"] == ValidationMessages.NOT_A_NUMBER
