from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Schedule, Acting, session, select, delete, update
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

PARAMETERS_FOR_GET_SCHEDULE = ["acting_id", "limit", "page", "order_by"]

PARAMETERS_FOR_PUT_SCHEDULE = [
    "start_date", "end_date", "start_time", "end_time", "max_visits",
    "week_day", "acting_id"
]

# POST schedule #


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

    acting = session.query(
        Acting.id,
        Acting.professional_id).filter(Acting.id == body["acting_id"]).first()

    if acting is None:
        raise ValidationException({
            "acting_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "acting", body["acting_id"])
        })

    if not current_user[
            "admin"] and acting["professional_id"] != current_user["id"]:
        raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_OPERATION)

    schedule = Schedule(**body)
    session.add(schedule)
    session.commit()
    session.refresh(schedule)

    return jsonify(schedule.as_json()), 201


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

    stmt = select(Schedule).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Schedule.created_at))

    if not current_user["admin"]:
        acting = session.query(Acting.id).filter(
            Acting.id == acting_id,
            Acting.professional_id == current_user["id"]).first()

        if acting is None:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    if acting_id is not None:
        stmt = stmt.filter(Schedule.acting_id == acting_id)

    schedules = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(schedules), 200


@bp_api.route("/schedules/<int:schedule_id>", methods=["GET"])
@swag_from(schedule_specs.get_schedule_by_id)
@token_required
def get_schedule_by_id(current_user, schedule_id):
    """
    Get schedule by id
    """
    if not current_user["admin"]:
        has_permission = session.query(Schedule.id).join(Acting).filter(
            Schedule.id == schedule_id,
            Acting.professional_id == current_user["id"]).first()

        if not has_permission:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    schedule = session.get(Schedule, schedule_id)

    if schedule is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Schedule"),
            status_code=404)

    return jsonify(schedule.as_json())


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

    acting = session.query(
        Acting.id,
        Acting.professional_id).filter(Acting.id == body["acting_id"]).first()

    if acting is None:
        raise ValidationException({
            "acting_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "acting", body["acting_id"])
        })

    if not current_user["admin"]:
        has_permission = acting["professional_id"] == current_user["id"]
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

    schedule = session.get(Schedule, schedule_id)

    return jsonify(schedule.as_json()), 200


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
