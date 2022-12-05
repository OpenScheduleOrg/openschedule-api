from flask import request, jsonify
from sqlalchemy import desc
from flasgger import swag_from

from . import bp_api
from ..models import Appointment, Acting, Patient, Clinic, Specialty, Professional, Schedule, session, select, delete, update
from ..exceptions import APIException
from ..utils import useless_params
from ..constants import ResponseMessages
from ..validations import validate_payload
from ..middlewares import token_required, only_admin

from ..docs import calendar_specs

SPECIALTY_FIELDS = (
    Specialty.id,
    Specialty.description,
)


@bp_api.route("/calendar/specialties", methods=["GET"])
@swag_from(calendar_specs.get_specialties_availables)
@token_required
def get_specialties_availables(_):
    """
    Obtain clinic specialties with available schedules
    """
    params = request.args
    clinic_id = int(params.get("clinic_id"))

    stmt = select(SPECIALTY_FIELDS).distinct().join(
        Acting, Acting.specialty_id == Specialty.id).join(
            Schedule, Acting.id == Schedule.acting_id).where(
                Acting.clinic_id == clinic_id,
                Schedule.max_visits > 0).order_by(desc(Specialty.description))

    specialties = [p._asdict() for p in session.execute(stmt).all()]

    return jsonify(specialties), 200
