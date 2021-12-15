import re
from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify

from . import bp_api
from ..models import Cliente, session, select
from ..exceptions import APIExceptionHandler
from ..utils import useless_params

PARAMETERS_FOR_POST_CLIENTE = ["nome", "sobrenome", "cpf", "telefone", "nascimento", "endereco"]
PARAMETERS_FOR_GET_CLIENTE = ["nome", "sobrenome", "cpf", "telefone", "nascimento", "endereco", "search"]

# POST cliente #
@bp_api.route("/cliente", methods=["POST"])
def post_cliente():
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CLIENTE)

    detail = {}
    if "nome" not in body:
        detail["nome"] = "required"
    if "cpf" not in body:
        detail["cpf"] = "required"
    if "telefone" not in body:
        detail["telefone"] = "required"

    if detail:
        raise APIExceptionHandler("Required parameter is missing", detail=detail)
    try:
        cliente = Cliente(**body)
        session.add(cliente)
        session.commit()

        session.refresh(cliente)

        return jsonify(status="success", data={"cliente": cliente._asjson()}), 201

    except APIExceptionHandler as e:
        raise e
    except Exception as e:
        raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)



# END POST cliente #

# GET clientes #
@bp_api.route("/clientes", methods=["GET"])
@bp_api.route("/clientes/<int:id>", methods=["GET"])
def get_clientes(id=None):
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_CLIENTE)

    data = {}

    nome = params.get("nome")
    sobrenome = params.get("sobrenome")
    cpf = params.get("cpf")
    telefone = params.get("telefone")
    nascimento = params.get("nascimento")
    endereco = params.get("endereco")
    search = params.get("search")

    cliente = None
    one = False

    if id:
        one = True
        try:
            cliente = session.get(Cliente, id)

        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)
        if(cliente):
            data["cliente"] = cliente._asjson()
        else: return jsonify(status="fail", message="cliente not found", data=None, status_code=404)

    elif cpf:
        one = True
        try:
            pass
        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)

    elif telefone:
        one = True
        try:
            stmt = select(Cliente).filter_by(telefone=telefone)
            cliente = session.execute(stmt).scalar()
        except Exception as e:
            raise APIExceptionHandler(str(getattr(e, "orig", None) or str(e)), status="error", status_code=500)


    if(cliente):
        data["cliente"] = cliente._asjson()
    elif(one): return jsonify(status="fail", message="cliente not found", data=None, status_code=404)

    return jsonify(status="success", data=data), 200
# END GET clientes #

# PUT cliente #
@bp_api.route("/cliente/<int:id>", methods=["PUT"])
def put_cliente(id):
    pass
# END PUT cliente #

# DELETE cliente #
@bp_api.route("/cliente", methods=["DELETE"])
def delete_cliente():
    pass
# END DELETE cliente #


