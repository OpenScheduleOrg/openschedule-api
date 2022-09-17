from datetime import time, datetime
from dateutil.parser import isoparse
from dateutil.relativedelta import relativedelta

from flask import request, jsonify

from . import bp_api
from ..models import session, select, Horario, Consulta

# POST horario #


@bp_api.route("/horarios", methods=["POST"])
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

    horarios_livres = []
    consulta_dia_max = datetime.combine(date=consulta_dia.date(),
                                        time=time.max)

    horario_dia = session.execute(
        select(Horario).where(Horario.clinica_id == clinica_id).where(
            Horario.dia_semana == consulta_dia.weekday())).scalar()

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
        now = datetime.now() + relativedelta(hours=2)
        while hora < pm_fim:
            if horario_dia.almoco and hora == am_fim:
                hora = pm_inicio
                continue
            if hora == marcada:
                marcada = consultas_marcadas.pop(
                    0) if consultas_marcadas else None
                hora += intervalo
                continue
            if hora > now:
                horarios_livres.append(str(hora))
            hora += intervalo

    return jsonify(status="success", data={"horarios_livres":
                                           horarios_livres}), 200


@bp_api.route("/horarios/dias/livres", methods=["GET"])
def get_dias_livres():
    """
    TODO
    """
    mes = int(request.args.get("month"))
    clinica_id = request.args.get("clinica_id")

    dias = []
    hoje = datetime.now()

    horarios_result = session.execute(
        select(Horario).where(Horario.clinica_id == clinica_id).order_by(
            Horario.dia_semana)).scalars().all()

    horarios = {}
    for horario in horarios_result:
        horarios[horario.dia_semana] = horario

    current = datetime.now() + relativedelta(hours=2)
    if current.month != mes:
        current = datetime(hoje.year + 1 if hoje.month > mes else hoje.year,
                           mes, 1)

    proximo_mes = datetime(current.year, current.month,
                           1) + relativedelta(months=1)

    consultas = session.execute(
        select(Consulta.marcada).where(Consulta.marcada >= current).where(
            Consulta.marcada < proximo_mes).order_by(
                Consulta.marcada)).scalars().all()

    current_consulta = consultas.pop(0) if consultas else None

    if current.month == mes:
        horario = horarios.get(current.weekday())
        if horario:
            current_horario = datetime.combine(current.date(),
                                               horario.am_inicio)

            while current_horario.time() < horario.pm_fim:
                if current_horario > current:
                    current = current_horario
                    break

                next_horario = current_horario + horario.intervalo
                if horario.almoco and (
                        next_horario.time() >= horario.am_fim
                        and next_horario.time() < horario.pm_inicio):
                    current_horario = datetime.combine(current_horario.date(),
                                                       horario.pm_inicio)
                    continue
                current_horario = next_horario

            # Verifica se existe algum horario livre no dia
            while current_horario.time() < horario.pm_fim:
                if not current_consulta or current_consulta > (
                        current_horario + horario.intervalo):
                    dias.append(current.day)
                    break
                current_consulta = consultas.pop(0) if consultas else None

                next_horario = current_horario + horario.intervalo
                if horario.almoco and (
                        next_horario.time() >= horario.am_fim
                        and next_horario.time() < horario.pm_inicio):
                    current_horario = datetime.combine(current_horario.date(),
                                                       horario.pm_inicio)
                    continue
                current_horario = next_horario

            while current_consulta and current_consulta.day == current.day:
                current_consulta = consultas.pop(0) if consultas else None

            current = datetime.combine(current.date(), time(
                0, 0)) + relativedelta(days=1)

    while current < proximo_mes:
        horario = horarios.get(current.weekday())
        if horario:
            current_horario = datetime.combine(current.date(),
                                               horario.am_inicio)
            while current_horario.time() < horario.pm_fim:
                if not current_consulta or current_consulta > (
                        current_horario + horario.intervalo):
                    dias.append(current.day)
                    break
                current_consulta = consultas.pop(0) if consultas else None

                next_horario = current_horario + horario.intervalo
                if horario.almoco and (
                        next_horario.time() >= horario.am_fim
                        and next_horario.time() < horario.pm_inicio):
                    current_horario = datetime.combine(current_horario.date(),
                                                       horario.pm_inicio)
                    continue
                current_horario = next_horario

        while current_consulta and current_consulta.day == current.day:
            current_consulta = consultas.pop(0) if consultas else None
        current = current + relativedelta(days=1)

    return jsonify(status="success", data={"dias": dias}), 200


# END GET horarios #

# PUT horario #


@bp_api.route("/horarios/<int:id>", methods=["PUT"])
def put_horario():
    """
    TODO
    """


# END PUT horario #

# DELETE horario #


@bp_api.route("/horarios", methods=["DELETE"])
def delete_horario():
    """
    TODO
    """


# END DELETE horario #
