import random
from datetime import date, time, datetime, timedelta

from faker import Faker

from app.models import db, select, session, result_to_json, Cliente, Clinica, Consulta, Horario, Usuario, NivelAcesso

fake = Faker(["pt_BR"])

NUMBERS_CLIENTES = 5
NUMBERS_USUARIOS = 3
NUMBERS_CLINICAS = 2


horario_templates = [{
    "am_inicio": time(hour=7),
    "am_fim": time(hour=11),
    "pm_inicio": time(hour=14),
    "pm_fim": time(hour=17),
    "intervalo": timedelta(minutes=30),
    "dia_semana": 0
}, {
    "am_inicio": time(hour=7),
    "pm_fim": time(hour=17),
    "intervalo": timedelta(minutes=30),
    "dia_semana": 0
}]


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("PRAGMA foreign_keys = ON")


def set_up_db():
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)
    db.create_all()
    create_clientes()
    create_clinicas()
    create_usuarios()
    create_horarios()
    create_consultas()


def create_clientes():

    with db.session():
        for _ in range(NUMBERS_CLIENTES):
            db.session.add(Cliente(
                nome=fake.first_name(), sobrenome=fake.last_name(),
                cpf=fake.cpf(),
                telefone=fake.msisdn()[-10:],
                endereco=fake.address(), nascimento=fake.date_between()))
        session.commit()


def create_clinicas():
    with db.session():
        for i in range(NUMBERS_CLINICAS):
            session.add(
                Clinica(
                    nome=fake.bs(),
                    tipo=f"clinica tipo {i}",
                    telefone=fake.msisdn()[-10:],
                    endereco=fake.address(),
                    latitude=str(fake.coordinate()),
                    longitude=str(fake.latitude()),
                ))
        session.commit()


def create_horarios():
    horarios = horario_templates

    clinicas = Clinica.query.all()

    if len(horarios):
        with db.session():
            i = 0

            for c in clinicas:

                horario = horarios[i % 2].copy()
                horario["clinica_id"] = c.id
                for wd in range(0, 5):
                    horario["dia_semana"] = wd

                    session.add(Horario(**horario))
                i += 1
                if (len(horarios) <= i):
                    i = 0

            session.commit()


def create_usuarios():
    clinicas = Clinica.query.all()

    with db.session():
        for clinica in clinicas:
            session.add(Usuario(nome=fake.first_name(), sobrenome=fake.last_name(),
                        foto=fake.image_url(), nivel_acesso=NivelAcesso.ADMIN,
                        username=fake.user_name(), email=fake.email(),
                        password=fake.password(), clinica_id=clinica.id))

            session.add(Usuario(nome=fake.first_name(), sobrenome=fake.last_name(),
                        foto=fake.image_url(), nivel_acesso=NivelAcesso.CLINICA_ADMIN,
                        username=fake.user_name(), email=fake.email(),
                        password=fake.password(), clinica_id=clinica.id))

            session.add(Usuario(nome=fake.first_name(), sobrenome=fake.last_name(),
                        foto=fake.image_url(), nivel_acesso=NivelAcesso.FUNCIONARI0,
                        username=fake.user_name(), email=fake.email(),
                        password=fake.password(), clinica_id=clinica.id))
        session.commit()


def generate_marcada(clinica_id):

    data = datetime.now() + timedelta(days=1)
    week_day = data.weekday()

    if (week_day == 5):
        data = data + timedelta(days=2)
        week_day = 0
    elif (week_day == 6):
        data = data + timedelta(days=1)
        week_day = 0

    horario = Horario.query.filter_by(clinica_id=clinica_id,
                                      dia_semana=week_day).first()

    marcada = datetime.combine(data.date(), horario.am_inicio)

    while Consulta.query.filter_by(clinica_id=clinica_id,
                                   marcada=marcada).first() is not None:
        if (marcada + timedelta(days=1)).weekday() == 5:
            marcada += timedelta(days=3)
        elif horario.am_fim and (
            (marcada + horario.intervalo).time() >= horario.am_fim
                and marcada.time() < horario.pm_inicio):
            marcada = datetime.combine(marcada.date(), horario.pm_inicio)
        elif (marcada + horario.intervalo).time() >= horario.pm_fim:
            marcada = datetime.combine(marcada.date() + timedelta(days=1),
                                       horario.am_inicio)
        else:
            marcada += horario.intervalo

    return marcada


def create_consultas():

    clinicas = Clinica.query.all()
    clientes = Cliente.query.all()

    with db.session():
        for cliente in clientes:
            for clinica in clinicas:
                c = {}
                marcada = generate_marcada(clinica.id)
                c["cliente_id"] = cliente.id
                c["clinica_id"] = clinica.id
                c["marcada"] = marcada
                session.add(Consulta(**c))
        session.commit()
