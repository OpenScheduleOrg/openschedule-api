from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Clinic, session, select, delete, update, ClinicType
from ..exceptions import APIException, ValidationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload

from ..docs import clinic_specs

PARAMETERS_FOR_POST_CLINIC = [
    "name", "cnpj", "phone", "type", "address", "latitude", "longitude"
]

PARAMETERS_FOR_GET_CLINIC = [
    "name", "cnpj", "phone", "limit", "type", "page", "order_by"
]

PARAMETERS_FOR_PUT_CLINIC = [
    "name", "cnpj", "phone", "address", "type", "latitude", "longitude"
]

# POST clinic #


@bp_api.route("/clinics", methods=["POST"])
@swag_from(clinic_specs.post_clinic)
def create_clinic():
    """
    Create a new clinic
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CLINIC)
    validate_payload(body, Clinic.validators)

    if session.query(
            Clinic.id).filter(Clinic.cnpj == body["cnpj"]).first() is not None:
        raise ValidationException({"cnpj": ValidationMessages.CNPJ_REGISTERED})
    if session.query(Clinic.id).filter(
            Clinic.phone == body["phone"]).first() is not None:
        raise ValidationException(
            {"phone": ValidationMessages.PHONE_REGISTERED})

    clinic = Clinic(**body)
    session.add(clinic)
    session.commit()
    session.refresh(clinic)

    return jsonify(clinic.as_json()), 201


# END POST clinic #


# GET clinics #
@bp_api.route("/clinics", methods=["GET"])
@swag_from(clinic_specs.get_clinics)
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
@swag_from(clinic_specs.get_clinic_by_id)
def get_clinic_by_id(clinic_id):
    """
    Get clinic by id
    """
    clinic = session.get(Clinic, clinic_id)

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic.as_json())


@bp_api.route("/clinics/<string:clinic_cnpj>/cnpj", methods=["GET"])
@swag_from(clinic_specs.get_clinic_by_cnpj)
def get_clinic_by_cnpj(clinic_cnpj):
    """
    Get clinic by cnpj
    """
    clinic = session.execute(
        select(Clinic).filter_by(cnpj=clinic_cnpj)).scalar()

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic.as_json())


@bp_api.route("/clinics/<string:clinic_phone>/phone", methods=["GET"])
@swag_from(clinic_specs.get_clinic_by_phone)
def get_clinic_by_phone(clinic_phone):
    """
    Get clinic by phone
    """
    clinic = session.execute(
        select(Clinic).filter_by(phone=clinic_phone)).scalar()

    if clinic is None:
        raise APIException(ResponseMessages.CLINIC_NO_FOUND, status_code=404)

    return jsonify(clinic.as_json())


# END GET clinics #

# PUT clinic #


@bp_api.route("/clinics/<int:clinic_id>", methods=["PUT"])
@swag_from(clinic_specs.update_clinic)
def update_clinic(clinic_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_PUT_CLINIC)
    validate_payload(body, Clinic.validators)

    if session.query(
            Clinic.id).filter(Clinic.cnpj == body["cnpj"],
                              Clinic.id != clinic_id).first() is not None:
        raise ValidationException({"cnpj": ValidationMessages.CNPJ_REGISTERED})
    if session.query(
            Clinic.id).filter(Clinic.phone == body["phone"],
                              Clinic.id != clinic_id).first() is not None:
        raise ValidationException(
            {"phone": ValidationMessages.PHONE_REGISTERED})

    stmt = update(Clinic).where(Clinic.id == clinic_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Clinic no found", status_code=404)

    clinic = session.get(Clinic, clinic_id)

    return jsonify(clinic.as_json()), 200


# END PUT clinic #

# DELETE clinic #


@bp_api.route("/clinics/<int:clinic_id>", methods=["DELETE"])
@swag_from(clinic_specs.delete_clinic)
def delete_clinic(clinic_id):
    """
    Delete clinic by id
    """
    stmt = delete(Clinic).where(Clinic.id == clinic_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE clinic #
