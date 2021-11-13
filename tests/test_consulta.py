import random
import json
from datetime import date, time, datetime, timedelta, timezone

from conftest import app, client

from db import db, Consulta, Cliente, Clinica, generate_marcada


def test_api_add_consulta(app, client):
    with app.app_context():
        clientes = Cliente.query.all()
        clinicas = Clinica.query.all()

    i = 0
    for cliente in clientes:

        for clinica in clinicas:
            new_consulta = {"descricao": "Avaliação"} if i%2 == 0 else {}
            new_consulta["id_cliente"] = cliente.id
            new_consulta["id_clinica"] = clinica.id

            with app.app_context():
                new_consulta["marcada"] = str(generate_marcada(new_consulta["id_clinica"]))

            rs = client.post("/consulta", json=new_consulta)

            print(rs.get_json())

            assert rs.status_code == 201

            rs_json = rs.get_json()
            new_consulta["marcada"] = datetime.fromisoformat(new_consulta["marcada"])

            with app.app_context():
                consulta = Consulta.query.filter_by(**new_consulta).first()
            expected_rs = {"status": "success", "data": {"consulta": consulta._asjson()}}

            assert expected_rs == rs_json

def test_invalid_parameters_add_consulta(app, client):

#   Tentando adicionar sem nenhum dado
    new_consulta = {}

    rs = client.post("/consulta", json=new_consulta)

    assert rs.status_code == 400

    rs_json = rs.get_json()
    assert rs_json["status"] == "fail"

    expected_data = {"payload": new_consulta, "detail": {"id_clinica": "required", "id_cliente": "required", "marcada": "required"}}

    assert rs_json["data"] == expected_data

#   Tentando cadastro de uma consulta em um cliente não cadastrado

    with app.app_context():
        consultas = Consulta.query.all()

        if (not consultas):
            raise Exception("It is not possible to continue without any registered consulta")

        new_consulta["id_cliente"] = random.choice(consultas).id_cliente
        new_consulta["id_clinica"] = random.choice(consultas).id_clinica
        new_consulta["marcada"] = str(generate_marcada(new_consulta["id_clinica"]))

    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["id_cliente"] = 0

    rs = client.post("/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": new_consulta_invalid, "detail": {"id_cliente": "invalid"}}

#   Tentando cadastro de uma consulta em uma clinica não cadastrada

    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["id_clinica"] = 0

    rs = client.post("/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": new_consulta_invalid, "detail": {"id_clinica": "invalid"}}

#   Data e hora no formato errado

    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["marcada"] = "not iso format"

    rs = client.post("/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": new_consulta_invalid, "detail": {"marcada": "invalid"}}

#   Tentando adicionar uma consulta em horário já marcado

    new_consulta_invalid = new_consulta.copy()
    with app.app_context():
        marcada = Consulta.query.filter_by(id_clinica=new_consulta_invalid["id_clinica"]).first().marcada


    new_consulta_invalid["marcada"] = str(marcada)

    rs = client.post("/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": new_consulta_invalid, "detail": {"marcada": "invalid"}}



def test_get_consultas(app, client):

    date_start = datetime.combine(date.today(), time(0), tzinfo=timezone.utc)
    date_end = date_start + timedelta(weeks=1)

#   Buscando todas as consultas

    rs = client.get("/consultas")

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.all()

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    #assert expected_rs == rs.get_json()

#   Buscando todas as consultas de uma clinica
    with app.app_context():
        id_clinica = Clinica.query.first().id

    rs = client.get("/consultas?id_clinica="+str(id_clinica))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_clinica=id_clinica)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    #assert expected_rs == rs.get_json()

#   Buscando todas as consultas de uma clinica no intervalo de uma semana

    with app.app_context():
        id_clinica = Clinica.query.first().id


    rs = client.get("/consultas?id_clinica=".format(id_clinica, date))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_clinica=id_clinica).filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    #assert expected_rs == rs.get_json()


#   Buscando todas as consultas de um cliente
    with app.app_context():
        id_cliente = Cliente.query.first().id

    rs = client.get("/consultas?id_cliente="+str(id_cliente))


    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_clinica=id_clinica)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    #assert expected_rs == rs.get_json()



