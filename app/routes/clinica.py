from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from app.routes import api
from app.models import db, Clinica

# GET clinicas #
@api.route("/clinicas", methods=["GET"])
def get_clinicas():
    clinicas = Clinica.query.all()
    clinicas_json = [clinica._asdict() for clinica in clinicas]

    return jsonify(clinicas=clinicas_json), 200
# END GET clinicas #


# GET clinica by ID #
@api.route("/clinica/<id>", methods=["GET"])
def get_clinica(id):
    clinica_objeto = Clinica.query.get(id)
    clinica_json = clinica_objeto._asdict()

    return jsonify(clinica=clinica_json), 200
# END GET clinica by ID #



