from flask import request, jsonify
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from . import bp_api
from ..models import Patient, session, select, delete, update
from ..exceptions import APIException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload, validate_unique

PARAMETERS_FOR_POST_PATIENT = ["name", "cpf", "phone", "birthdate", "address"]

PARAMETERS_FOR_GET_PATIENT = [
    "name", "cpf", "phone", "limit", "page", "order_by"
]

PARAMETERS_FOR_PUT_PATIENT = ["name", "cpf", "phone", "birthdate"]

FIELDS_UNIQUE = {
    "cpf": ValidationMessages.CPF_REGISTERED,
    "phone": ValidationMessages.PHONE_REGISTERED
}

# POST patient #


@bp_api.route("/patients", methods=["POST"])
def create_patient():
    """
    Create a new patient
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    try:
        patient = Patient(**body)
        session.add(patient)
        session.commit()
        session.refresh(patient)
    except IntegrityError as e:
        validate_unique(e, FIELDS_UNIQUE)
        raise e

    return jsonify(patient=patient.as_json()), 201


# END POST patient #


# GET patients #
@bp_api.route("/patients", methods=["GET"])
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
def get_patient_by_id(patient_id=None):
    """
    Get patient by id
    """
    patient = session.get(Patient, patient_id)

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient=patient.as_json())


@bp_api.route("/patients/<string:patient_cpf>/cpf", methods=["GET"])
def get_patient_by_cpf(patient_cpf):
    """
    Get patient by cpf
    """
    patient = session.execute(
        select(Patient).filter_by(cpf=patient_cpf)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient=patient.as_json())


@bp_api.route("/patients/<string:patient_phone>/phone", methods=["GET"])
def get_patient_by_phone(patient_phone):
    """
    Get patient by phone
    """
    patient = session.execute(
        select(Patient).filter_by(phone=patient_phone)).scalar()

    if patient is None:
        raise APIException(ResponseMessages.PATIENT_NO_FOUND, status_code=404)

    return jsonify(patient=patient.as_json())


# END GET patients #

# PUT patient #


@bp_api.route("/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PATIENT)
    validate_payload(body, Patient.validators)

    try:
        stmt = update(Patient).where(Patient.id == patient_id).values(**body)
        rowcount = session.execute(stmt).rowcount
        session.commit()
    except IntegrityError as e:
        validate_unique(e, FIELDS_UNIQUE)
        raise e

    if not rowcount:
        raise APIException("Patient no found", status_code=404)

    patient = session.get(Patient, patient_id)

    return jsonify(patient=patient.as_json()), 200


# END PUT patient #

# DELETE patient #


@bp_api.route("/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """
    Delete patient
    """
    stmt = delete(Patient).where(Patient.id == patient_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE patient #
