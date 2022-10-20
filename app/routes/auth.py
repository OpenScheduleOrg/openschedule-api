import datetime

import jwt
from flask import request, jsonify, current_app
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_
from flasgger import swag_from

from . import bp_auth
from ..models import session, select, User
from ..helpers.auth import get_header_token, decode_token

from ..docs import auth_specs


@bp_auth.route("/signin", methods=["POST"])
@swag_from(auth_specs.signin)
def signin():
    """
    Performs login
    """
    remember_me = request.args.get("remember_me")
    body = request.get_json() if request.data else None
    header_auth = request.authorization

    username = (header_auth and header_auth.username) or (body
                                                          and body["username"])
    password = (header_auth and header_auth.password) or (body
                                                          and body["password"])

    if not username or not password:
        return jsonify({"message": "credentials required"}), 401

    user = session.execute(
        select(User).where(
            or_(User.username == username, User.email == username))).scalar()

    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = jwt.encode(
            {
                'user_id':
                user.id,
                'name':
                user.name,
                'admin':
                True,
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(
                    seconds=current_app.config["ACCESS_TOKEN_EXPIRE"])
            }, current_app.config["JWT_SECRET_KEY"], "HS256")
        if remember_me and remember_me != "false":
            session_token = jwt.encode(
                {
                    'user_id':
                    user.id,
                    'name':
                    user.name,
                    'admin':
                    True,
                    'exp':
                    datetime.datetime.utcnow() + datetime.timedelta(
                        seconds=current_app.config["SESSION_TOKEN_EXPIRE"])
                }, current_app.config["JWT_SECRET_KEY"], "HS512")

            return jsonify({
                "access_token": access_token,
                "session_token": session_token
            }), 200

        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "username or password wrong"}), 401


@bp_auth.route("/refresh-token", methods=["GET"])
@swag_from(auth_specs.refresh_token)
def refresh_token():
    """
    Refresh token that are close to expiring
    """
    auth_token = get_header_token(request.headers.get("Authorization"))

    payload = decode_token(auth_token, current_app.config["JWT_SECRET_KEY"],
                           "HS256")

    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=current_app.config["ACCESS_TOKEN_EXPIRE"])

    access_token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"],
                              "HS256")
    return jsonify({"access_token": access_token}), 200


@bp_auth.route("/restore-session", methods=["GET"])
@swag_from(auth_specs.restore_session)
def restore_session():
    """
    Restore session with session token
    """
    auth_token = get_header_token(request.headers.get("Authorization"))

    payload = decode_token(auth_token, current_app.config["JWT_SECRET_KEY"],
                           "HS512")

    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=current_app.config["ACCESS_TOKEN_EXPIRE"])

    access_token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"],
                              "HS256")
    return jsonify({"access_token": access_token}), 200
