import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError

from factory import PatientBuilder

from app.models import Patient, session
from app.exceptions import ValidationException
from app.validations import validate_payload
from app.constants import ValidationMessages

fake = Faker(["pt_BR"])


def test_should_raise_exception_when_patient_cpf_already_in_use(app):
    """
    Should raise a exception when cpf is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*patients.cpf"):
        with app.app_context():
            cpf = fake.cpf()
            session.add(
                PatientBuilder().complete().with_cpf(cpf).build_object())
            session.add(
                PatientBuilder().complete().with_cpf(cpf).build_object())
            session.flush()


def test_should_raise_exception_when_patient_phone_already_in_use(app):
    """
    Should raise a exception when phone is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*patients.phone"):
        with app.app_context():
            phone = fake.msisdn()[-10:]
            session.add(
                PatientBuilder().complete().with_phone(phone).build_object())
            session.add(
                PatientBuilder().complete().with_phone(phone).build_object())
            session.flush()


def test_should_not_raise_exception_if_payload_is_valid():
    """
    Should not raise exception if payload is valid
    """
    payload = PatientBuilder().build()
    validate_payload(payload, Patient.validators)

    payload = PatientBuilder().complete().build()
    validate_payload(payload, Patient.validators)


def test_should_raise_exception_when_validation_payload_fails():
    """
    Should raise a exception if payload validation fails
    """
    payload = {}
    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Patient.validators)

    errors = e_info.value.errors
    assert len(errors) == 2
    assert "name" in errors and errors[
        "name"] == ValidationMessages.REQUIRED_FIELD.format("name")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.REQUIRED_FIELD.format("phone")

    payload = PatientBuilder().with_name(fake.pystr(
        min_chars=1, max_chars=1)).with_cpf("not a cpf").with_phone("not a phone number").with_birthdate(
            "not a date").with_registration(fake.pystr(min_chars=21, max_chars=22)).build()

    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Patient.validators)

    errors = e_info.value.errors
    assert len(errors) == 5
    assert "name" in errors and "name" in errors["name"] and "least" in errors[
        "name"] and "2" in errors["name"]
    assert "registration" in errors and "most 20" in errors["registration"]
    assert "cpf" in errors and errors[
        "cpf"] == ValidationMessages.INVALID_CPF.format("cpf")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.INVALID_PHONE.format("phone")
    assert "birthdate" in errors and errors[
        "birthdate"] == ValidationMessages.INVALID_DATE.format("birthdate")

    payload = PatientBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).build()

    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Patient.validators)

    errors = e_info.value.errors
    assert len(errors) == 1
    assert "name" in errors and "name" in errors["name"] and "most" in errors[
        "name"] and "255" in errors["name"]
