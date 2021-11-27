from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import api
from ..models import db, Clinica
from ..exceptions import APIExceptionHandler

# POST clinica #
@api.route("/clinica", methods=["POST"])
def post_clinica():
    pass
# END POST clinica #

# GET clinicas #
@api.route("/clinicas", methods=["GET"])
@api.route("/clinicas/<int:id>", methods=["GET"])
def get_clinicas(id):
    pass
# END GET clinicas #

# PUT clinica #
@api.route("/clinica/<int:id>", methods=["PUT"])
def put_clinica(id):
    pass
# END PUT clinica #

# DELETE clinica #
@api.route("/clinica", methods=["DELETE"])
def delete_clinica():
    pass
# END DELETE clinica #


