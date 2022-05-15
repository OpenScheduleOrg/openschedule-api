from conftest import app, client

from db import db, Clinica


def test_all_clinicas(app, client):

    rs = client.get("/clinicas")

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        clinicas = Clinica.query.all()

    expected_rs = {"status": "success", "data":{"clinicas": [c.as_json() for c in clinicas]}}

    assert expected_rs == rs_json
