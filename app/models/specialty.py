from sqlalchemy import Column, String

from . import db, TimestampMixin
from ..validations import Validator


class Specialty(TimestampMixin, db.Model):

    __tablename__ = "specialties"
    description = Column(String(255), nullable=False)

    validators = {
        "description": Validator("description").required().length(4, 255),
    }
