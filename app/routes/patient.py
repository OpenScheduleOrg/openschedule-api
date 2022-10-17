from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Patient, session, select, delete, update
from ..exceptions import APIException, ValidationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload

from ..docs import patient_specs

PARAMETERS_FOR_POST_PATIENT = ["name", "cpf", "phone", "birthdate", "address"]

PARAMETERS_FOR_GET_PATIENT = [
    "name", "cpf", "phone", "limit", "page", "order_by"
]

PARAMETERS_FOR_PUT_PATIENT = ["name", "cpf", "phone", "birthdate"]

# POST patient #


@bp_api.route("/patients", methods=["POST"])
@swag_from(patient_specs.post_patient)
def create_patient():
    """
    Create a new patient
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    if session.query(
            Patient.id).filter(Patient.cpf == body["cpf"]).first() is not None:
        raise ValidationException({"cpf": ValidationMessages.CPF_REGISTERED})
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
def get_patients():
    """
    Get patients
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_PATIENT)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    name = params.get("name")
    cpf = params.get("cpf")
    phone = params.get("phone")

    stmt = select(Patient).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Patient.created_at))

    if name is not None:
        stmt = stmt.filter(Patient.name.like("%" + name + "%"))

    if cpf is not None:
        stmt = stmt.filter(Patient.cpf.like("%" + cpf + "%"))

    if phone is not None:
        stmt = stmt.filter(Patient.phone.like("%" + phone + "%"))

    patients = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(patients), 200


@bp_api.route("/patients/<int:patient_id>", methods=["GET"])
@swag_from(patient_specs.get_patient_by_id)
def get_patient_by_id(patient_id):
    """
    Get patient by id
    """
    patient = session.get(Patient, patient_id)

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient.as_json())


@bp_api.route("/patients/<string:patient_cpf>/cpf", methods=["GET"])
@swag_from(patient_specs.get_patient_by_cpf)
def get_patient_by_cpf(patient_cpf):
    """
    Get patient by cpf
    """
    patient = session.execute(
        select(Patient).filter_by(cpf=patient_cpf)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient.as_json())


@bp_api.route("/patients/<string:patient_phone>/phone", methods=["GET"])
@swag_from(patient_specs.get_patient_by_phone)
def get_patient_by_phone(patient_phone):
    """
    Get patient by phone
    """
    patient = session.execute(
        select(Patient).filter_by(phone=patient_phone)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient.as_json())


# END GET patients #

# PUT patient #


@bp_api.route("/patients/<int:patient_id>", methods=["PUT"])
@swag_from(patient_specs.update_patient)
def update_patient(patient_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    if session.query(
            Patient.id).filter(Patient.cpf == body["cpf"],
                               Patient.id != patient_id).first() is not None:
        raise ValidationException({"cpf": ValidationMessages.CPF_REGISTERED})
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
def delete_patient(patient_id):
    """
    Delete patient by id
    """
    stmt = delete(Patient).where(Patient.id == patient_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE patient #
