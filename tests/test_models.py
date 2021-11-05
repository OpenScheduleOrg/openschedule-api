from datetime import date

from app.models import db, Cliente, Clinica, Consulta
from conftest import app

def test_add_cliente(app):
    c1 = Cliente(nome="Ryan Ray", cpf="23323432134", telefone="88473838934", endereco="Bairro foo, rua bar",nascimento=date(2000, 10, 10))

    with app.app_context():
        db.session.add(c1)
        db.session.commit()

