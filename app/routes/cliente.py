from app.routes import api

from datetime import datetime, time, date, timedelta
import calendar

from flask import request

from app.common.utils import gen_response, insertSort, CPFormat
from app.models import Cliente



@api.route("/cliente", methods=["POST"])
def post_cliente():
    body = request.get_json()

    nome = body["nome"]
    cpf = CPFormat(body["cpf"])
    telefone = body["telefone"]
    if cpf:
        try:
            cliente = Cliente(nome, cpf, telefone)
            db.session.add(cliente)
            db.session.commit()
            return gen_response(200, cliente=cliente.to_json(), msg="Cliente cadastrado com sucesso")
        except Exception as e:
            print('Erro', e)

    return gen_response(400, msg="Erro ao cadastrar cliente")
# END POST cliente #


# GET clientes #
@api.route("/clientes", methods=["GET"])
def get_clientes():
    clientes: list[Cliente] = Cliente.query.all()
    clientes_json = [cliente.to_json() for cliente in clientes]

    return gen_response(200, clientes=clientes_json)
# END GET clientes #


# GET cliente by ID #
@api.route("/cliente/<id>", methods=["GET"])
def get_cliente(id):
    cliente_json = {}
    cliente: Cliente or None = Cliente.query.get(id)

    if(cliente):
        cliente_json = cliente.to_json()
        consultas: list[Consulta] = insertSort(cliente.consultas)
        cliente_json["consultas"] = {}
        for consulta in consultas:
            data_str = str(consulta.agenda.data)
            if(not data_str in cliente_json["consultas"]):
                cliente_json["consultas"][data_str] = [
                    {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome}]
            else:
                for key, day_consultas in enumerate(cliente_json["consultas"][data_str][:]):
                    if(day_consultas["hora"] > consulta.agenda.hora):
                        cliente_json["consultas"][data_str].insert(
                            key, {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome})
                        break
                    if(key == len(cliente_json["consultas"][data_str])-1):
                        cliente_json["consultas"][data_str] += [
                            {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome}]

        return gen_response(200, cliente=cliente_json)

    return gen_response(400, msg="Cliente não existe")
# END GET cliente by ID #


# GET cliente by telefone #
@api.route("/telefone/<telefone>", methods=["GET"])
def get_cliente_telefone(telefone):
    cliente_json = {}
    cliente: Cliente = Cliente.query.filter_by(telefone=telefone).first()
    if(cliente):
        cliente_json = cliente.to_json()
        consulta: Consulta
        cliente_json["consultas"] = [{"data": consulta.agenda.data, "hora": consulta.agenda.hora,
                                      "clinica": consulta.clinica.nome} for consulta in cliente.consultas]

    return gen_response(200, cliente=cliente_json)
# END GET cliente by telefone #


