from datetime import datetime, time, date, timedelta
import calendar

from dateutil.parser import isoparse
from flask import request, jsonify

from . import bp_api
from ..models import session, select, delete, result_to_json, Consulta, Cliente, Clinica, Horario
from ..exceptions import APIExceptionHandler
from ..utils import useless_params, valid_date_params

PARAMETERS_FOR_POST_CONSULTA = ["cliente_id", "clinica_id", "marcada", "descricao", "realizada"]
PARAMETERS_FOR_GET_CONSULTA = ["cliente_id", "clinica_id", "date_start", "date_end"]
PARAMETERS_FOR_PUT_CONSULTA = ["marcada", "realizada", "descricao"]

# POST cosulta #
@bp_api.route("/consulta", methods=["POST"])
def post_consulta():
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CONSULTA)

    detail = {}
    if "clinica_id" not in body:
        detail["clinica_id"] = "required"
    if "cliente_id" not in body:
        detail["cliente_id"] = "required"
    if "marcada" not in body:
        detail["marcada"] = "required"

    if detail:
        raise APIExceptionHandler("Required parameter is missing", detail=detail)
    try:
        cliente = session.execute(select(Cliente.id).where(Cliente.id == body["cliente_id"])).scalar()

        if cliente is None:
            raise APIExceptionHandler("cliente_id is not a id of a cliente", detail={"cliente_id": "invalid"})

        consulta = Consulta(**body)
        session.add(consulta)
        session.commit()

        session.refresh(consulta)

        return jsonify(status="success", data={"consulta": consulta._asjson()}), 201

    except APIExceptionHandler as e:
        raise e
    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

# END POST cosulta #


# GET consultas #
@bp_api.route("/consultas/<int:id>", methods=["GET"])
@bp_api.route("/consultas", methods=["GET"])
def get_consultas(id=None):
    params = request.args

    useless_params(params.keys(), PARAMETERS_FOR_GET_CONSULTA)

    clinica_id = params.get("clinica_id")
    cliente_id = params.get("cliente_id")
    date_start = params.get("date_start")
    date_end = params.get("date_end")

    if(clinica_id is not None):
        clinica = session.execute(select(Clinica.id, Clinica.nome, Clinica.tipo, Clinica.endereco, Clinica.telefone).where(Clinica.id == clinica_id)).first()

        if clinica is None:
            raise APIExceptionHandler("clinica_id is not a reference to a clinica",  detail={"clinica_id": "not found"}, status_code=404)
        clinica = clinica._asdict()

    if(cliente_id is not None):
        cliente = session.execute(select(Cliente.id, Cliente.nome, Cliente.telefone, Cliente.endereco).where(Cliente.id == cliente_id)).first()

        if cliente is None:
            raise APIExceptionHandler("cliente_id is not a reference to a cliente",  detail={"cliente_id": "not found"}, status_code=404)

        cliente = cliente._asdict()

    data = {}
    columns = (Consulta.id, Consulta.marcada, Consulta.realizada, Consulta.descricao, Consulta.duracao)
    cliente_columns = (Consulta.cliente_id, Cliente.nome.label("cliente_nome"), Cliente.sobrenome.label("cliente_sobrenome"), Cliente.telefone.label("cliente_telefone"), Cliente.cpf.label("cliente_cpf"),)
    clinica_columns = (Consulta.clinica_id, Clinica.nome.label("clinica_nome"), Clinica.tipo.label("clinica_tipo"),)

    if id is not None:

        try:
            stmt = select(*columns, *cliente_columns, *clinica_columns).join(Consulta.cliente).join(Consulta.clinica).where(Consulta.id == id)

            data["consulta"] = result_to_json(session.execute(stmt), first=True, marcada=lambda v: v.isoformat())

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

        if(data["consulta"] is None):
            raise APIExceptionHandler("id is not a reference to a consulta", detail={"id": "not found"}, payload={"id": id}, status_code=404)

    elif(clinica_id or cliente_id or date_start or date_end):

        date_start, date_end = valid_date_params(date_start=date_start, date_end=date_end)
        try:
            if(cliente_id and clinica_id):
                stmt = select(*columns).where(Consulta.clinica_id == clinica_id, Consulta.cliente_id == cliente_id)
                data["clinica"] = clinica
                data["cliente"] = cliente

            elif(clinica_id):
                stmt = select(*columns,  *cliente_columns).join(Consulta.cliente).where(Consulta.clinica_id == clinica_id)
                data["clinica"] = clinica

            elif(cliente_id):
                stmt = select(*columns, *clinica_columns).join(Consulta.clinica).where(Consulta.cliente_id == cliente_id)
                data["cliente"] = cliente

            else:
                stmt = select(*columns, *cliente_columns, *clinica_columns).join(Consulta.cliente).join(Consulta.clinica)

            if(date_start):
                stmt = stmt.where(Consulta.marcada >= date_start)
            if(date_end):
                stmt = stmt.where(Consulta.marcada <= date_end)

            data["consultas"] = result_to_json(session.execute(stmt), marcada=lambda v: v.isoformat())

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

    else:
        date_start = datetime.combine(date.today(), time(0))
        date_end =  datetime.combine(date_start.date() + timedelta(weeks=1), time.max)

        try:

            stmt = select(*columns, *cliente_columns, *clinica_columns).join(Consulta.cliente).join(Consulta.clinica).where(Consulta.marcada >= date_start, Consulta.marcada <= date_end)
            data["consultas"] = result_to_json(session.execute(stmt), marcada=lambda v: v.isoformat())

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

    return jsonify(status="success", data=data), 200

# END GET consultas #

# PUT consulta #
@bp_api.route("/consulta/<int:id>", methods=["PUT"])
def update_consulta(id):
    body = request.get_json()


    useless_params(body.keys(), PARAMETERS_FOR_PUT_CONSULTA)

    consulta = session.get(Consulta, id)
    if consulta is None:
        raise APIExceptionHandler("id is not a reference for a consulta", detail={"id": "not found"}, payload = {"id": id}, status_code=404)

    try:
        if body.get("marcada"):
            consulta.marcada = body["marcada"]
        if body.get("descricao"):
            consulta.descricao = body["descricao"]
        if body.get("realizada") is not None:
            consulta.realizada = body["realizada"]

        session.commit()
        session.refresh(consulta)
    except APIExceptionHandler as e:
        raise e
    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

    return jsonify(status="success", data={"consulta": consulta._asjson()}), 200
# END PUT consulta #

# DELETE consulta #
@bp_api.route("/consulta/<int:id>", methods=["DELETE"])
def delete_consulta(id):

    try:
        stmt = delete(Consulta).where(Consulta.id == id)

        rowcount = session.execute(stmt).rowcount

        session.commit()

    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

    if rowcount == 0:
        raise APIExceptionHandler("id is not a reference for a consulta", detail={"id": "not found"}, payload = {"id": id}, status_code=404)

    return jsonify(status="success", data=None), 200

# END DELETE consulta#

