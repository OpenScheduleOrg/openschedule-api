from datetime import date, time, datetime, timedelta

from db import session, select, result_to_json
from db import Consulta, Cliente, Clinica, generate_marcada, Horario


def test_add_consulta(app, client, access_token):

    #   Marcando consultas com todos os usuários em todas as clinicas
    with app.app_context():
        clientes = session.execute(select(Cliente)).scalars().all()
        clinicas = session.execute(select(Clinica)).scalars().all()

    i = 0
    for cliente in clientes:

        for clinica in clinicas:
            new_consulta = {"descricao": "Avaliação"} if i % 2 == 0 else {}
            new_consulta["cliente_id"] = cliente.id
            new_consulta["clinica_id"] = clinica.id

            with app.app_context():
                new_consulta["marcada"] = generate_marcada(
                    new_consulta["clinica_id"]).isoformat()

            rs = client.post("/api/consulta", json=new_consulta)
            print(rs.json)

            assert rs.status_code == 201

            rs_json = rs.get_json()
            new_consulta["marcada"] = datetime.fromisoformat(
                new_consulta["marcada"])

            with app.app_context():
                consulta = session.execute(
                    select(Consulta).filter_by(**new_consulta)).scalars().first()
            expected_rs = {
                "status": "success",
                "data": {
                    "consulta": consulta.as_json()
                }
            }

            assert expected_rs == rs_json


def test_invalid_parameters_add_consulta(app, client):

    #   Tentando adicionar sem nenhum dado
    new_consulta = {}

    rs = client.post("/api/consulta", json=new_consulta)

    assert rs.status_code == 400

    rs_json = rs.get_json()
    assert rs_json["status"] == "fail"

    expected_data = {
        "payload": new_consulta,
        "detail": {
            "clinica_id": "required",
            "cliente_id": "required",
            "marcada": "required"
        }
    }

    assert rs_json["data"] == expected_data

    #   Tentando cadastro de uma consulta em um cliente não cadastrado
    with app.app_context():
        consulta = session.execute(select(Consulta)).scalars().first()

        if (not consulta):
            raise Exception(
                "It is not possible to continue without any registered consulta"
            )

        new_consulta["cliente_id"] = consulta.cliente_id
        new_consulta["clinica_id"] = consulta.clinica_id
        new_consulta["marcada"] = str(
            generate_marcada(new_consulta["clinica_id"]))

    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["cliente_id"] = 0

    rs = client.post("/api/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": new_consulta_invalid,
        "detail": {
            "cliente_id": "invalid"
        }
    }

    #   Tentando cadastro de uma consulta em uma clinica não cadastrada
    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["clinica_id"] = 0

    rs = client.post("/api/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": new_consulta_invalid,
        "detail": {
            "clinica_id": "invalid"
        }
    }

    #   Data e hora no formato errado
    new_consulta_invalid = new_consulta.copy()
    new_consulta_invalid["marcada"] = "not iso format"

    rs = client.post("/api/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": new_consulta_invalid,
        "detail": {
            "marcada": "invalid"
        }
    }

    #   Tentando adicionar uma consulta em horário já marcado
    new_consulta_invalid = new_consulta.copy()
    with app.app_context():
        marcada = session.execute(
            select(Consulta.marcada).where(
                Consulta.clinica_id ==
                new_consulta_invalid["clinica_id"])).scalars().first()

    new_consulta_invalid["marcada"] = marcada.isoformat()

    rs = client.post("/api/consulta", json=new_consulta_invalid)
    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": new_consulta_invalid,
        "detail": {
            "marcada": "invalid"
        }
    }

    #  tentando unserir com parametros não utilizados

    new_consulta_invalid = {
        "invalid": "data wothless",
        "notvalid": "data unusable",
        **new_consulta
    }
    rs = client.post("/api/consulta", json=new_consulta_invalid)

    assert rs.status_code == 422

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": new_consulta_invalid,
        "detail": {
            "invalid": "unusable",
            "notvalid": "unusable"
        }
    }


def test_get_consultas(app, client):

    expected_rs = {"status": "success", "data": {}}

    date_start = datetime.combine(date.today(), time(0))
    date_end = datetime.combine(date_start.date() + timedelta(weeks=1),
                                time.max)

    columns = (Consulta.id, Consulta.marcada, Consulta.realizada,
               Consulta.descricao, Consulta.duracao)
    cliente_columns = (Consulta.cliente_id, Cliente.nome.label("cliente_nome"),
                       Cliente.sobrenome.label("cliente_sobrenome"),
                       Cliente.telefone.label("cliente_telefone"),
                       Cliente.cpf.label("cliente_cpf"))
    clinica_columns = (
        Consulta.clinica_id,
        Clinica.nome.label("clinica_nome"),
        Clinica.tipo.label("clinica_tipo"),
    )

    with app.app_context():
        clinica = session.execute(
            select(Clinica.id, Clinica.nome, Clinica.tipo, Clinica.endereco,
                   Clinica.telefone)).first()._asdict()
        cliente = session.execute(
            select(Cliente.id, Cliente.nome, Cliente.telefone,
                   Cliente.endereco)).first()._asdict()


#   Buscando todas as consultas

    rs = client.get("/api/consultas")

    assert rs.status_code == 200

    with app.app_context():
        stmt = select(*columns, *cliente_columns, *clinica_columns).join(
            Consulta.cliente).join(Consulta.clinica).where(
                Consulta.marcada >= date_start, Consulta.marcada <= date_end)
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas}

    assert expected_rs == rs.get_json()

    #   Buscando uma consulta pelo id
    with app.app_context():
        stmt = select(*columns, *cliente_columns, *clinica_columns).join(
            Consulta.cliente).join(Consulta.clinica)
        consulta = result_to_json(session.execute(stmt),
                                  first=True,
                                  marcada=lambda v: v.isoformat())

    rs = client.get("/api/consultas/" + str(consulta["id"]))

    assert rs.status_code == 200

    expected_rs["data"] = {"consulta": consulta}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas em um determinado intervalo
    rs = client.get("/api/consultas?date_start={}&date_end={}".format(
        date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        stmt = select(*columns, *cliente_columns, *clinica_columns).join(
            Consulta.cliente).join(Consulta.clinica).where(
                Consulta.marcada >= date_start, Consulta.marcada <= date_end)
        consulta = result_to_json(session.execute(stmt),
                                  marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de uma clinica

    rs = client.get("/api/consultas?clinica_id=" + str(clinica["id"]))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        stmt = select(*columns, *cliente_columns).join(
            Consulta.cliente).where(Consulta.clinica_id == clinica["id"])
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas, "clinica": clinica}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de uma clinica no intervalo de uma semana
    rs = client.get(
        "/api/consultas?clinica_id={}&date_start={}&date_end={}".format(
            clinica["id"], date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        stmt = select(*columns, *cliente_columns).join(Consulta.cliente).where(
            Consulta.clinica_id == clinica["id"]).where(
                Consulta.marcada >= date_start, Consulta.marcada <= date_end)
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas, "clinica": clinica}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de um cliente
    rs = client.get("/api/consultas?cliente_id=" + str(cliente["id"]))

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        stmt = select(*columns, *clinica_columns).join(
            Consulta.clinica).where(Consulta.cliente_id == cliente["id"])
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas, "cliente": cliente}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de um cliente no intervalo de uma semana
    rs = client.get(
        "/api/consultas?cliente_id={}&date_start={}&date_end={}".format(
            cliente["id"], date_start.isoformat(), date_end.isoformat()))

    assert rs.status_code == 200

    with app.app_context():
        stmt = select(*columns, *clinica_columns).join(Consulta.clinica).where(
            Consulta.cliente_id == cliente["id"]).where(
                Consulta.marcada >= date_start, Consulta.marcada <= date_end)
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {"consultas": consultas, "cliente": cliente}

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de um cliente em uma clinica
    rs = client.get("/api/consultas?cliente_id={}&clinica_id={}".format(
        cliente["id"], clinica["id"]))

    assert rs.status_code == 200

    with app.app_context():
        stmt = select(*columns).join(Consulta.clinica).where(
            Consulta.cliente_id == cliente["id"],
            Consulta.clinica_id == clinica["id"])
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {
        "consultas": consultas,
        "cliente": cliente,
        "clinica": clinica
    }

    assert expected_rs == rs.get_json()

    #   Buscando todas as consultas de um cliente em uma clinica no intervalo de uma semana
    rs = client.get(
        "/api/consultas?cliente_id={}&clinica_id={}&date_start={}&date_end={}".
        format(cliente["id"], clinica["id"], date_start.isoformat(),
               date_end.isoformat()))

    assert rs.status_code == 200

    with app.app_context():
        stmt = select(*columns).where(
            Consulta.cliente_id == cliente["id"],
            Consulta.clinica_id == clinica["id"]).where(
                Consulta.marcada >= date_start, Consulta.marcada <= date_end)
        consultas = result_to_json(session.execute(stmt),
                                   marcada=lambda v: v.isoformat())

    expected_rs["data"] = {
        "consultas": consultas,
        "cliente": cliente,
        "clinica": clinica
    }

    assert expected_rs == rs.get_json()


def test_invalid_parameters_get_consulta(app, client):

    #   busca com paramatros não utlizados
    rs = client.get("/api/consultas?invalid=1&notvalid=0")

    assert rs.status_code == 422

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "invalid": '1',
            "notvalid": '0'
        },
        "detail": {
            "invalid": "unusable",
            "notvalid": "unusable"
        }
    }

    #   tentando busca consultas de uma clinica não cadastrada
    rs = client.get("/api/consultas?clinica_id=0")

    assert rs.status_code == 404

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "clinica_id": '0'
        },
        "detail": {
            "clinica_id": "not found"
        }
    }

    #   tentando buscar uma consulta não cadastrada
    rs = client.get("/api/consultas/0")

    assert rs.status_code == 404

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "id": 0
        },
        "detail": {
            "id": "not found"
        }
    }

    #   tentando busca consultas de um cliente não cadastrada
    rs = client.get("/api/consultas?cliente_id=0")

    assert rs.status_code == 404

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "cliente_id": '0'
        },
        "detail": {
            "cliente_id": "not found"
        }
    }

    #   tentando buscar consultas com date_start e date_end com valores não iso format

    rs = client.get("/api/consultas?date_start={}&date_end={}".format(
        "notadateinisoformat", "thisisthesame"))

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "date_start": "notadateinisoformat",
            "date_end": "thisisthesame"
        },
        "detail": {
            "date_start": "invalid",
            "date_end": "invalid"
        }
    }

    #   tentando buscar consultas com date_start > date_end

    date_start = datetime.combine(date.today(), time(0))
    date_end = datetime.combine(date_start.date() + timedelta(weeks=1),
                                time.max)

    rs = client.get("/api/consultas?date_start={}&date_end={}".format(
        date_end, date_start))

    assert rs.status_code == 400

    rs_json = rs.get_json()

    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "payload": {
            "date_start": str(date_end),
            "date_end": str(date_start)
        },
        "detail": {
            "date_start": "invalid",
            "date_end": "invalid"
        }
    }


def test_update_consulta(app, client):

    expected_rs = {"status": "success", "data": {}}

    #   atualizando uma consulta
    body = {"descricao": "Consulta realizada", "realizada": True}
    with app.app_context():
        consulta = session.execute(select(Consulta)).scalars().first()
        body["marcada"] = generate_marcada(consulta.id).isoformat()

    rs = client.put("/api/consulta/%i" % (consulta.id), json=body)

    assert rs.status_code == 200

    with app.app_context():
        consulta = session.get(Consulta, consulta.id)

    expected_rs["data"] = {"consulta": consulta.as_json()}
    for key, value in body.items():
        if key == "marcada":
            value = datetime.fromisoformat(value)
        assert consulta.__dict__[key] == value

    assert expected_rs == rs.get_json()


def test_invalid_parameters_update_consulta(app, client):

    with app.app_context():
        clinica_id = session.execute(select(Clinica.id)).scalars().first()
        consultas = session.execute(
            select(Consulta).filter_by(clinica_id=clinica_id)).scalars().all()
        if (len(consultas) < 2):
            raise Exception("Need more than 1 consulta in a same clinica")
        horario = session.execute(
            select(Horario).filter_by(
                clinica_id=consultas[1].clinica_id)).scalars().first()


#   tentando atualizar uma consulta não existente

    body = {"marcada": datetime.now().isoformat(), "realizada": True}

    rs = client.put("/api/consulta/%i" % (0), json=body)

    rs_json = rs.get_json()

    assert rs.status_code == 404
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "detail": {
            "id": "not found"
        },
        "payload": {
            "id": 0,
            **body
        }
    }

    #   tentando atualizar uma consulta com uma data já utilizada

    body = {"marcada": consultas[1].marcada.isoformat(), "realizada": True}

    rs = client.put("/api/consulta/%i" % (consultas[0].id), json=body)

    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "detail": {
            "marcada": "invalid"
        },
        "payload": body
    }

    #   tentando atualizar uma consulta com uma data já utilizada

    body = {"marcada": consultas[1].marcada.isoformat()}

    rs = client.put("/api/consulta/%i" % (consultas[0].id), json=body)

    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "detail": {
            "marcada": "invalid"
        },
        "payload": body
    }

    #   tentando atualizar uma consulta para um horário fora do expediente

    body["marcada"] = (
        datetime.combine(consultas[0].marcada.date(), horario.am_inicio) -
        timedelta(minutes=10)).isoformat()

    rs = client.put("/api/consulta/%i" % (consultas[0].id), json=body)

    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "detail": {
            "marcada": "invalid"
        },
        "payload": body
    }

    if (horario.am_fim):
        body["marcada"] = (
            datetime.combine(consultas[0].marcada.date(), horario.am_fim) +
            timedelta(minutes=10)).isoformat()

        rs = client.put("/api/consulta/%i" % (consultas[0].id), json=body)

        rs_json = rs.get_json()

        assert rs.status_code == 400
        assert rs_json["status"] == "fail"
        assert rs_json["data"] == {
            "detail": {
                "marcada": "invalid"
            },
            "payload": body
        }

    body["marcada"] = (
        datetime.combine(consultas[0].marcada.date(), horario.pm_fim) +
        timedelta(minutes=10)).isoformat()

    rs = client.put("/api/consulta/%i" % (consultas[0].id), json=body)

    rs_json = rs.get_json()

    assert rs.status_code == 400
    assert rs_json["status"] == "fail"
    assert rs_json["data"] == {
        "detail": {
            "marcada": "invalid"
        },
        "payload": body
    }


def test_delete_consulta(app, client):

    #   removendo uma consulta

    with app.app_context():
        consulta_id = session.execute(select(Consulta)).scalars().first().id

    rs = client.delete("/api/consulta/%i" % (consulta_id))

    assert rs.status_code == 200

    expected_rs = {"status": "success", "data": None}
    assert expected_rs == rs.get_json()

    with app.app_context():
        consulta = session.get(Consulta, consulta_id)
        assert consulta is None


def test_invalid_parameters_delete_consulta(app, client):

    #   tentando remover uma consulta não existente

    rs = client.delete("/api/consulta/%i" % (0))

    assert rs.status_code == 404

    assert rs.get_json()["status"] == "fail"
    assert rs.get_json()["data"] == {
        "detail": {
            "id": "not found"
        },
        "payload": {
            "id": 0
        }
    }
