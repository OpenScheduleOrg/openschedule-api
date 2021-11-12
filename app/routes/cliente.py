from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from app.routes import api
from app.models import db, Cliente

@api.route("/cliente", methods=["POST"])
def post_cliente():
    body = request.get_json()

    if ("nascimento" in body):
        body["nascimento"] = date.fromisoformat(body["nascimento"])
    try:
        cliente = Cliente(**body)
        db.session.add(cliente)
        db.session.commit()
        db.session.refresh(cliente)
        return jsonify(cliente=cliente._asdict(), msg="cliente "+ cliente.nome +" cadastrado com sucesso", success=True), 201
    except Exception as e:
        print('Error: ', e)

    return jsonify(msg="Erro ao cadastrar cliente"), 400
# END POST cliente #


# GET clientes #
@api.route("/clientes", methods=["GET"])
def get_clientes():
    clientes: list[Cliente] = Cliente.query.all()
    clientes_json = [cliente._asdict() for cliente in clientes]

    return jsonify(clientes=clientes_json, qtd=len(clientes)), 200
# END GET clientes #


# GET cliente by ID #
@api.route("/cliente/<int:id>", methods=["GET"])
def get_cliente(id):
    cliente_json = {}
    cliente: Cliente or None = Cliente.query.get(id)

    if(cliente):
        cliente_json = cliente._asdict()
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

        return jsonify(cliente=cliente_json), 200

    return jsonify(msg="Cliente não existe"), 400
# END GET cliente by ID #


# GET cliente by telefone #
@api.route("/telefone/<telefone>", methods=["GET"])
def get_cliente_telefone(telefone):
    cliente_json = {}
    cliente: Cliente = Cliente.query.filter_by(telefone=telefone).first()
    if(cliente):
        cliente_json = cliente._asdict()
        consulta: Consulta
        cliente_json["consultas"] = [{"data": consulta.agenda.data, "hora": consulta.agenda.hora,
                                      "clinica": consulta.clinica.nome} for consulta in cliente.consultas]

    return jsonify(cliente=cliente_json), 200
# END GET cliente by telefone #


