from flask import request, jsonify
from sqlalchemy import desc
from passlib.hash import pbkdf2_sha256
from flasgger import swag_from

from . import bp_api
from ..models import User, session, select, delete, update
from ..exceptions import APIException, ValidationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload

from ..docs import user_specs

PARAMETERS_FOR_POST_USER = ["name", "username", "email", "password"]

PARAMETERS_FOR_GET_USER = ["name", "limit", "page", "order_by"]

PARAMETERS_FOR_PUT_USER = ["name", "username", "email", "password"]

# POST user #


@bp_api.route("/users", methods=["POST"])
@swag_from(user_specs.post_user)
def create_user():
    """
    Create a new user
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_USER)
    validate_payload(body, User.validators)

    if session.query(User.id).filter(
            User.username == body["username"]).first() is not None:
        raise ValidationException(
            {"username": ValidationMessages.USERNAME_REGISTERED})
    if session.query(
            User.id).filter(User.email == body["email"]).first() is not None:
        raise ValidationException(
            {"email": ValidationMessages.EMAIL_REGISTERED})

    body["password"] = pbkdf2_sha256.hash(body["password"])

    user = User(**body)
    session.add(user)
    session.commit()
    session.refresh(user)

    return jsonify(user.as_json()), 201


# END POST user #


# GET users #
@bp_api.route("/users", methods=["GET"])
@swag_from(user_specs.get_users)
def get_users():
    """
    Get users
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_USER)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    name = params.get("name")

    stmt = select(User).limit(limit).offset(
        (page - 1) * limit).order_by(desc(User.created_at))

    if name is not None:
        stmt = stmt.filter(User.name.like("%" + name + "%"))

    users = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(users), 200


@bp_api.route("/users/<int:user_id>", methods=["GET"])
@swag_from(user_specs.get_user_by_id)
def get_user_by_id(user_id):
    """
    Get user by id
    """
    user = session.get(User, user_id)

    if user is None:
        raise APIException(ResponseMessages.USER_NO_FOUND, status_code=404)

    return jsonify(user.as_json())


@bp_api.route("/users/<string:user_username>/username", methods=["GET"])
@swag_from(user_specs.get_user_by_username)
def get_user_by_username(user_username):
    """
    Get user by username
    """
    user = session.execute(
        select(User).filter_by(username=user_username)).scalar()

    if user is None:
        raise APIException(ResponseMessages.USER_NO_FOUND, status_code=404)

    return jsonify(user.as_json())


@bp_api.route("/users/<string:user_email>/email", methods=["GET"])
@swag_from(user_specs.get_user_by_email)
def get_user_by_email(user_email):
    """
    Get user by email
    """
    user = session.execute(select(User).filter_by(email=user_email)).scalar()

    if user is None:
        raise APIException(ResponseMessages.USER_NO_FOUND, status_code=404)

    return jsonify(user.as_json())


# END GET users #

# PUT user #


@bp_api.route("/users/<int:user_id>", methods=["PUT"])
@swag_from(user_specs.update_user)
def update_user(user_id):
    """
    Update patiend with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_USER)
    validate_payload(body, User.validators)

    if session.query(User.id).filter(User.username == body["username"],
                                     User.id != user_id).first() is not None:
        raise ValidationException(
            {"username": ValidationMessages.USERNAME_REGISTERED})
    if session.query(User.id).filter(User.email == body["email"],
                                     User.id != user_id).first() is not None:
        raise ValidationException(
            {"email": ValidationMessages.EMAIL_REGISTERED})

    body["password"] = pbkdf2_sha256.hash(body["password"])

    stmt = update(User).where(User.id == user_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("User no found", status_code=404)

    user = session.get(User, user_id)

    return jsonify(user.as_json()), 200


# END PUT user #

# DELETE user #


@bp_api.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from(user_specs.delete_user)
def delete_user(user_id):
    """
    Delete user by id
    """
    stmt = delete(User).where(User.id == user_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE user #
