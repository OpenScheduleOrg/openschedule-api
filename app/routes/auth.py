import os

from flask import request, jsonify, current_app
import jwt

from . import api
from ..models import select
from ..common.exc import APIExceptionHandler


user = {
    "id": 1,
    "nome": "Marcos",
    "sobrenome": "Vim",
    "email": "g@g.com",
    "username": "marcos",
    "password":"hash",
    "clinica_id": 1
}

@api.route("/loged", methods=["GET"])
def loged():
    encoded_jwt = request.cookies.get("jwt-token")

    if(encoded_jwt):
        try:
            payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
            if(payload["password"] == user["password"] and payload["username"] == user["username"]):
                return jsonify(status="success", data={"funcionario": user}), 200
        except:
            pass

    return jsonify(status="fail", message="without token", data=None), 401



@api.route("/signin", methods=["POST"])
def signin():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    if (user["username"] == username and user["password"] == password):
        res_json = jsonify(status="success", data={ "funcionario":user })
        encoded_jwt = jwt.encode({"id": user["id"], "username": user["username"], "password": user["password"] }, SECRET_KEY, algorithm="HS256")
        res_json.set_cookie("jwt-token", encoded_jwt, 172800, httponly=True)

        return res_json, 200

    return jsonify(status="fail", message="username or password incorrect", data=None), 401

@api.route("/logout", methods=["DELETE"])
def logout():

    res_json = jsonify(status="success", data=None)
    res_json.delete_cookie("jwt-token")

    return res_json, 200

