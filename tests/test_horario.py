import json

from conftest import app, client

from db import db, Horario


def test_all_horarios(app, client):

    rs = client.get("/horarios")

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        horarios_data = Horario.query.all()

    expected_rs = {"status": "success", "data": {"horarios": [h._asjson() for h in horarios_data]}}

    assert expected_rs == rs_json

