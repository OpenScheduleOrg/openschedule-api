from datetime import date, time, datetime, timezone, timedelta

from app.models import db, Cliente, Clinica, Consulta, Horario

clientes_data = [{"nome":"Ryan Ray", "cpf":"23323432134", "telefone":"88473838934", "endereco":"Bairro foo, rua bar", "nascimento":date(2000, 10, 10)}]

clinicas_data = [{"nome":"Doutor Foo Bar", "tipo":"Odontologica", "telefone":"78673426732", "endereco":"Cidade c, 52323-2312, bairro Bar, rua Foo", "longitude": "93713413", "latitude":"23432432"}, {"nome":"Clinica Doutor Gelol", "tipo":"Fisioterapia", "telefone":"88673426732", "endereco":"Cidade b, 98232-2312, bairro sao fulano, rua das clinicas", "longitude": "33713413", "latitude":"23212432"} ]

horarios_data = [{"am_inicio": time(hour=10), "am_fim": time(hour=14), "pm_inicio": time(hour=17), "pm_fim": time(hour=20), "intervalo": timedelta(minutes=30), "almoco": True, "dia_semana": 0}, {"am_inicio": time(hour=10), "pm_fim": time(hour=20), "intervalo": timedelta(minutes=30), "dia_semana": 0}]

consultas_data = [{"realizada": False}]

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("PRAGMA foreign_keys = ON")

def set_up_db():
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)
    db.create_all()
    create_clientes(clientes_data)
    create_clinicas(clinicas_data)
    create_horarios(horarios_data)
    create_consultas(consultas_data)


def create_clientes(clientes: list):

    with db.session() as session:
        for c in clientes:
            c_copy = c.copy()
            db.session.add(Cliente(**c_copy))
        session.commit()

def create_clinicas(clinicas: list):
    with db.session() as session:
        for c in clinicas:
            session.add(Clinica(**c))
        session.commit()

def create_horarios(horarios: list):

    clinicas = Clinica.query.all()

    if len(horarios):
        with db.session() as session:
            i = 0

            for c in clinicas:

                horario = horarios[i].copy()
                horario["id_clinica"] = c.id
                for wd in range(0, 5):
                    horario["dia_semana"] = wd

                    session.add(Horario(**horario))
                i += 1
                if(len(horarios) <= i):
                    i = 0

            session.commit()

def generate_marcada(id_clinica, hora=None):

    data = datetime.now(timezone.utc) + timedelta(days=1)
    week_day = data.weekday()


    if(week_day == 5):
        data = data + timedelta(days=2)
        week_day = 0
    elif(week_day == 6):
        data =  data + timedelta(days=1)
        week_day = 0


    horario = Horario.query.filter_by(id_clinica=id_clinica, dia_semana=week_day).first()

    marcada = datetime.combine(data.date(), hora or horario.am_inicio, tzinfo=timezone.utc)
    one_day = timedelta(days=1)

    while Consulta.query.filter(Consulta.id_clinica == id_clinica).filter(Consulta.marcada >= datetime.combine(marcada.date(), horario.am_inicio, tzinfo=timezone.utc)).filter(Consulta.marcada < datetime.combine(marcada.date(), horario.pm_fim, tzinfo=timezone.utc)).first() is not None:
        if marcada.weekday() == 5:
            marcada += timedelta(days=2)
        else:
            marcada += one_day

    return marcada


def create_consultas(consultas: list):

    id_clinica = Clinica.query.first().id
    id_cliente = Cliente.query.first().id

    marcada = generate_marcada(id_clinica)
    c = {}
    with db.session() as session:
        c["id_cliente"] = id_cliente
        c["id_clinica"] = id_clinica
        c["marcada"] = marcada
        session.add(Consulta(**c))
        session.commit()

