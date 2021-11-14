from datetime import datetime, time, date, timedelta, timezone
import calendar

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from . import api
from ..models import db, Consulta, Cliente, Clinica, Horario
from ..common.exc import APIExceptionHandler

PARAMETERS_FOR_GET_CONSULTA = ["id_cliente", "id_clinica", "date_start", "date_end"]

# POST cosulta #
@api.route("/consulta", methods=["POST"])
def post_consulta():
    body = request.get_json()
    detail_error = {}

    if "id_clinica" not in body:
        detail_error["id_clinica"] = "required"
    if "id_cliente" not in body:
        detail_error["id_cliente"] = "required"
    if "marcada" not in body:
        detail_error["marcada"] = "required"

    if len(detail_error):
        raise APIExceptionHandler("Required parameter is missing", detail=detail_error)
    try:
        cliente = Cliente.query.get(body["id_cliente"])

        if cliente is None:
            raise APIExceptionHandler("id_cliente is not a id of a cliente", detail={"id_cliente": "invalid"})

        consulta = Consulta(**body)
        db.session.add(consulta)
        db.session.commit()

        db.session.refresh(consulta)

        return jsonify(status="success", data={"consulta": consulta._asjson()}), 201

    except APIExceptionHandler as e:
        raise e
    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

# END POST cosulta #


# GET consultas #
@api.route("/consultas", methods=["GET"])
def get_consultas():

    def isoformat_datetime(**kw):
        detail = {}
        converted = []

        for key, value in kw.items():
            if(value is None):
                converted.append(None)
                continue
            try:
                converted.append(datetime.fromisoformat(value))
            except ValueError as e:
                detail[key] = "invalid"
            except Exception as e:
                raise e

        if len(detail.keys()):
            raise APIExceptionHandler("Date and time are not in iso format", detail=detail)

        if((isinstance(converted[0], datetime) and isinstance(converted[1], datetime)) and converted[0] > converted[1]):
                raise APIExceptionHandler("Invalid datetime values date_start < date_end", detail={"date_start": "invalid", "date_end":"invalid"})

        return converted

    detail = {}
    for key in request.args.keys():
        if key not in PARAMETERS_FOR_GET_CONSULTA:
            detail[key] = "unusable"

    if len(detail.keys()):
        raise APIExceptionHandler("Request have parameters worthless", detail=detail, status_code=406)

    id_clinica = request.args.get("id_clinica")
    id_cliente = request.args.get("id_cliente")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")

    if(id_clinica):
        clinica = Clinica.query.get(id_clinica)

        if clinica is None:
            raise APIExceptionHandler("id_clinica is not a reference to a clinica",  detail={"id_clinica": "not found"})
    if(id_cliente):
        cliente = Cliente.query.get(id_cliente)

        if cliente is None:
            raise APIExceptionHandler("id_cliente is not a reference to a cliente",  detail={"id_cliente": "not found"})

    data = {}

    if(id_clinica and id_cliente):

        date_start, date_end = isoformat_datetime(date_start=date_start, date_end=date_end)

        try:

            consultas = Consulta.query.filter_by(id_clinica=id_clinica, id_cliente=id_cliente)

            if(date_start):
                consultas = consultas.filter(Consulta.marcada >= date_start)
            if(date_end):
                consultas = consultas.filter(Consulta.marcada <= date_end)

            consultas = consultas.all()

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

        data["consultas"] = [c._asjson() for c in consultas]


    elif(id_clinica):

        date_start, date_end = isoformat_datetime(date_start=date_start, date_end=date_end)

        try:

            consultas = Consulta.query.filter_by(id_clinica=id_clinica)

            if(date_start):
                consultas = consultas.filter(Consulta.marcada >= date_start)
            if(date_end):
                consultas = consultas.filter(Consulta.marcada <= date_end)

            consultas = consultas.all()

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

        data["consultas"] = [c._asjson() for c in consultas]

    elif(id_cliente):

        date_start, date_end = isoformat_datetime(date_start=date_start, date_end=date_end)

        try:
            consultas = Consulta.query.filter_by(id_cliente=id_cliente)

            if(date_start):
                consultas = consultas.filter(Consulta.marcada >= date_start)
            if(date_end):
                consultas = consultas.filter(Consulta.marcada <= date_end)

            consultas = consultas.all()

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)


        data["consultas"] = [c._asjson() for c in consultas]

    elif(date_start or date_end):

        date_start, date_end = isoformat_datetime(date_start=date_start, date_end=date_end)

        try:
            consultas = Consulta.query

            if(date_start):
                consultas = consultas.filter(Consulta.marcada >= date_start)
            if(date_end):
                consultas = consultas.filter(Consulta.marcada <= date_end)

            consultas = consultas.all()

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)


        data["consultas"] = [c._asjson() for c in consultas]
    else:
        date_start = datetime.combine(date.today(), time(0), tzinfo=timezone.utc)
        date_end =  datetime.combine(date_start.date() + timedelta(weeks=1), time.max, tzinfo=timezone.utc)

        try:
            consultas = Consulta.query.filter(Consulta.marcada >= date_start).filter(Consulta.marcada <= date_end).all()

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)


        data["consultas"] = [c._asjson() for c in consultas]

    return jsonify(status="success", data=data), 200

# END GET consultas #


# GET consulta by ID#
@api.route("/consulta/<int:id>", methods=["GET"])
def get_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        consulta_json = consulta._asdict()

    return jsonify(consulta=consulta_json), 200
# END GET consulta by ID#

# DELETE consulta by ID#
@api.route("/consulta/<id>", methods=["DELETE"])
def delete_consulta(id):
    consulta_json = {}
    consulta = Consulta.query.get(id)
    if(consulta):
        db.session.delete(consulta)
        consulta_json = consulta._asdict()
        db.session.commit()
        return jsonify(consulta=consulta_json), 200

    return jsonify(msg="A consulta não existe"), 400
# END DELETE consulta by ID#

