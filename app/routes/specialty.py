from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Specialty, session, select, delete, update
from ..exceptions import APIException
from ..utils import useless_params
from ..constants import ResponseMessages
from ..validations import validate_payload
from ..middlewares import token_required, only_admin

from ..docs import specialty_specs

PARAMETERS_FOR_POST_SPECIALTY = ["description"]

PARAMETERS_FOR_GET_SPECIALTY = ["description", "limit", "page", "order_by"]

PARAMETERS_FOR_PUT_SPECIALTY = ["description"]

# POST specialty #


@bp_api.route("/specialties", methods=["POST"])
@swag_from(specialty_specs.post_specialty)
@token_required
@only_admin
def create_specialty(_):
    """
    Create a new specialty
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_SPECIALTY)
    validate_payload(body, Specialty.validators)

    specialty = Specialty(**body)
    session.add(specialty)
    session.commit()
    session.refresh(specialty)

    return jsonify(specialty.as_json()), 201


# END POST specialty #


# GET specialties #
@bp_api.route("/specialties", methods=["GET"])
@swag_from(specialty_specs.get_specialties)
@token_required
def get_specialties(_):
    """
    Get specialties
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_SPECIALTY)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    description = params.get("description")

    stmt = select(Specialty).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Specialty.created_at))

    if description is not None:
        stmt = stmt.filter(Specialty.description.like("%" + description + "%"))

    specialties = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(specialties), 200


@bp_api.route("/specialties/<int:specialty_id>", methods=["GET"])
@swag_from(specialty_specs.get_specialty_by_id)
@token_required
@only_admin
def get_specialty_by_id(_, specialty_id):
    """
    Get specialty by id
    """
    specialty = session.get(Specialty, specialty_id)

    if specialty is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Specialty"),
            status_code=404)

    return jsonify(specialty.as_json())


# END GET specialties #

# PUT specialty #


@bp_api.route("/specialties/<int:specialty_id>", methods=["PUT"])
@swag_from(specialty_specs.update_specialty)
@token_required
@only_admin
def update_specialty(_, specialty_id):
    """
    Update specialty with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_SPECIALTY)
    validate_payload(body, Specialty.validators, PARAMETERS_FOR_PUT_SPECIALTY)

    stmt = update(Specialty).where(Specialty.id == specialty_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Specialty no found", status_code=404)

    specialty = session.get(Specialty, specialty_id)

    return jsonify(specialty.as_json()), 200


# END PUT specialty #

# DELETE specialty #


@bp_api.route("/specialties/<int:specialty_id>", methods=["DELETE"])
@swag_from(specialty_specs.delete_specialty)
@token_required
@only_admin
def delete_specialty(_, specialty_id):
    """
    Delete specialty by id
    """
    stmt = delete(Specialty).where(Specialty.id == specialty_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE specialty #
