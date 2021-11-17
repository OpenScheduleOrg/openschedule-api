from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import api
from ..models import db, Horario
from ..common.exc import APIExceptionHandler

# POST horario #
@api.route("/horario", methods=["POST"])
def post_horario():
    pass
# END POST horario #

# GET horarios #
@api.route("/horarios", methods=["GET"])
@api.route("/horarios/<int:id>", methods=["GET"])
def get_horarios(id):
    pass
# END GET horarios #

# PUT horario #
@api.route("/horario/<int:id>", methods=["PUT"])
def put_horario(id):
    pass
# END PUT horario #

# DELETE horario #
@api.route("/horario", methods=["DELETE"])
def delete_horario():
    pass
# END DELETE horario #


