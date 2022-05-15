from flask import request, jsonify, current_app

from . import bp_auth
from ..models import session, select
from ..exceptions import APIExceptionHandler
from ..auth import cria_token, verifica_token


@bp_auth.route("/signin/<string:auth_type>", methods=["GET", "POST"])
def signin(auth_type="header"):
    """
    Everyone knows whats is a login
    """
    id_token = None
    password = None
    username = None
    usuario = None

    if request.headers.get("Authorization", None):
        try:
            pass
        except Exception:
            invalid_credentials = True

    body = request.get_json()


@bp_auth.route("/logout", methods=["DELETE"])
def logout():
    """
    This is the opposite of login
    """

    res_json = jsonify(status="success", data=None)
    res_json.delete_cookie("jwt-token")

    return res_json, 200
