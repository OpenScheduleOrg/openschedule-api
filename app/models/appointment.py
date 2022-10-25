from sqlalchemy import Column, ForeignKey, Text, SmallInteger, Integer, Date

from . import db, TimestampMixin
from ..validations import Validator


class Appointment(TimestampMixin, db.Model):
    __tablename__ = "appointments"

    complaint = Column(Text)
    prescription = Column(Text)
    scheduled_day = Column(Date, nullable=False)
    start_time = Column(SmallInteger, nullable=False)
    end_time = Column(SmallInteger)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    acting_id = Column(Integer, ForeignKey('actuations.id'), nullable=False)

    validators = {
        "scheduled_day": Validator("scheduled_day").required().date(),
        "start_time": Validator("start_time").required().number(),
        "end_time": Validator("end_time").number(),
        "patient_id": Validator("patient_id").required(),
        "acting_id": Validator("acting_id").number()
    }
