from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import api
from ..models import Cliente
from ..exceptions import APIExceptionHandler

# POST cliente #
@api.route("/cliente", methods=["POST"])
def post_cliente():
    pass
# END POST cliente #

# GET clientes #
@api.route("/clientes", methods=["GET"])
@api.route("/clientes/<int:id>", methods=["GET"])
def get_clientes(id):
    pass
# END GET clientes #

# PUT cliente #
@api.route("/cliente/<int:id>", methods=["PUT"])
def put_cliente(id):
    pass
# END PUT cliente #

# DELETE cliente #
@api.route("/cliente", methods=["DELETE"])
def delete_cliente():
    pass
# END DELETE cliente #


