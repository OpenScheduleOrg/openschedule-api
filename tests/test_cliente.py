from datetime import date, datetime

from conftest import app, client

from db import Cliente

def test_all_clientes(app, client):
    rs = client.get("/clientes")

    assert rs.status_code == 200

    rs_json = rs.get_json()

    with app.app_context():
        clientes = Cliente.query.all()

    expected_rs = {"status":"success", "data": {"clientes": [c.as_json() for c in clientes]}}

    assert expected_rs == rs_json

def test_add_cliente(app, client):

    new_cliente = {"nome": "Bob Test", "cpf":"67863478678", "telefone":"89987436743", "endereco":"bairro da flores, rua verde 123", "nascimento":date(2000, 10, 10).isoformat()}

    rs = client.post("/cliente", json=new_cliente)

    assert rs.status_code == 201

    rs_json = rs.get_json()

    with app.app_context():
        cliente = Cliente.query.filter_by(**new_cliente).first()
        cliente_dict = cliente.as_json()

    expected_rs = {"status": "success", "data":{"cliente": cliente_dict}}

    assert expected_rs == rs_json

def test_add_invalid_cliente(app, client):
    pass

def test_get_cliente(app, client):
    pass

def test_get_not_exist_cliente(app, client):
    pass

def test_update_cliente(app, client):
    pass

def test_update_invalid_cliente(app, client):
    pass



