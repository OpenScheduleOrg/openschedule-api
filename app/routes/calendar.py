from datetime import timedelta

from flask import request, jsonify
from sqlalchemy import desc, func, inspect
from flasgger import swag_from

from . import bp_api
from ..models import Appointment, Acting, Specialty, Professional, Schedule, session, select
from ..middlewares import token_required
from ..validations import Validator, validate_payload

from ..docs import calendar_specs

#  Validators  #

validators = {
    "clinic_id": Validator("clinic_id").required().number(),
    "specialty_id": Validator("specialty_id").required().number(),
    "num_days": Validator("num_days").number(),
    "first_day_startime": Validator("first_day_startime").number(),
    "start_date": Validator("start_date").date(),
    "day": Validator("day").date(),
}

#  END Validators  #

SPECIALTY_FIELDS = inspect(Specialty).attrs

SCHEDULE_FIELDS = (
    *inspect(Schedule).attrs,
    Professional.id.label("professional_id"),
    Professional.name.label("professional_name"),
    Specialty.id.label("specialty_id"),
    Specialty.description.label("specialty_description"),
)

# QUERIES #

COUNT_APPOINTMENTS = select(func.count(Appointment.id)).where(
    Appointment.start_time >= Schedule.start_time,
    Appointment.start_time < Schedule.end_time,
    Appointment.acting_id == Acting.id)

# QUERIES #


@bp_api.route("/calendar/specialties", methods=["GET"])
@swag_from(calendar_specs.get_specialties_availables)
@token_required
def get_specialties_availables(_):
    """
    Obtain clinic specialties with available schedules
    """
    params = {**request.args}
    validate_payload(params, validators, ["clinic_id"])

    clinic_id = params.get("clinic_id")

    stmt = select(SPECIALTY_FIELDS).distinct().join(
        Acting, Acting.specialty_id == Specialty.id).join(
            Schedule, Acting.id == Schedule.acting_id).where(
                Acting.clinic_id == clinic_id,
                Schedule.max_visits > 0).order_by(desc(Specialty.description))

    specialties = [p._asdict() for p in session.execute(stmt).all()]

    return jsonify(specialties), 200


@bp_api.route("/calendar/free/days", methods=["GET"])
@swag_from(calendar_specs.get_free_days)
@token_required
def get_free_days(_):
    """
    Return next x days with availables schedules
    """
    params = {**request.args}
    validate_payload(params, validators)

    clinic_id = params.get("clinic_id")
    specialty_id = params.get("specialty_id")
    num_days = params.get("num_days") or 10
    start_date = params.get("start_date")
    first_day_startime = params.get("first_day_startime") or 0

    free_days = []

    stmt = select(Schedule.week_day).distinct().join(
        Acting, Acting.id == Schedule.acting_id).where(
            Acting.clinic_id == clinic_id,
            Acting.specialty_id == specialty_id).order_by(Schedule.week_day)

    week_days = list(session.execute(stmt).scalars())
    base_stmt = select(Schedule.id).join(
        Acting, Acting.id == Schedule.acting_id).where(
            Acting.clinic_id == clinic_id, Acting.specialty_id == specialty_id)

    if start_date.weekday() in week_days:
        stmt = base_stmt.where(
            Schedule.week_day == start_date.weekday(),
            Schedule.start_time > first_day_startime,
            Schedule.max_visits > COUNT_APPOINTMENTS.where(
                Appointment.scheduled_day == start_date).scalar_subquery())

        if session.execute(stmt).first():
            free_days.append(start_date)
            num_days -= 1

    current_date = start_date
    while week_days and num_days > 0:
        current_date = current_date + timedelta(days=1)
        if current_date.weekday() not in week_days:
            continue
        stmt = base_stmt.where(
            Schedule.week_day == current_date.weekday(),
            Schedule.max_visits > COUNT_APPOINTMENTS.where(
                Appointment.scheduled_day == current_date).scalar_subquery())

        if session.execute(stmt).first():
            free_days.append(current_date)
            num_days -= 1

    return jsonify(free_days), 200


@bp_api.route("/calendar/available/schedules", methods=["GET"])
@swag_from(calendar_specs.get_available_schedules)
@token_required
def get_available_schedules(_):
    """
    Return available schedules in day
    """
    params = {**request.args}
    validate_payload(params, validators, ["specialty_id", "day"])

    clinic_id = params.get("clinic_id")
    specialty_id = params.get("specialty_id")
    day = params.get("day")

    stmt = select(SCHEDULE_FIELDS).distinct().join(
        Acting, Acting.id == Schedule.acting_id).join(
            Professional, Acting.professional_id == Professional.id).join(
                Specialty, Acting.specialty_id == Specialty.id).where(
                    Acting.clinic_id == clinic_id,
                    Acting.specialty_id == specialty_id,
                    Schedule.week_day == day.weekday(),
                    Schedule.max_visits > COUNT_APPOINTMENTS.where(
                        Appointment.scheduled_day == day).scalar_subquery())

    free_schedules = [sc._asdict() for sc in session.execute(stmt).all()]

    return jsonify(free_schedules), 200
