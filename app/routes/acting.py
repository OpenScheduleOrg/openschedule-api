from flask import request, jsonify
from sqlalchemy import desc, inspect
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
clinic_cols = (Clinic.name.label("clinic_name"), )
professional_cols = (Professional.name.label("professional_name"), )
specialty_cols = (Specialty.description.label("specialty_description"), )

base_query = select(*inspect(Acting).attrs, *clinic_cols,
                    *professional_cols, *specialty_cols).join(
                        Clinic, Acting.clinic_id == Clinic.id).join(
                            Professional,
                            Acting.professional_id == Professional.id).join(
                                Specialty, Acting.specialty_id == Specialty.id)


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

    stmt = base_query.filter(Acting.id == acting.id)
    acting = session.execute(stmt).first()
    return jsonify(acting._asdict()), 201


# END POST acting #

# GET actuations #


@bp_api.route("/actuations", methods=["GET"])
@swag_from(acting_specs.get_actuations)
@token_required
def get_actuations(_):
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

    stmt = base_query.limit(limit).offset(
        (page - 1) * limit).order_by(desc(Acting.created_at))

    if professional_id is not None:
        stmt = stmt.filter(Acting.professional_id == professional_id)
    elif clinic_id is not None:
        stmt = stmt.filter(Acting.clinic_id == clinic_id)
    elif specialty_id is not None:
        stmt = stmt.filter(Acting.specialty_id == specialty_id)

    actuations = [p._asdict() for p in session.execute(stmt).all()]
    return jsonify(actuations), 200


@bp_api.route("/actuations/<int:acting_id>", methods=["GET"])
@swag_from(acting_specs.get_acting_by_id)
@token_required
def get_acting_by_id(_, acting_id):
    """
    Get acting by id
    """
    stmt = base_query.filter(Acting.id == acting_id)
    acting = session.execute(stmt).first()

    if acting is None:
        raise APIException(ResponseMessages.ENTITY_NOT_FOUND.format("Acting"),
                           status_code=404)

    return jsonify(acting._asdict())


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

    stmt = base_query.filter(Acting.id == acting_id)
    acting = session.execute(stmt).first()
    return jsonify(acting._asdict()), 200


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
