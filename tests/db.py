import json
from datetime import date

from app.models import db, Cliente, Clinica, Consulta, Horario

clientes_data = [{"nome":"Ryan Ray", "cpf":"23323432134", "telefone":"88473838934", "endereco":"Bairro foo, rua bar", "nascimento":"2000-10-10"}]

def set_up_db():
    db.create_all()
    create_cliente(*clientes_data)


def create_cliente(*clientes: list):
    for c in clientes:
        c_copy = c.copy()
        c_copy["nascimento"] = date.fromisoformat(c["nascimento"])
        db.session.add(Cliente(**c_copy))

    db.session.commit()

