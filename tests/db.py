import random
from datetime import date, time, datetime, timedelta

from app.models import db, session, select, result_to_json,Cliente, Clinica, Consulta, Horario

NUMBERS_CLIENTES = 15
NUMBERS_CLINICAS = 4

cliente_template = {"nome":"cliente {}", "cpf":"{}{}{}{}{}{}{}{}{}{}{}", "telefone":"{}{}{}{}{}{}{}{}{}{}{}", "endereco":"Bairro do cliente {}, rua do cliente {}", "nascimento":date(2000, 10, 10)}

clinica_template = {"nome":"Clinica {}", "tipo":"Tipo de clinica {}", "telefone":"{}{}{}{}{}{}{}{}{}{}{}", "endereco":"bairro da clinica {}, rua da clinica {}", "longitude": "893713413", "latitude":"23432432"}

horario_templates = [
    {"am_inicio": time(hour=7), "am_fim": time(hour=11), "pm_inicio": time(hour=14), "pm_fim": time(hour=17), "intervalo": timedelta(minutes=30), "almoco": True, "dia_semana": 0},
    {"am_inicio": time(hour=7), "pm_fim": time(hour=17), "intervalo": timedelta(minutes=30), "dia_semana": 0}]

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("PRAGMA foreign_keys = ON")

def set_up_db():
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)
    db.create_all()
    create_clientes()
    create_clinicas()
    create_horarios()
    create_consultas()


def create_clientes():

    clientes = []
    for i in range(1, NUMBERS_CLIENTES):
        cliente = cliente_template.copy()
        cliente["nome"] = cliente["nome"].format(i)
        cliente["cpf"] = cliente["cpf"].format(random.randint(1, 9), *[random.randint(0, 9) for _ in range (10)])
        cliente["telefone"] = cliente["telefone"].format(random.randint(1, 9), random.randint(1, 9), 9, *[random.randint(0, 9) for _ in range (8)])
        cliente["endereco"] = cliente["endereco"].format(i, i)
        cliente["nascimento"] = cliente["nascimento"] + timedelta(days=i)
        clientes.append(cliente)

    with db.session() as session:
        for c in clientes:
            c_copy = c.copy()
            db.session.add(Cliente(**c_copy))
        session.commit()

def create_clinicas():

    clinicas = []
    for i in range(1, NUMBERS_CLINICAS):
        clinica = clinica_template.copy()
        clinica["nome"] = clinica["nome"].format(i)
        clinica["tipo"] = clinica["tipo"].format(i)
        clinica["telefone"] = clinica["telefone"].format(random.randint(1, 9), random.randint(1, 9), 9, *[random.randint(0, 9) for _ in range (8)])
        clinica["endereco"] = clinica["endereco"].format(i, i)
        clinicas.append(clinica)

    with db.session() as session:
        for c in clinicas:
            session.add(Clinica(**c))
        session.commit()

def create_horarios():
    horarios = horario_templates

    clinicas = Clinica.query.all()

    if len(horarios):
        with db.session() as session:
            i = 0

            for c in clinicas:

                horario = horarios[i%2].copy()
                horario["clinica_id"] = c.id
                for wd in range(0, 5):
                    horario["dia_semana"] = wd

                    session.add(Horario(**horario))
                i += 1
                if(len(horarios) <= i):
                    i = 0

            session.commit()

def generate_marcada(clinica_id):

    data = datetime.now() + timedelta(days=1)
    week_day = data.weekday()


    if(week_day == 5):
        data = data + timedelta(days=2)
        week_day = 0
    elif(week_day == 6):
        data =  data + timedelta(days=1)
        week_day = 0

    horario = Horario.query.filter_by(clinica_id=clinica_id, dia_semana=week_day).first()

    marcada = datetime.combine(data.date(), horario.am_inicio)

    while Consulta.query.filter_by(clinica_id=clinica_id, marcada=marcada).first() is not None:
        if (marcada+timedelta(days=1)).weekday() == 5:
            marcada += timedelta(days=3)
        elif horario.almoco and ((marcada+horario.intervalo).time() >= horario.am_fim and marcada.time() < horario.pm_inicio):
            marcada = datetime.combine(marcada.date(), horario.pm_inicio)
        elif (marcada+horario.intervalo).time() >= horario.pm_fim:
            marcada = datetime.combine(marcada.date() + timedelta(days=1), horario.am_inicio)
        else:
            marcada += horario.intervalo

    return marcada


def create_consultas():

    clinicas = Clinica.query.all()
    clientes = Cliente.query.all()

    with db.session() as session:
        for cliente in clientes:
                for clinica in clinicas:
                    c = {}
                    marcada = generate_marcada(clinica.id)
                    c["cliente_id"] = cliente.id
                    c["clinica_id"] = clinica.id
                    c["marcada"] = marcada
                    session.add(Consulta(**c))
        session.commit()

