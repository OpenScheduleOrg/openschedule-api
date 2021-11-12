from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from app.routes import api
from app.models import db, Horario


@api.route("/horarios", methods=["GET"])
def get_horarios():

    horarios = Horario.query.all()

    horarios_json = [h._asjson() for h in horarios]

    return jsonify(status="success", data={"horarios": horarios_json}), 200

@api.route("/horario", methods=["GET"])
def get_horario():

    return jsonify({"status": "fail", "message": "Nenhum horario encontrado"}), 404
