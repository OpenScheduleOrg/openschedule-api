import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError

from app.models import Patient, session
from app.exceptions import ValidationException
from app.validations import validate_payload
from app.constants import ValidationMessages

fake = Faker(["pt_BR"])


def test_should_not_raise_exception_when_patient_have_valid_parameters(app):
    """
    Should not raise a exception when the patient parameters are valid
    """
    with app.app_context():
        patient = Patient(name=fake.name(),
                          cpf=fake.ssn(),
                          phone=fake.msisdn()[-10:],
                          address=fake.address(),
                          birthdate=fake.date_between())
        session.add(patient)
        session.flush()


def test_should_raise_exception_when_patient_name_is_none(app):
    """
    Should raise a exception when name is none
    """
    with pytest.raises(IntegrityError, match=r".*NOT NULL.*patients.name"):
        with app.app_context():
            patient = Patient(name=None,
                              cpf=fake.ssn(),
                              phone=fake.msisdn()[-10:],
                              address=fake.address(),
                              birthdate=fake.date_between())
            session.add(patient)
            session.flush()


def test_should_raise_exception_when_patient_cpf_is_none(app):
    """
    Should raise a exception when cpf is none
    """
    with pytest.raises(IntegrityError, match=r".*NOT NULL.*patients.cpf"):
        with app.app_context():
            patient = Patient(name=fake.name(),
                              cpf=None,
                              phone=fake.msisdn()[-10:],
                              address=fake.address(),
                              birthdate=fake.date_between())
            session.add(patient)
            session.flush()


def test_should_raise_exception_when_patient_phone_is_none(app):
    """
    Should raise a exception when phone is none
    """
    with pytest.raises(IntegrityError, match=r".*NOT NULL.*patients.phone"):
        with app.app_context():
            patient = Patient(name=fake.name(),
                              cpf=fake.cpf(),
                              phone=None,
                              address=fake.address(),
                              birthdate=fake.date_between())
            session.add(patient)
            session.flush()


def test_should_raise_exception_when_patient_cpf_already_in_use(app):
    """
    Should raise a exception when cpf is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*patients.cpf"):
        with app.app_context():
            cpf = fake.cpf()
            patients = [None, None]
            patients[0] = Patient(name=fake.name(),
                                  cpf=cpf,
                                  phone=fake.msisdn()[-10:],
                                  address=fake.address(),
                                  birthdate=fake.date_between())
            patients[1] = Patient(name=fake.name(),
                                  cpf=cpf,
                                  phone=fake.msisdn()[-10:],
                                  address=fake.address(),
                                  birthdate=fake.date_between())
            session.add_all(patients)
            session.flush()


def test_should_raise_exception_when_patient_phone_already_in_use(app):
    """
    Should raise a exception when phone is already registered
    """
    with pytest.raises(IntegrityError, match=r".*UNIQUE.*patients.phone"):
        with app.app_context():
            phone = fake.msisdn()[-10:]
            patients = [None, None]
            patients[0] = Patient(name=fake.name(),
                                  cpf=fake.cpf(),
                                  phone=phone,
                                  address=fake.address(),
                                  birthdate=fake.date_between())
            patients[1] = Patient(name=fake.name(),
                                  cpf=fake.cpf(),
                                  phone=phone,
                                  address=fake.address(),
                                  birthdate=fake.date_between())
            session.add_all(patients)
            session.flush()


def test_should_not_raise_exception_if_payload_is_valid():
    """
    Should not raise exception if payload is valid
    """
    payload = {
        "name": fake.name(),
        "cpf": fake.cpf(),
        "phone": fake.msisdn()[-10:],
    }
    validate_payload(payload, Patient.validators)

    payload["address"] = fake.address()
    payload["birthdate"] = fake.date_between()
    validate_payload(payload, Patient.validators)


def test_should_raise_exception_when_validation_payload_fails():
    """
    Should raise a exception if payload validation fails
    """
    payload = {}
    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Patient.validators)

    errors = e_info.value.errors
    assert len(errors) == 3
    assert "name" in errors and errors[
        "name"] == ValidationMessages.REQUIRED_FIELD.format("name")
    assert "cpf" in errors and errors[
        "cpf"] == ValidationMessages.REQUIRED_FIELD.format("cpf")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.REQUIRED_FIELD.format("phone")

    payload["name"] = fake.name()
    payload["cpf"] = "not a cpf"
    payload["phone"] = "not a phone number"
    payload["birthdate"] = "not a date"
    with pytest.raises(ValidationException) as e_info:
        validate_payload(payload, Patient.validators)

    errors = e_info.value.errors
    assert len(errors) == 3
    assert "cpf" in errors and errors[
        "cpf"] == ValidationMessages.INVALID_CPF.format("cpf")
    assert "phone" in errors and errors[
        "phone"] == ValidationMessages.INVALID_PHONE.format("phone")
    assert "birthdate" in errors and errors[
        "birthdate"] == ValidationMessages.INVALID_DATE.format("birthdate")
