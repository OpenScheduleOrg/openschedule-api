from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Patient, session, select, delete, update
from ..exceptions import APIException, ValidationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload
from ..middlewares import token_required

from ..docs import patient_specs

PARAMETERS_FOR_POST_PATIENT = ["name", "cpf", "phone", "birthdate", "address", "registration"]

PARAMETERS_FOR_GET_PATIENT = [
    "name", "cpf", "phone", "limit", "page", "order_by", "registration"
]

PARAMETERS_FOR_PUT_PATIENT = ["name", "cpf", "phone", "birthdate", "registration"]

# POST patient #


@bp_api.route("/patients", methods=["POST"])
@swag_from(patient_specs.post_patient)
@token_required
def create_patient(_):
    """
    Create a new patient
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    if "cpf" in body and session.query(
            Patient.id).filter(Patient.cpf == body["cpf"]).first() is not None:
        raise ValidationException({"cpf": ValidationMessages.CPF_REGISTERED})
    if "registration" in body and session.query(
            Patient.id).filter(Patient.registration == body["registration"]).first() is not None:
        raise ValidationException({"registration": ValidationMessages.REGISTRATION_REGISTERED})
    if session.query(Patient.id).filter(
            Patient.phone == body["phone"]).first() is not None:
        raise ValidationException(
            {"phone": ValidationMessages.PHONE_REGISTERED})

    patient = Patient(**body)
    session.add(patient)
    session.commit()
    session.refresh(patient)

    return jsonify(patient.as_json()), 201


# END POST patient #


# GET patients #
@bp_api.route("/patients", methods=["GET"])
@swag_from(patient_specs.get_patients)
@token_required
def get_patients(_):
    """
    Get patients
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_PATIENT)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    name = params.get("name")
    cpf = params.get("cpf")
    registration = params.get("registration")
    phone = params.get("phone")

    stmt = select(Patient).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Patient.created_at))

    if name is not None:
        stmt = stmt.filter(Patient.name.like("%" + name + "%"))

    if cpf is not None:
        stmt = stmt.filter(Patient.cpf.like("%" + cpf + "%"))

    if registration is not None:
        stmt = stmt.filter(Patient.registration.like("%" + registration + "%"))

    if phone is not None:
        stmt = stmt.filter(Patient.phone.like("%" + phone + "%"))

    patients = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(patients), 200


@bp_api.route("/patients/<int:patient_id>", methods=["GET"])
@swag_from(patient_specs.get_patient_by_id)
@token_required
def get_patient_by_id(_, patient_id):
    """
    Get patient by id
    """
    patient = session.get(Patient, patient_id)

    if patient is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Patient"),
                           status_code=404)

    return jsonify(patient.as_json())


@bp_api.route("/patients/<string:patient_cpf>/cpf", methods=["GET"])
@swag_from(patient_specs.get_patient_by_cpf)
@token_required
def get_patient_by_cpf(_, patient_cpf):
    """
    Get patient by cpf
    """
    patient = session.execute(
        select(Patient).filter_by(cpf=patient_cpf)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Patient"),
                           status_code=404)

    return jsonify(patient.as_json())


@bp_api.route("/patients/<string:patient_registration>/registration", methods=["GET"])
@swag_from(patient_specs.get_patient_by_registration)
@token_required
def get_patient_by_registration(_, patient_registration):
    """
    Get patient by registration
    """
    patient = session.execute(
        select(Patient).filter_by(registration=patient_registration)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Patient"),
                           status_code=404)

    return jsonify(patient.as_json())


@bp_api.route("/patients/<string:patient_phone>/phone", methods=["GET"])
@swag_from(patient_specs.get_patient_by_phone)
@token_required
def get_patient_by_phone(_, patient_phone):
    """
    Get patient by phone
    """
    patient = session.execute(
        select(Patient).filter_by(phone=patient_phone)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Patient"),
                           status_code=404)

    return jsonify(patient.as_json())


# END GET patients #

# PUT patient #


@bp_api.route("/patients/<int:patient_id>", methods=["PUT"])
@swag_from(patient_specs.update_patient)
@token_required
def update_patient(_, patient_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    if "cpf" in body and session.query(
            Patient.id).filter(Patient.cpf == body["cpf"],
                               Patient.id != patient_id).first() is not None:
        raise ValidationException({"cpf": ValidationMessages.CPF_REGISTERED})
    if "registration" in body and session.query(
            Patient.id).filter(Patient.registration == body["registration"]).first() is not None:
        raise ValidationException({"registration": ValidationMessages.REGISTRATION_REGISTERED})
    if session.query(
            Patient.id).filter(Patient.phone == body["phone"],
                               Patient.id != patient_id).first() is not None:
        raise ValidationException(
            {"phone": ValidationMessages.PHONE_REGISTERED})

    stmt = update(Patient).where(Patient.id == patient_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Patient no found", status_code=404)

    patient = session.get(Patient, patient_id)

    return jsonify(patient.as_json()), 200


# END PUT patient #

# DELETE patient #


@bp_api.route("/patients/<int:patient_id>", methods=["DELETE"])
@swag_from(patient_specs.delete_patient)
@token_required
def delete_patient(_, patient_id):
    """
    Delete patient by id
    """
    stmt = delete(Patient).where(Patient.id == patient_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE patient #
