try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from helpers import CPFormat, gen_response, insertSort
from datetime import datetime, time, date, timedelta
import calendar
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
database_username = os.environ.get("DATABASE_USERNAME")
database_password = os.environ.get("DATABASE_PASSWORD")
database_host = os.environ.get("DATABASE_HOST")
database_schema = os.environ.get("DATABASE_SCHEMA")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{database_username}:{database_password}@{database_host}/{database_schema}"


db = SQLAlchemy(app)


###################################### MODELOS #####################################
class Clinica(db.Model):
    __tablename__ = "clinica"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(255))
    fone_contato = Column(String(20), nullable=False)
    endereco = Column(String(255), nullable=False)
    longitude = Column(String(45), nullable=False)
    latitude = Column(String(45), nullable=False)

    consultas = relationship("Consulta", back_populates="clinica")
    horarios = relationship("Horario", back_populates="clinica")

    def __init__(self, nome, tipo, fone_contato, endereco, longitude, latitude):
        self.nome = nome
        self.tipo = tipo
        self.fone_contato = fone_contato
        self.endereco = endereco
        self.long = longitude
        self.latitude = latitude

    def to_json(self):
        return {"id": self.id_clinica, "nome": self.nome, "tipo": self.tipo,
                "fone_contato": self.fone_contato, "endereco": {
                    "text": self.endereco,
                    "coord": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
                }


class Cliente(db.Model):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False)
    telefone = Column(String(20), nullable=False)
    endereco = Column(String(255), default=None)
    nascimento = Column(Date, default=None)

    consultas = relationship("Consulta", back_populates="cliente")
    horarios = relationship("Horario", back_populates="horario")
    def __init__(self,  nome, cpf, telefone, endereco, nascimento):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.nascimento = nascimento

    def to_json(self):
        return {"id": self.id_cliente, "nome": self.nome, "cpf": self.cpf, "telefone": self.telefone, "endereco": self.endereco, "nascimento":self.nascimento}


class Consulta(db.Model):
    __tablename__ = "consulta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    marcada = (DateTime)
    descricao = Column(String(255))
    realizada = Column(Boolean)
    id_cliente = Column(Integer, ForeignKey(
        'cliente.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey(
        'clinica.id'), nullable=False)

    cliente: Cliente = relationship("Cliente", back_populates="consultas")
    clinica: Clinica = relationship("Clinica", back_populates="consultas")

    def __init__(self, id_cliente, id_clinica, descricao, marcada, realizada=False):
        self.id_cliente = id_cliente
        self.id_clinica = id_clinica
        self.descricao = descircao
        self.marcada = marcada
        self.realizada = realizada

    def to_json(self):
        return {"id": self.id_consulta, "nome": self.cliente.nome,"marcada":self.marcada, "descricao":self.descricao, "realizada":self.realizada , "clinica": self.clinica.nome}

class Horario(db.Model):
    __tablename__ = "horario"

    id = Column(Integer, primary_key=True, autoincrement=True)

    am_inicio = Column(Time, nullable=False)
    am_fim = Column(Time)
    pm_inicio = Column(Time)
    pm_fim = Column(Time, nullable=False)
    intervalo = Column(Time, nullable=False)
    almoco = Column(Boolean)
    dia_semana = Column(Integer)

    id_clinica = Column(Integer, ForeignKey('clinica.id'), nullable=False)

    clinica = relationship('Clinica', back_populates='horarios')

    def __init__(self, am_inicio, am_fim, pm_inicio, pm_fim, intervalo, almoco, dia_semana):
        self.am_inicio = am_inicio
        self.am_fim = am_fim
        self.pm_inicio = pm_inicio
        self.pm_fim = pm_fim
        self.intervalo = intervalo
        self.almoco = almoco
        self.dia_semana = dia_semana

    def to_json(self):
        return {"id":self.id, "am_inicio":self.am_inicio, "am_fim":self.am_fim, "pm_inicio":self.pm_incio, "pm_fim":self.pm_fim, "intervalo":self.intervalo, "almoco":self.almoco, "dia_semana":self.dia_semana}

######################################################################################


###################################### CLIENTE #######################################
# POST cliente #
@app.route("/cliente", methods=["POST"])
def post_cliente():
    body = request.get_json()

    nome = body["nome"]
    cpf = CPFormat(body["cpf"])
    telefone = body["telefone"]
    if cpf:
        try:
            cliente = Cliente(nome, cpf, telefone)
            db.session.add(cliente)
            db.session.commit()
            return gen_response(200, cliente=cliente.to_json(), msg="Cliente cadastrado com sucesso")
        except Exception as e:
            print('Erro', e)

    return gen_response(400, msg="Erro ao cadastrar cliente")
# END POST cliente #


# GET clientes #
@app.route("/clientes", methods=["GET"])
def get_clientes():
    clientes: list[Cliente] = Cliente.query.all()
    clientes_json = [cliente.to_json() for cliente in clientes]

    return gen_response(200, clientes=clientes_json)
# END GET clientes #


# GET cliente by ID #
@app.route("/cliente/<id>", methods=["GET"])
def get_cliente(id):
    cliente_json = {}
    cliente: Cliente or None = Cliente.query.get(id)

    if(cliente):
        cliente_json = cliente.to_json()
        consultas: list[Consulta] = insertSort(cliente.consultas)
        cliente_json["consultas"] = {}
        for consulta in consultas:
            data_str = str(consulta.agenda.data)
            if(not data_str in cliente_json["consultas"]):
                cliente_json["consultas"][data_str] = [
                    {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome}]
            else:
                for key, day_consultas in enumerate(cliente_json["consultas"][data_str][:]):
                    if(day_consultas["hora"] > consulta.agenda.hora):
                        cliente_json["consultas"][data_str].insert(
                            key, {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome})
                        break
                    if(key == len(cliente_json["consultas"][data_str])-1):
                        cliente_json["consultas"][data_str] += [
                            {"id": consulta.id_consulta, "hora": consulta.agenda.hora, "clinica": consulta.clinica.nome}]

        return gen_response(200, cliente=cliente_json)

    return gen_response(400, msg="Cliente não existe")
# END GET cliente by ID #


# GET cliente by telefone #
@app.route("/telefone/<telefone>", methods=["GET"])
def get_cliente_telefone(telefone):
    cliente_json = {}
    cliente: Cliente = Cliente.query.filter_by(telefone=telefone).first()
    if(cliente):
        cliente_json = cliente.to_json()
        consulta: Consulta
        cliente_json["consultas"] = [{"data": consulta.agenda.data, "hora": consulta.agenda.hora,
                                      "clinica": consulta.clinica.nome} for consulta in cliente.consultas]

    return gen_response(200, cliente=cliente_json)
# END GET cliente by telefone #


######################################  AGENDA #######################################
# GET agenda #
@app.route("/agenda", methods=["GET"])
def get_agenda():
    datas: list[Agenda] = Agenda.query.all()

    datas_json = {}

    for data in datas:
        str_data = str(data.data)
        if(not str_data in datas_json):
            datas_json[str_data] = []

        body_data = {"hora": str(data.hora), "id": data.id_data}
        if(len(data.consultas)):
            consulta: Consulta = data.consultas[0]
            body_data["consulta"] = {
                "cliente": consulta.cliente.to_json(), "clinica": consulta.clinica.to_json()}

        datas_json[str_data] += [body_data]

    return gen_response(200, **datas_json)
# END GET agenda #


# GET horarios by dia do mês #
@app.route("/horarios/<day>", methods=["GET"])
def get_horarios(day):

    day = abs(int(day))
    today = datetime.now()
    mes_size = calendar.monthrange(today.year, today.month)
    datas: list[Agenda] = []

    if(day > 0 and day <= mes_size[1]):
        if(day == today.day and today.hour < 12):
            data = date(today.year, today.month, today.day)
            datas = Agenda.query.filter(
                Agenda.data == data, Agenda.hora > time(today.hour+1, today.minute)).all()
        else:
            mes = today.month
            if(day > today.day):
                data = date(today.year, mes, day)
            else:
                mes += 1
                ano = today.year
                if(mes == 1):
                    ano += 1
                data = date(ano, mes, day)

            datas = Agenda.query.filter(Agenda.data == data).all()

        horarios = [{"hora": data.hora, "id": data.id_data}
                    for data in datas if data.consultas == []]

        body = {"weekday": calendar.weekday(data.year, data.month, data.day)+1}
        body["data"] = data
        body["horarios"] = horarios

        return gen_response(200, **body)
    else:
        return gen_response(400, msg="Que mês é esse com esse dia?")
# END GET horarios by dia do mês#


#####################################  CONSULTA  #####################################
# POST cosulta #
@app.route("/consulta", methods=["POST"])
def post_consulta():
    body = request.get_json()

    try:
        id_clinica = int(body['id_clinica'])
        id_cliente = int(body['id_cliente'])
        id_data = int(body['id_data'])

        clinica: Clinica = Clinica.query.get(id_clinica)
        data: Agenda = Agenda.query.get(id_data)
        cliente: Cliente = Cliente.query.get(id_cliente)

        if(clinica and data and cliente and (data.consultas == [])):
            consulta = Consulta(id_cliente, id_clinica, id_data)
            db.session.add(consulta)
            db.session.commit()

            return gen_response(200, consulta=consulta.to_json(), msg="Consulta marcada com sucesso")
    except Exception as e:
        print('Error:', e)

    return gen_response(400, msg="Algo de errado não está certo")
# END POST cosulta #


# GET consultas #
@app.route("/consultas", methods=["GET"])
def get_consultas():
    consultas = Consulta.query.all()
    consultas_json = [consulta.to_json() for consulta in consultas]

    return gen_response(200, consultas=consultas_json)
# END GET consultas #


# GET consulta by ID#
@app.route("/consulta/<id>", methods=["GET"])
def get_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        consulta_json = consulta.to_json()

    return gen_response(200, consulta=consulta_json)
# END GET consulta by ID#

# DELETE consulta by ID#
@app.route("/consulta/<id>", methods=["DELETE"])
def delete_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        db.session.delete(consulta)
        consulta_json = consulta.to_json()
        db.session.commit()
        return gen_response(200, consulta=consulta_json)

    return gen_response(400, msg="A consulta não existe")
# END DELETE consulta by ID#



##################################### CLINICAS #######################################
# GET clinicas #
@app.route("/clinicas", methods=["GET"])
def get_clinicas():
    clinicas = Clinica.query.all()
    clinicas_json = [clinica.to_json() for clinica in clinicas]

    return gen_response(200, clinicas=clinicas_json)
# END GET clinicas #


# GET clinica by ID #
@app.route("/clinica/<id>", methods=["GET"])
def get_clinica(id):
    clinica_objeto = Clinica.query.get(id)
    clinica_json = clinica_objeto.to_json()

    return gen_response(200, clinica=clinica_json)
# END GET clinica by ID #


if(__name__ == "__main__"):
    app.run(debug=True, port=3000)
