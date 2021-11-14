import random
from datetime import date, time, datetime, timezone, timedelta

from app.models import db, Cliente, Clinica, Consulta, Horario

NUMBERS_CLIENTES = 10
NUMBERS_CLINICAS = 2

cliente_template = {"nome":"cliente {}", "cpf":"{}{}{}{}{}{}{}{}{}{}{}", "telefone":"{}{}{}{}{}{}{}{}{}{}{}", "endereco":"Bairro do cliente {}, rua do cliente {}", "nascimento":date(2000, 10, 10)}

clinica_template = {"nome":"Clinia {}", "tipo":"Tipo de clinica {}", "telefone":"{}{}{}{}{}{}{}{}{}{}{}", "endereco":"bairro da clinica {}, rua da clinica {}", "longitude": "893713413", "latitude":"23432432"}

horario_templates = [
    {"am_inicio": time(hour=10), "am_fim": time(hour=14), "pm_inicio": time(hour=17), "pm_fim": time(hour=20), "intervalo": timedelta(minutes=30), "almoco": True, "dia_semana": 0},
    {"am_inicio": time(hour=10), "pm_fim": time(hour=20), "intervalo": timedelta(minutes=30), "dia_semana": 0}]

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
                horario["id_clinica"] = c.id
                for wd in range(0, 5):
                    horario["dia_semana"] = wd

                    session.add(Horario(**horario))
                i += 1
                if(len(horarios) <= i):
                    i = 0

            session.commit()

def generate_marcada(id_clinica):

    data = datetime.now(timezone.utc) + timedelta(days=1)
    week_day = data.weekday()


    if(week_day == 5):
        data = data + timedelta(days=2)
        week_day = 0
    elif(week_day == 6):
        data =  data + timedelta(days=1)
        week_day = 0

    horario = Horario.query.filter_by(id_clinica=id_clinica, dia_semana=week_day).first()

    marcada = datetime.combine(data.date(), horario.am_inicio, tzinfo=timezone.utc)

    while Consulta.query.filter_by(id_clinica=id_clinica, marcada=marcada).first() is not None:
        if (marcada+timedelta(days=1)).weekday() == 5:
            marcada += timedelta(days=3)
        elif horario.almoco and ((marcada+horario.intervalo).time() >= horario.am_fim and marcada.time() < horario.pm_inicio):
            marcada = datetime.combine(marcada.date(), horario.pm_inicio, tzinfo=timezone.utc)
        elif (marcada+horario.intervalo).time() >= horario.pm_fim:
            marcada = datetime.combine(marcada.date() + timedelta(days=1), horario.am_inicio, tzinfo=timezone.utc)
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
                    c["id_cliente"] = cliente.id
                    c["id_clinica"] = clinica.id
                    c["marcada"] = marcada
                    session.add(Consulta(**c))
        session.commit()

