from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Appointment, Acting, Patient, session, select, delete, update
from ..exceptions import APIException, ValidationException, AuthorizationException
from ..utils import useless_params
from ..constants import ResponseMessages, ValidationMessages
from ..validations import validate_payload
from ..middlewares import token_required

from ..docs import appointment_specs

PARAMETERS_FOR_POST_APPOINTMENT = [
    "complaint", "prescription", "scheduled_day", "start_time", "end_time",
    "patient_id", "acting_id"
]

PARAMETERS_FOR_GET_APPOINTMENT = [
    "acting_id", "patient_id", "limit", "page", "order_by"
]

PARAMETERS_FOR_PUT_APPOINTMENT = [
    "complaint", "prescription", "scheduled_day", "start_time", "end_time",
    "patient_id", "acting_id"
]

# POST appointment #


@bp_api.route("/appointments", methods=["POST"])
@swag_from(appointment_specs.post_appointment)
@token_required
def create_appointment(current_user):
    """
    Create a new appointment
    """
    body = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_APPOINTMENT)
    validate_payload(body, Appointment.validators)

    if session.query(Patient.id).filter(
            Patient.id == body["patient_id"]).first() is None:
        raise ValidationException({
            "patient_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "patient", body["patient_id"])
        })

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

    appointment = Appointment(**body)
    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return jsonify(appointment.as_json()), 201


# END POST appointment #

# GET appointments #


@bp_api.route("/appointments", methods=["GET"])
@swag_from(appointment_specs.get_appointments)
@token_required
def get_appointments(current_user):
    """
    Get appointments
    """
    params = request.args
    useless_params(params.keys(), PARAMETERS_FOR_GET_APPOINTMENT)

    page = int(params.get("page") or 1)
    limit = int(params.get("limit") or 20)
    acting_id = params.get("acting_id")
    patient_id = params.get("patient_id")

    stmt = select(Appointment).limit(limit).offset(
        (page - 1) * limit).order_by(desc(Appointment.created_at))

    if not current_user["admin"]:
        acting = session.query(Acting.id).filter(
            Acting.id == acting_id,
            Acting.professional_id == current_user["id"]).first()

        if acting is None:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    if acting_id is not None:
        stmt = stmt.filter(Appointment.acting_id == acting_id)
    if patient_id is not None:
        stmt = stmt.filter(Appointment.patient_id == patient_id)

    appointments = [p.as_json() for p in session.execute(stmt).scalars()]

    return jsonify(appointments), 200


@bp_api.route("/appointments/<int:appointment_id>", methods=["GET"])
@swag_from(appointment_specs.get_appointment_by_id)
@token_required
def get_appointment_by_id(current_user, appointment_id):
    """
    Get appointment by id
    """
    if not current_user["admin"]:
        has_permission = session.query(Appointment.id).join(Acting).filter(
            Appointment.id == appointment_id,
            Acting.professional_id == current_user["id"]).first()

        if not has_permission:
            raise AuthorizationException(ResponseMessages.NOT_AUHORIZED_ACCESS)

    appointment = session.get(Appointment, appointment_id)

    if appointment is None:
        raise APIException(
            ResponseMessages.ENTITY_NOT_FOUND.format("Appointment"),
            status_code=404)

    return jsonify(appointment.as_json())


# END GET appointments #

# PUT appointment #


@bp_api.route("/appointments/<int:appointment_id>", methods=["PUT"])
@swag_from(appointment_specs.update_appointment)
@token_required
def update_appointment(current_user, appointment_id):
    """
    Update appointment with id
    """
    body: dict[str, str] = request.get_json()

    useless_params(body.keys(), PARAMETERS_FOR_POST_APPOINTMENT)
    validate_payload(body, Appointment.validators)

    if session.query(Patient.id).filter(
            Patient.id == body["patient_id"]).first() is None:
        raise ValidationException({
            "patient_id":
            ValidationMessages.NO_ENTITY_RELATIONSHIP.format(
                "patient", body["patient_id"])
        })

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
            has_permission = session.query(Appointment.id).join(Acting).filter(
                Appointment.id == appointment_id,
                Acting.professional_id == current_user["id"]).first()

        if not has_permission:
            raise AuthorizationException(
                ResponseMessages.NOT_AUHORIZED_OPERATION)

    stmt = update(Appointment).where(Appointment.id == appointment_id).values(
        **body)
    rowcount = session.execute(stmt).rowcount
    session.commit()

    if not rowcount:
        raise APIException("Appointment no found", status_code=404)

    appointment = session.get(Appointment, appointment_id)

    return jsonify(appointment.as_json()), 200


# END PUT appointment #

# DELETE appointment #


@bp_api.route("/appointments/<int:appointment_id>", methods=["DELETE"])
@swag_from(appointment_specs.delete_appointment)
@token_required
def delete_appointment(current_user, appointment_id):
    """
    Delete appointment by id
    """
    if not current_user["admin"]:
        has_permission = session.query(Appointment.id).join(Acting).filter(
            Appointment.id == appointment_id,
            Acting.professional_id == current_user["id"]).first()

        if has_permission is None:
            raise AuthorizationException(
                ResponseMessages.NOT_AUHORIZED_OPERATION)

    stmt = delete(Appointment).where(Appointment.id == appointment_id)
    session.execute(stmt)
    session.commit()

    return "", 204


# END DELETE appointment #
