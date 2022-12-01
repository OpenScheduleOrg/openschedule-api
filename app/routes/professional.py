from flask import request, jsonify
from sqlalchemy import desc
from passlib.hash import pbkdf2_sha256
from flasgger import swag_from

from . import bp_api
from ..models import Professional, Acting, Specialty, Clinic, session, select, delete, update
from ..exceptions import APIException, ValidationException, AuthorizationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload
from ..middlewares import token_required, only_admin

from ..docs import professional_specs

PARAMETERS_FOR_POST_PROFESSIONAL = [
    "name", "phone", "reg_number", "username", "email", "password"
]

PARAMETERS_FOR_GET_PROFESSIONAL = [
    "name", "phone", "reg_number", "username", "email", "limit", "page",
    "order_by"
]

PARAMETERS_FOR_PUT_PROFESSIONAL = [
    "name", "phone", "reg_number", "username", "email", "password"
]

# POST professional #
query_actuations = select(
    Acting.id, Acting.professional_id, Acting.clinic_id,
    Clinic.name.label("clinic_name"), Acting.specialty_id,
    Specialty.description.label("specialty_description")).join(
        Clinic, Acting.clinic_id == Clinic.id).join(
            Specialty, Acting.specialty_id == Specialty.id)


@bp_api.route("/professionals", methods=["POST"])
@swag_from(professional_specs.post_professional)
@token_required
@only_admin
def create_professional(_):
    """
    Create a new professional
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_PROFESSIONAL)
    validate_payload(body, Professional.validators)

    if session.query(Professional.id).filter(
            Professional.username == body["username"]).first() is not None:
        raise ValidationException(
            {"username": ValidationMessages.USERNAME_REGISTERED})
    if session.query(Professional.id).filter(
            Professional.email == body["email"]).first() is not None:
        raise ValidationException(
            {"email": ValidationMessages.EMAIL_REGISTERED})

    body["password"] = pbkdf2_sha256.hash(body["password"])

    professional = Professional(**body)
    session.add(professional)
    session.commit()
    session.refresh(professional)

    return jsonify(professional.as_json()), 201


# END POST professional #


# GET professionals #
@bp_api.route("/professionals", methods=["GET"])
@swag_from(professional_specs.get_professionals)
@token_required
def get_professionals(_):
    """
    Get professionals
    """

    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_PROFESSIONAL)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    name = params.get("name")
    phone = params.get("phone")
    reg_number = params.get("reg_number")
    username = params.get("username")
    email = params.get("email")

    stmt = select(Professional).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Professional.created_at))

    if name is not None:
        stmt = stmt.filter(Professional.name.like("%" + name + "%"))

    if phone is not None:
        stmt = stmt.filter(Professional.phone.like("%" + phone + "%"))

    if reg_number is not None:
        stmt = stmt.filter(Professional.reg_number.like("%" + reg_number +
                                                        "%"))

    if username is not None:
        stmt = stmt.filter(Professional.username.like("%" + username + "%"))

    if email is not None:
        stmt = stmt.filter(Professional.email.like("%" + email + "%"))

    professionals = {}

    for p in session.execute(stmt).scalars():
        professionals[p.id] = {**p.as_json(), "actuations": []}

    for act in session.execute(
            query_actuations.filter(
                Acting.professional_id.in_(professionals.keys())).order_by(
                    Acting.professional_id)).all():
        professionals[act.professional_id]["actuations"].append(act._asdict())

    return jsonify(list(professionals.values())), 200


@bp_api.route("/professionals/<int:professional_id>", methods=["GET"])
@swag_from(professional_specs.get_professional_by_id)
@token_required
def get_professional_by_id(current_user, professional_id):
    """
    Get professional by id
    """
    if not current_user["admin"] and current_user["id"] != professional_id:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    professional = session.get(Professional, professional_id)

    if professional is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Professional"),
            status_code=404)

    professional = professional.as_json()
    professional["actuations"] = [
        a._asdict() for a in session.execute(
            query_actuations.where(
                Acting.professional_id == professional_id)).all()
    ]

    return jsonify(professional), 200


@bp_api.route("/professionals/<string:professional_username>/username",
              methods=["GET"])
@swag_from(professional_specs.get_professional_by_username)
@token_required
@only_admin
def get_professional_by_username(_, professional_username):
    """
    Get professional by username
    """
    professional = session.execute(
        select(Professional).filter_by(
            username=professional_username)).scalar()

    if professional is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Professional"),
            status_code=404)

    professional = professional.as_json()
    professional["actuations"] = [
        a._asdict() for a in session.execute(
            query_actuations.where(
                Acting.professional_id == professional["id"])).all()
    ]

    return jsonify(professional), 200


@bp_api.route("/professionals/<string:professional_email>/email",
              methods=["GET"])
@swag_from(professional_specs.get_professional_by_email)
@token_required
@only_admin
def get_professional_by_email(_, professional_email):
    """
    Get professional by email
    """
    professional = session.execute(
        select(Professional).filter_by(email=professional_email)).scalar()

    if professional is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Professional"),
            status_code=404)

    professional = professional.as_json()
    professional["actuations"] = [
        a._asdict() for a in session.execute(
            query_actuations.where(
                Acting.professional_id == professional["id"])).all()
    ]

    return jsonify(professional), 200


@bp_api.route("/professionals/<string:professional_phone>/phone",
              methods=["GET"])
@swag_from(professional_specs.get_professional_by_phone)
@token_required
@only_admin
def get_professional_by_phone(_, professional_phone):
    """
    Get professional by phone
    """
    professional = session.execute(
        select(Professional).filter_by(phone=professional_phone)).scalar()

    if professional is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Professional"),
            status_code=404)

    professional = professional.as_json()
    professional["actuations"] = [
        a._asdict() for a in session.execute(
            query_actuations.where(
                Acting.professional_id == professional["id"])).all()
    ]

    return jsonify(professional), 200


# END GET professionals #

# PUT professional #


@bp_api.route("/professionals/<int:professional_id>", methods=["PUT"])
@swag_from(professional_specs.update_professional)
@token_required
def update_professional(current_user, professional_id):
    """
    Update professional with id
    """
    body: dict[str, str] = request.get_json()

    if not current_user["admin"] and current_user["id"] != professional_id:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_OPERATION)

    useless_params(body.keys(), PARAMETERS_FOR_PUT_PROFESSIONAL)
    validate_payload(body, Professional.validators_update,
                     PARAMETERS_FOR_PUT_PROFESSIONAL)

    if session.query(Professional.id).filter(
            Professional.username == body["username"],
            Professional.id != professional_id).first() is not None:
        raise ValidationException(
            {"username": ValidationMessages.USERNAME_REGISTERED})
    if session.query(Professional.id).filter(
            Professional.email == body["email"],
            Professional.id != professional_id).first() is not None:
        raise ValidationException(
            {"email": ValidationMessages.EMAIL_REGISTERED})

    if "password" in body:
        body["password"] = pbkdf2_sha256.hash(body["password"])

    stmt = update(Professional).where(
        Professional.id == professional_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Professional no found", status_code=404)

    professional = session.get(Professional, professional_id)

    return jsonify(professional.as_json()), 200


# END PUT professional #

# DELETE professional #


@bp_api.route("/professionals/<int:professional_id>", methods=["DELETE"])
@swag_from(professional_specs.delete_professional)
@token_required
@only_admin
def delete_professional(_, professional_id):
    """
    Delete professional by id
    """
    stmt = delete(Professional).where(Professional.id == professional_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE professional #
