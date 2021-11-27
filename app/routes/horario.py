from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import bp_api
from ..models import Horario
from ..exceptions import APIExceptionHandler

# POST horario #
@bp_api.route("/horario", methods=["POST"])
def post_horario():
    pass
# END POST horario #

# GET horarios #
@bp_api.route("/horarios", methods=["GET"])
@bp_api.route("/horarios/<int:id>", methods=["GET"])
def get_horarios(id):
    pass
# END GET horarios #

# PUT horario #
@bp_api.route("/horario/<int:id>", methods=["PUT"])
def put_horario(id):
    pass
# END PUT horario #

# DELETE horario #
@bp_api.route("/horario", methods=["DELETE"])
def delete_horario():
    pass
# END DELETE horario #


