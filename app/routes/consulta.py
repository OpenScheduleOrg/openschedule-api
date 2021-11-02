from app.routes import api

from datetime import datetime, time, date, timedelta
import calendar
from app.common.utils import gen_response, insertSort, CPFormat
from flask import request
from app.models import Consulta

# POST cosulta #
@api.route("/consulta", methods=["POST"])
def post_consulta():
    body = request.get_json()

    try:
        id_clinica = int(body['id_clinica'])
        id_cliente = int(body['id_cliente'])
        id_data = int(body['id_data'])

        clinica: Clinica = Clinica.query.get(id_clinica)
        data: Agenda = Agenda.query.get(id_data)
        cliente: Cliente = Cliente.query.get(id_cliente)

        if(clinica and data and cliente and (data.consultas == [])):
            consulta = Consulta(id_cliente, id_clinica, id_data)
            db.session.add(consulta)
            db.session.commit()

            return gen_response(200, consulta=consulta.to_json(), msg="Consulta marcada com sucesso")
    except Exception as e:
        print('Error:', e)

    return gen_response(400, msg="Algo de errado não está certo")
# END POST cosulta #


# GET consultas #
@api.route("/consultas", methods=["GET"])
def get_consultas():
    consultas = Consulta.query.all()
    consultas_json = [consulta.to_json() for consulta in consultas]

    return gen_response(200, consultas=consultas_json)
# END GET consultas #


# GET consulta by ID#
@api.route("/consulta/<id>", methods=["GET"])
def get_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        consulta_json = consulta.to_json()

    return gen_response(200, consulta=consulta_json)
# END GET consulta by ID#

# DELETE consulta by ID#
@api.route("/consulta/<id>", methods=["DELETE"])
def delete_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        db.session.delete(consulta)
        consulta_json = consulta.to_json()
        db.session.commit()
        return gen_response(200, consulta=consulta_json)

    return gen_response(400, msg="A consulta não existe")
# END DELETE consulta by ID#

