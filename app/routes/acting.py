from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Acting, Clinic, Professional, Specialty, session, select, delete, update
from ..exceptions import APIException, ValidationException, AuthorizationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..middlewares import token_required, only_admin

from ..docs import acting_specs

PARAMETERS_FOR_POST_ACTING = ["professional_id", "clinic_id", "specialty_id"]

PARAMETERS_FOR_GET_ACTING = [
    "professional_id", "clinic_id", "specialty_id", "limit", "page", "order_by"
]

PARAMETERS_FOR_PUT_ACTING = ["professional_id", "clinic_id", "specialty_id"]

# POST acting #


@bp_api.route("/actuations", methods=["POST"])
@swag_from(acting_specs.post_acting)
@token_required
@only_admin
def create_acting(_):
    """
    Create a new acting
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_ACTING)

    if session.query(Professional.id).filter(
            Professional.id == body["professional_id"]).first() is None:
        raise ValidationException({
            "professional_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "professional", body["professional_id"])
        })

    if session.query(
            Clinic.id).filter(Clinic.id == body["clinic_id"]).first() is None:
        raise ValidationException({
            "clinic_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "clinic", body["clinic_id"])
        })

    if session.query(Specialty.id).filter(
            Specialty.id == body["specialty_id"]).first() is None:
        raise ValidationException({
            "specialty_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "specialty", body["specialty_id"])
        })

    acting = Acting(**body)
    session.add(acting)
    session.commit()
    session.refresh(acting)

    return jsonify(acting.as_json()), 201


# END POST acting #

# GET actuations #


@bp_api.route("/actuations", methods=["GET"])
@swag_from(acting_specs.get_actuations)
@token_required
def get_actuations(current_user):
    """
    Get actuations
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_ACTING)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    professional_id = params.get("professional_id")
    clinic_id = params.get("clinic_id")
    specialty_id = params.get("specialty_id")

    stmt = select(Acting).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Acting.created_at))

    if not current_user["admin"] and str(
            current_user["id"]) != professional_id:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    if professional_id is not None:
        stmt = stmt.filter(Acting.professional_id == professional_id)
    elif clinic_id is not None:
        stmt = stmt.filter(Acting.clinic_id == clinic_id)
    elif specialty_id is not None:
        stmt = stmt.filter(Acting.specialty_id == specialty_id)

    actuations = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(actuations), 200


@bp_api.route("/actuations/<int:acting_id>", methods=["GET"])
@swag_from(acting_specs.get_acting_by_id)
@token_required
def get_acting_by_id(current_user, acting_id):
    """
    Get acting by id
    """
    acting = session.get(Acting, acting_id)

    if acting is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Acting"),
                           status_code=404)

    if not current_user[
            "admin"] and current_user["id"] != acting.professional_id:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    return jsonify(acting.as_json())


# END GET actuations #

# PUT acting #


@bp_api.route("/actuations/<int:acting_id>", methods=["PUT"])
@swag_from(acting_specs.update_acting)
@token_required
def update_acting(current_user, acting_id):
    """
    Update acting with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_ACTING)

    if not current_user[
            "admin"] and current_user["id"] != body["professional_id"]:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_OPERATION)

    if session.query(Professional.id).filter(
            Professional.id == body["professional_id"]).first() is None:
        raise ValidationException({
            "professional_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "professional", body["professional_id"])
        })

    if session.query(
            Clinic.id).filter(Clinic.id == body["clinic_id"]).first() is None:
        raise ValidationException({
            "clinic_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "clinic", body["clinic_id"])
        })

    if session.query(Specialty.id).filter(
            Specialty.id == body["specialty_id"]).first() is None:
        raise ValidationException({
            "specialty_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "specialty", body["specialty_id"])
        })

    stmt = update(Acting).where(Acting.id == acting_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Acting no found", status_code=404)

    acting = session.get(Acting, acting_id)

    return jsonify(acting.as_json()), 200


# END PUT acting #

# DELETE acting #


@bp_api.route("/actuations/<int:acting_id>", methods=["DELETE"])
@swag_from(acting_specs.delete_acting)
@token_required
@only_admin
def delete_acting(_, acting_id):
    """
    Delete acting by id
    """
    stmt = delete(Acting).where(Acting.id == acting_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE acting #
