from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import bp_api
from ..models import Cliente
from ..exceptions import APIExceptionHandler

# POST cliente #
@bp_api.route("/cliente", methods=["POST"])
def post_cliente():
    pass
# END POST cliente #

# GET clientes #
@bp_api.route("/clientes", methods=["GET"])
@bp_api.route("/clientes/<int:id>", methods=["GET"])
def get_clientes(id):
    pass
# END GET clientes #

# PUT cliente #
@bp_api.route("/cliente/<int:id>", methods=["PUT"])
def put_cliente(id):
    pass
# END PUT cliente #

# DELETE cliente #
@bp_api.route("/cliente", methods=["DELETE"])
def delete_cliente():
    pass
# END DELETE cliente #


