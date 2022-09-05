import os

from flask import request, jsonify, abort
import jwt

from . import bp_auth
from ..models import select
from ..exceptions import APIExceptionHandler
from ..auth import getToken, validateToken, REMEMBER_EXPIRE

user = {
    "id": 1,
    "nome": "Marcos",
    "sobrenome": "Pacheco",
    "email": "marcos@consuchat.com",
    "username": "marcos",
    "password": "pass",
    "clinica_id": 1
}


@bp_auth.route("/loged", methods=["GET"])
def loged():
    token = request.cookies.get("jwt-token")

    if (token):
        payload = validateToken(token)
        try:
            if (payload["password"] == user["password"]
                    and payload["username"] == user["username"]):
                return jsonify(status="success", data={"funcionario":
                                                       user}), 200
        except Exception:
            pass

    return jsonify(status="fail", message="token not exists", data=None), 401


@bp_auth.route("/signin", methods=["POST"])
def signin():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    if (user["username"] == username and user["password"] == password):

        expire = REMEMBER_EXPIRE if body.get("rememberMe") else None

        token = getToken(user["id"], user["username"], user["password"],
                         expire)

        res_json = jsonify(status="success", data={"funcionario": user})
        res_json.set_cookie("jwt-token", token, expire, httponly=True)

        return res_json, 200

    return jsonify(status="fail",
                   message="username ou senha incorreto.",
                   data=None), 401


@bp_auth.route("/logout", methods=["DELETE"])
def logout():

    res_json = jsonify(status="success", data=None)
    res_json.delete_cookie("jwt-token")

    return res_json, 200
