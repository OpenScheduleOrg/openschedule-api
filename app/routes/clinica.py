from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import bp_api
from ..models import db, Clinica
from ..exceptions import APIExceptionHandler

# POST clinica #
@bp_api.route("/clinica", methods=["POST"])
def post_clinica():
    pass
# END POST clinica #

# GET clinicas #
@bp_api.route("/clinicas", methods=["GET"])
@bp_api.route("/clinicas/<int:id>", methods=["GET"])
def get_clinicas(id):
    pass
# END GET clinicas #

# PUT clinica #
@bp_api.route("/clinica/<int:id>", methods=["PUT"])
def put_clinica(id):
    pass
# END PUT clinica #

# DELETE clinica #
@bp_api.route("/clinica", methods=["DELETE"])
def delete_clinica():
    pass
# END DELETE clinica #


