from flask import request, jsonify
from sqlalchemy import inspect
from flasgger import swag_from

from . import bp_api
from ..models import Schedule, Acting, Clinic, Professional, Specialty, session, select, delete, update
from ..exceptions import APIException, ValidationException, AuthorizationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload
from ..middlewares import token_required

from ..docs import schedule_specs

PARAMETERS_FOR_POST_SCHEDULE = [
    "start_date", "end_date", "start_time", "end_time", "max_visits",
    "week_day", "acting_id"
]

PARAMETERS_FOR_GET_SCHEDULE = [
    "acting_id", "limit", "page", "order_by", "professional_id", "clinic_id",
    "specialty_id"
]

PARAMETERS_FOR_PUT_SCHEDULE = [
    "start_date", "end_date", "start_time", "end_time", "max_visits",
    "week_day", "acting_id"
]

# POST schedule #
clinic_cols = (Clinic.id.label("clinic_id"), Clinic.name.label("clinic_name"))
professional_cols = (Professional.id.label("professional_id"),
                     Professional.name.label("professional_name"))
specialty_cols = (Specialty.id.label("specialty_id"),
                  Specialty.description.label("specialty_description"))

base_query = select(
    *inspect(Schedule).attrs, *clinic_cols, *professional_cols,
    *specialty_cols).join(Acting, Schedule.acting_id == Acting.id).join(
        Clinic, Acting.clinic_id == Clinic.id).join(
            Professional, Acting.professional_id == Professional.id).join(
                Specialty, Acting.specialty_id == Specialty.id)


@bp_api.route("/schedules", methods=["POST"])
@swag_from(schedule_specs.post_schedule)
@token_required
def create_schedule(current_user):
    """
    Create a new schedule
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_SCHEDULE)
    validate_payload(body, Schedule.validators)

    acting = session.query(Acting.id, Acting.professional_id).filter(Acting.id == body["acting_id"]).first()

    if acting is None:
        raise ValidationException({
            "acting_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "acting", body["acting_id"])
        })

    if not current_user["admin"] and acting.professional_id != current_user["id"]:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_OPERATION)

    schedule = Schedule(**body)
    session.add(schedule)
    session.commit()

    stmt = base_query.filter(Schedule.id == schedule.id)
    schedule = session.execute(stmt).first()
    return jsonify(schedule._asdict()), 201


# END POST schedule #

# GET schedules #


@bp_api.route("/schedules", methods=["GET"])
@swag_from(schedule_specs.get_schedules)
@token_required
def get_schedules(current_user):
    """
    Get schedules
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_SCHEDULE)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    acting_id = params.get("acting_id")
    clinic_id = params.get("clinic_id")
    professional_id = params.get("professional_id")
    specialty_id = params.get("specialty_id")

    stmt = base_query.limit(limit).offset(
        (page - 1) * limit).order_by(Schedule.week_day, Schedule.start_time)

    if acting_id is not None:
        stmt = stmt.filter(Schedule.acting_id == acting_id)
    if clinic_id is not None:
        stmt = stmt.filter(Clinic.id == professional_id)
    if professional_id is not None:
        stmt = stmt.filter(Professional.id == professional_id)
    if specialty_id is not None:
        stmt = stmt.filter(Specialty.id == specialty_id)

    schedules = []

    for sc in session.execute(stmt).all():
        schedules.append(sc._asdict())
        if not current_user[
                "id"] and sc["professional_id"] != current_user["id"]:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    return jsonify(schedules), 200


@bp_api.route("/schedules/<int:schedule_id>", methods=["GET"])
@swag_from(schedule_specs.get_schedule_by_id)
@token_required
def get_schedule_by_id(current_user, schedule_id):
    """
    Get schedule by id
    """
    stmt = base_query.filter(Schedule.id == schedule_id)
    schedule = session.execute(stmt).first()

    if schedule is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Schedule"),
            status_code=404)

    if not current_user["admin"]:
        if not schedule.professional_id == current_user["id"]:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    return jsonify(schedule._asdict())


# END GET schedules #

# PUT schedule #


@bp_api.route("/schedules/<int:schedule_id>", methods=["PUT"])
@swag_from(schedule_specs.update_schedule)
@token_required
def update_schedule(current_user, schedule_id):
    """
    Update schedule with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_SCHEDULE)
    validate_payload(body, Schedule.validators)

    acting = session.query(Acting.id, Acting.professional_id).filter(Acting.id == body["acting_id"]).first()

    if acting is None:
        raise ValidationException({
            "acting_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "acting", body["acting_id"])
        })

    if not current_user["admin"]:
        has_permission = acting.professional_id == current_user["id"]
        if has_permission:
            has_permission = session.query(Schedule.id).join(Acting).filter(
                Schedule.id == schedule_id,
                Acting.professional_id == current_user["id"]).first()

        if not has_permission:
            raise AuthorizationException(
                ResponseMessages.NOT_AUHORIZED_OPERATION)

    stmt = update(Schedule).where(Schedule.id == schedule_id).values(**body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Schedule no found", status_code=404)

    stmt = base_query.filter(Schedule.id == schedule_id)
    schedule = session.execute(stmt).first()
    return jsonify(schedule._asdict()), 200


# END PUT schedule #

# DELETE schedule #


@bp_api.route("/schedules/<int:schedule_id>", methods=["DELETE"])
@swag_from(schedule_specs.delete_schedule)
@token_required
def delete_schedule(current_user, schedule_id):
    """
    Delete schedule by id
    """
    if not current_user["admin"]:
        has_permission = session.query(Schedule.id).join(Acting).filter(
            Schedule.id == schedule_id,
            Acting.professional_id == current_user["id"]).first()

        if not has_permission:
            raise AuthorizationException(
                ResponseMessages.NOT_AUHORIZED_OPERATION)

    stmt = delete(Schedule).where(Schedule.id == schedule_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE schedule #
