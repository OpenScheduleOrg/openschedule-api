import random
import json
from datetime import date, time, datetime, timedelta, timezone

from conftest import app, client

from db import db, Consulta, Cliente, Clinica, generate_marcada


def test_add_consulta(app, client):

#   Marcando consultas com todos os usuários em todas as clinicas
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

    date_start = datetime.combine(date.today(), time(0))
    date_end = datetime.combine(date_start.date()+timedelta(weeks=1), time.max)

#   Buscando todas as consultas

    rs = client.get("/consultas")

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end).all()

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()

#   Buscando todas as consultas de uma clinica
    with app.app_context():
        id_clinica = Clinica.query.first().id

    rs = client.get("/consultas?id_clinica="+str(id_clinica))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_clinica=id_clinica)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()

#   Buscando todas as consultas de uma clinica no intervalo de uma semana
    rs = client.get("/consultas?id_clinica={}&date_start={}&date_end={}".format(id_clinica, date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_clinica=id_clinica).filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end).all()

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()

#   Buscando todas as consultas de um cliente
    with app.app_context():
        id_cliente = Cliente.query.first().id

    rs = client.get("/consultas?id_cliente="+str(id_cliente))


    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_cliente=id_cliente)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()


#   Buscando todas as consultas de um cliente no intervalo de uma semana
    rs = client.get("/consultas?id_cliente={}&date_start={}&date_end={}".format(id_cliente, date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_cliente=id_cliente).filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end).all()

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()

#   Buscando todas as consultas de um cliente em uma clinica
    rs = client.get("/consultas?id_cliente={}&id_clinica={}".format(id_cliente,id_clinica))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_cliente=id_cliente, id_clinica=id_clinica)

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()

#   Buscando todas as consultas de um cliente em uma clinica no intervalo de uma semana
    rs = client.get("/consultas?id_cliente={}&id_clinica={}&date_start={}&date_end={}".format(id_cliente, id_clinica, date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        consultas = Consulta.query.filter_by(id_cliente=id_cliente, id_clinica=id_clinica).filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end).all()

    expected_rs = {"status": "success", "data":{"consultas": [c._asjson() for c in consultas]}}

    assert expected_rs == rs.get_json()




def test_invalid_parameters_get_consulta(app, client):

#   busca com paramatros não utlizados
    rs = client.get("/consultas?inval=1&notvalid=0")

    assert rs.status_code == 406

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": {"inval":'1', "notvalid":'0'}, "detail":{"inval":"unusable", "notvalid":"unusable"}}

#   tentando busca consultas de uma clinica não cadastrada

    rs = client.get("/consultas?id_clinica=0")

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": {"id_clinica":'0'}, "detail":{"id_clinica": "not found"}}

#   tentando busca consultas de um cliente não cadastrada

    rs = client.get("/consultas?id_cliente=0")

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": {"id_cliente":'0'}, "detail":{"id_cliente": "not found"}}

#   tentando buscar consultas com date_start e date_end com valores não iso format

    rs = client.get("/consultas?date_start={}&date_end={}".format("notadateinisoformat", "thisisthesame"))

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": {"date_start":"notadateinisoformat", "date_end": "thisisthesame"}, "detail":{"date_start": "invalid", "date_end":"invalid"}}

#   tentando buscar consultas com date_start > date_end

    date_start = datetime.combine(date.today(), time(0))
    date_end = datetime.combine(date_start.date()+timedelta(weeks=1), time.max)

    rs = client.get("/consultas?date_start={}&date_end={}".format(date_end, date_start))

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {"payload": {"date_start":str(date_end), "date_end": str(date_start)}, "detail":{"date_start": "invalid", "date_end":"invalid"}}


