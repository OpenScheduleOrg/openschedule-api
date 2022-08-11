from datetime import datetime, time, date, timedelta

from flask import request, jsonify

from . import bp_api
from ..models import session, select, delete, result_to_json, Consulta, Patient, Clinica
from ..exceptions import APIException
from ..utils import useless_params
from ..validations import validate_dates

PARAMETERS_FOR_POST_CONSULTA = [
    "patient_id", "clinica_id", "marcada", "descricao", "realizada"
]
PARAMETERS_FOR_GET_CONSULTA = [
    "patient_id", "clinica_id", "date_start", "date_end"
]
PARAMETERS_FOR_PUT_CONSULTA = ["marcada", "realizada", "descricao"]

# POST cosulta #


@bp_api.route("/consulta", methods=["POST"])
def post_consulta():
    """
    post consulta
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_CONSULTA)

    detail = {}
    if "clinica_id" not in body:
        detail["clinica_id"] = "required"
    if "patient_id" not in body:
        detail["patient_id"] = "required"
    if "marcada" not in body:
        detail["marcada"] = "required"

    if detail:
        raise APIException("Required parameter is missing", detail=detail)
    try:
        patient = session.execute(
            select(
                Patient.id).where(Patient.id == body["patient_id"])).scalar()

        if patient is None:
            raise APIException("patient_id is not a id of a patient",
                               detail={"patient_id": "invalid"})

        consulta = Consulta(**body)
        session.add(consulta)
        session.commit()

        session.refresh(consulta)

        return jsonify(status="success", data={"consulta":
                                               consulta.as_json()}), 201

    except APIException as e:
        raise e
    except Exception as e:
        raise APIException(str(getattr(e, "orig", None) or str(e)),
                           status="error",
                           status_code=500) from e


# END POST cosulta #


# GET consultas #
@bp_api.route("/consultas/<int:consulta_id>", methods=["GET"])
@bp_api.route("/consultas", methods=["GET"])
def get_consultas(consulta_id=None):
    """
    Get consultas
    """
    params = request.args

    useless_params(params.keys(), PARAMETERS_FOR_GET_CONSULTA)

    clinica_id = params.get("clinica_id")
    patient_id = params.get("patient_id")
    date_start = params.get("date_start")
    date_end = params.get("date_end")

    if clinica_id is not None:
        clinica = session.execute(
            select(Clinica.id, Clinica.nome, Clinica.tipo, Clinica.endereco,
                   Clinica.telefone).where(Clinica.id == clinica_id)).first()

        if clinica is None:
            raise APIException("clinica_id is not a reference to a clinica",
                               detail={"clinica_id": "not found"},
                               status_code=404)
        clinica = clinica._asdict()

    if patient_id is not None:
        patient = session.execute(
            select(Patient.id, Patient.nome, Patient.telefone,
                   Patient.endereco).where(Patient.id == patient_id)).first()

        if patient is None:
            raise APIException("patient_id is not a reference to a patient",
                               detail={"patient_id": "not found"},
                               status_code=404)
        patient = patient._asdict()

    data = {}
    columns = (Consulta.id, Consulta.marcada, Consulta.realizada,
               Consulta.descricao, Consulta.duracao)
    patient_columns = (
        Consulta.patient_id,
        Patient.name.label("patient_name"),
        Patient.phone.label("patient_phone"),
        Patient.cpf.label("patient_cpf"),
    )
    clinica_columns = (
        Consulta.clinica_id,
        Clinica.nome.label("clinica_nome"),
        Clinica.tipo.label("clinica_tipo"),
    )

    if consulta_id is not None:

        try:
            stmt = select(*columns, *patient_columns, *clinica_columns).join(
                Consulta.patient).join(
                    Consulta.clinica).where(Consulta.id == consulta_id)

            data["consulta"] = result_to_json(session.execute(stmt),
                                              first=True,
                                              marcada=lambda v: v.isoformat())

        except Exception as e:
            raise APIException(str(getattr(e, "orig", None) or str(e)),
                               status="error",
                               status_code=500) from e

        if data["consulta"] is None:
            raise APIException("id is not a reference to a consulta",
                               detail={"id": "not found"},
                               payload={"id": consulta_id},
                               status_code=404)

    elif (clinica_id or patient_id or date_start or date_end):

        if date_start and date_end:
            date_start, date_end, *_ = validate_dates(date_start=date_start,
                                                      date_end=date_end)
        try:
            if patient_id and clinica_id:
                stmt = select(*columns).where(
                    Consulta.clinica_id == clinica_id,
                    Consulta.patient_id == patient_id)
                data["clinica"] = clinica
                data["patient"] = patient

            elif clinica_id:
                stmt = select(*columns, *patient_columns).join(
                    Consulta.patient).where(Consulta.clinica_id == clinica_id)
                data["clinica"] = clinica

            elif patient_id:
                stmt = select(*columns, *clinica_columns).join(
                    Consulta.clinica).where(Consulta.patient_id == patient_id)
                data["patient"] = patient

            else:
                stmt = select(*columns, *patient_columns,
                              *clinica_columns).join(Consulta.patient).join(
                                  Consulta.clinica)

            if date_start:
                stmt = stmt.where(Consulta.marcada >= date_start)
            if date_end:
                stmt = stmt.where(Consulta.marcada <= date_end)

            data["consultas"] = result_to_json(session.execute(stmt),
                                               marcada=lambda v: v.isoformat())
        except Exception as e:
            raise APIException(str(getattr(e, "orig", None) or str(e)),
                               status="error",
                               status_code=500) from e

    else:
        date_start = datetime.combine(date.today(), time(0))
        date_end = datetime.combine(date_start.date() + timedelta(weeks=1),
                                    time.max)

        try:

            stmt = select(*columns, *patient_columns, *clinica_columns).join(
                Consulta.patient).join(Consulta.clinica).where(
                    Consulta.marcada >= date_start,
                    Consulta.marcada <= date_end)
            data["consultas"] = result_to_json(session.execute(stmt),
                                               marcada=lambda v: v.isoformat())

        except Exception as e:
            raise APIException(str(getattr(e, "orig", None) or str(e)),
                               status="error",
                               status_code=500) from e

    return jsonify(status="success", data=data), 200


# END GET consultas #

# PUT consulta #


@bp_api.route("/consultas/<int:consulta_id>", methods=["PUT"])
def put_consulta(consulta_id):
    """
    update consulta
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_PUT_CONSULTA)

    consulta = session.get(Consulta, consulta_id)
    if consulta is None:
        raise APIException("id is not a reference for a consulta",
                           detail={"id": "not found"},
                           payload={"id": consulta_id},
                           status_code=404)

    try:
        if body.get("marcada"):
            consulta.marcada = body["marcada"]
        if body.get("descricao"):
            consulta.descricao = body["descricao"]
        if body.get("realizada") is not None:
            consulta.realizada = body["realizada"]

        session.commit()
        session.refresh(consulta)
    except APIException as e:
        raise e
    except Exception as e:
        raise APIException(str(getattr(e, "orig", None) or str(e)),
                           status="error",
                           status_code=500) from e

    return jsonify(status="success", data={"consulta":
                                           consulta.as_json()}), 200


# END PUT consulta #

# DELETE consulta #


@bp_api.route("/consultas/<int:id>", methods=["DELETE"])
def delete_consulta(consulta_id):
    """
    delete consulta
    """
    try:
        stmt = delete(Consulta).where(Consulta.id == consulta_id)

        rowcount = session.execute(stmt).rowcount

        session.commit()
    except Exception as e:
        raise APIException(str(getattr(e, "orig", None) or str(e)),
                           status="error",
                           status_code=500) from e
    if rowcount == 0:
        raise APIException("id is not a reference for a consulta",
                           detail={"id": "not found"},
                           payload={"id": consulta_id},
                           status_code=404)

    return jsonify(status="success", data=None), 200


# END DELETE consulta#
