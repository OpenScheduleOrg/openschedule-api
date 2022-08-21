from flask import request, jsonify
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from . import bp_api
from ..models import Clinic, session, select, delete, update, ClinicType
from ..exceptions import APIException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload, validate_unique

PARAMETERS_FOR_POST_CLINIC = [
    "name", "cnpj", "phone", "type", "address", "latitude", "longitude"
]

PARAMETERS_FOR_GET_CLINIC = [
    "name", "cnpj", "phone", "limit", "type", "page", "order_by"
]

PARAMETERS_FOR_PUT_CLINIC = [
    "name", "cnpj", "phone", "address", "type", "latitude", "longitude"
]

FIELDS_UNIQUE = {
    "cnpj": ValidationMessages.CNPJ_REGISTERED,
    "phone": ValidationMessages.PHONE_REGISTERED
}

# POST clinic #


@bp_api.route("/clinics", methods=["POST"])
def create_clinic():
    """
    Create a new clinic
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CLINIC)
    validate_payload(body, Clinic.validators)

    try:
        clinic = Clinic(**body)
        session.add(clinic)
        session.commit()
        session.refresh(clinic)
    except IntegrityError as e:
        validate_unique(e, FIELDS_UNIQUE)
        raise e

    return jsonify(clinic=clinic.as_json()), 201


# END POST clinic #


# GET clinics #
@bp_api.route("/clinics", methods=["GET"])
def get_clinics():
    """
    Get clinics
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_CLINIC)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    name = params.get("name")
    cnpj = params.get("cnpj")
    phone = params.get("phone")
    clinic_type = params.get("type")

    stmt = select(Clinic).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Clinic.created_at))

    if name is not None:
        stmt = stmt.filter(Clinic.name.like("%" + name + "%"))

    if cnpj is not None:
        stmt = stmt.filter(Clinic.cnpj.like("%" + cnpj + "%"))

    if phone is not None:
        stmt = stmt.filter(Clinic.phone.like("%" + phone + "%"))

    if clinic_type is not None:
        stmt = stmt.filter(Clinic.type == ClinicType(int(clinic_type)))

    clinics = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(clinics), 200


@bp_api.route("/clinics/<int:clinic_id>", methods=["GET"])
def get_clinic_by_id(clinic_id=None):
    """
    Get clinic by id
    """
    clinic = session.get(Clinic, clinic_id)

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic=clinic.as_json())


@bp_api.route("/clinics/<string:clinic_cnpj>/cnpj", methods=["GET"])
def get_clinic_by_cnpj(clinic_cnpj):
    """
    Get clinic by cnpj
    """
    clinic = session.execute(
        select(Clinic).filter_by(cnpj=clinic_cnpj)).scalar()

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic=clinic.as_json())


@bp_api.route("/clinics/<string:clinic_phone>/phone", methods=["GET"])
def get_clinic_by_phone(clinic_phone):
    """
    Get clinic by phone
    """
    clinic = session.execute(
        select(Clinic).filter_by(phone=clinic_phone)).scalar()

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic=clinic.as_json())


# END GET clinics #

# PUT clinic #


@bp_api.route("/clinics/<int:clinic_id>", methods=["PUT"])
def update_clinic(clinic_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CLINIC)
    validate_payload(body, Clinic.validators)

    try:
        stmt = update(Clinic).where(Clinic.id == clinic_id).values(**body)
        rowcount = session.execute(stmt).rowcount
        session.commit()
    except IntegrityError as e:
        validate_unique(e, FIELDS_UNIQUE)
        raise e

    if not rowcount:
        raise APIException("Clinic no found", status_code=404)

    clinic = session.get(Clinic, clinic_id)

    return jsonify(clinic=clinic.as_json()), 200


# END PUT clinic #

# DELETE clinic #


@bp_api.route("/clinics/<int:clinic_id>", methods=["DELETE"])
def delete_clinic(clinic_id):
    """
    Delete clinic
    """
    stmt = delete(Clinic).where(Clinic.id == clinic_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE clinic #
