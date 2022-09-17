from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import bp_api
from ..models import session, select, Clinica
from ..exceptions import APIExceptionHandler
from ..utils import useless_params

# POST clinica #


@bp_api.route("/clinicas", methods=["POST"])
def post_clinica():
    pass


# END POST clinica #

# GET clinicas #


@bp_api.route("/clinicas", methods=["GET"])
@bp_api.route("/clinicas/<int:id>", methods=["GET"])
def get_clinicas(id=None):

    clinica = session.get(Clinica, id)

    return jsonify(status="success", data={"clinica": clinica._asjson()}), 200


# END GET clinicas #

# PUT clinica #


@bp_api.route("/clinicas/<int:id>", methods=["PUT"])
def put_clinica(id):
    pass


# END PUT clinica #

# DELETE clinica #


@bp_api.route("/clinicas", methods=["DELETE"])
def delete_clinica():
    pass


# END DELETE clinica #
