from app.routes import api

from datetime import datetime, time, date, timedelta
import calendar
from app.common.utils import gen_response, insertSort, CPFormat
from flask import request
from app.models import Clinica

# GET clinicas #
@api.route("/clinicas", methods=["GET"])
def get_clinicas():
    clinicas = Clinica.query.all()
    clinicas_json = [clinica.to_json() for clinica in clinicas]

    return gen_response(200, clinicas=clinicas_json)
# END GET clinicas #


# GET clinica by ID #
@api.route("/clinica/<id>", methods=["GET"])
def get_clinica(id):
    clinica_objeto = Clinica.query.get(id)
    clinica_json = clinica_objeto.to_json()

    return gen_response(200, clinica=clinica_json)
# END GET clinica by ID #



