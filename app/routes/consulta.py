from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from . import api
from ..models import db, Consulta, Cliente, Clinica, Horario
from ..common.exc import APIExceptionHandler

# POST cosulta #
@api.route("/consulta", methods=["POST"])
def post_consulta():
    body = request.get_json()
    detail_error = {}

    if "id_clinica" not in body:
        detail_error["id_clinica"] = "required"
    if "id_cliente" not in body:
        detail_error["id_cliente"] = "required"
    if "marcada" not in body:
        detail_error["marcada"] = "required"

    if len(detail_error):
        raise APIExceptionHandler("Required parameter is missing", detail=detail_error)
    try:
        cliente = Cliente.query.get(body["id_cliente"])

        if cliente is None:
            raise APIExceptionHandler("id_cliente is not a id of a cliente", detail={"id_cliente": "invalid"})

        consulta = Consulta(**body)
        db.session.add(consulta)
        db.session.commit()

        db.session.refresh(consulta)

        return jsonify(status="success", data={"consulta": consulta._asjson()}), 201

    except APIExceptionHandler as e:
        raise e
    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

# END POST cosulta #


# GET consultas #
@api.route("/consultas", methods=["GET"])
def get_consultas():
    try:
        consultas = Consulta.query.filter_by().all()
        consultas_json = [consulta._asjson() for consulta in consultas]

        return jsonify(status="success", data={"consultas":consultas_json}), 200

    except SQLAlchemyError as e:
        return jsonify(status="error", message=str(e), path=request.full_path, data=e.__dict__), 500

# END GET consultas #


# GET consulta by ID#
@api.route("/consulta/<int:id>", methods=["GET"])
def get_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        consulta_json = consulta._asdict()

    return jsonify(consulta=consulta_json), 200
# END GET consulta by ID#

# DELETE consulta by ID#
@api.route("/consulta/<id>", methods=["DELETE"])
def delete_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        db.session.delete(consulta)
        consulta_json = consulta._asdict()
        db.session.commit()
        return jsonify(consulta=consulta_json), 200

    return jsonify(msg="A consulta não existe"), 400
# END DELETE consulta by ID#

