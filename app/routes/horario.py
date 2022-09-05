from datetime import time, datetime
from dateutil.parser import isoparse

from flask import request, jsonify

from . import bp_api
from ..models import session, select, Horario, Consulta

# POST horario #


@bp_api.route("/horario", methods=["POST"])
def post_horario():
    """
    TODO
    """


# END POST horario #

# GET horarios #


@bp_api.route("/horarios", methods=["GET"])
def get_horarios():
    """
    TODO
    """
    clinica_id = request.args.get("clinica_id")

    data = {}
    data["horarios"] = []

    stmt = select(Horario).where(Horario.clinica_id == clinica_id)
    result = session.execute(stmt).scalars().all()

    for row in result:
        data["horarios"] += [row._asjson()]

    return jsonify(status="success", data=data), 200


@bp_api.route("/horarios/livres", methods=["GET"])
def get_horarios_livres():
    """
    TODO
    """
    consulta_dia = isoparse(request.args.get("consulta_dia"))
    clinica_id = request.args.get("clinica_id")

    data = {}
    data["horarios_livres"] = []
    consulta_dia_max = datetime.combine(date=consulta_dia.date(),
                                        time=time.max)

    stmt = select(Horario).where(Horario.clinica_id == clinica_id).where(
        Horario.dia_semana == consulta_dia.weekday())
    horario_dia = session.execute(stmt).scalar()

    consultas_marcadas = session.execute(
        select(Consulta.marcada).where(Consulta.marcada >= consulta_dia).where(
            Consulta.marcada <= consulta_dia_max).order_by(
                Consulta.marcada)).scalars().all()

    if horario_dia:
        intervalo = horario_dia.intervalo
        hora = datetime.combine(consulta_dia.date(), horario_dia.am_inicio)
        if horario_dia.almoco:
            am_fim = datetime.combine(consulta_dia.date(), horario_dia.am_fim)
            pm_inicio = datetime.combine(consulta_dia.date(),
                                         horario_dia.pm_inicio)

        pm_fim = datetime.combine(consulta_dia.date(), horario_dia.pm_fim)

        marcada = consultas_marcadas.pop(0) if consultas_marcadas else None
        while hora < pm_fim:
            if horario_dia.almoco and hora == am_fim:
                hora = pm_inicio
                continue
            if hora == marcada:
                marcada = consultas_marcadas.pop(
                    0) if consultas_marcadas else None
                hora += intervalo
                continue
            data["horarios_livres"].append(str(hora))
            hora += intervalo

    return jsonify(status="success", data=data), 200


# END GET horarios #

# PUT horario #


@bp_api.route("/horario/<int:id>", methods=["PUT"])
def put_horario():
    """
    TODO
    """


# END PUT horario #

# DELETE horario #


@bp_api.route("/horario", methods=["DELETE"])
def delete_horario():
    """
    TODO
    """


# END DELETE horario #
