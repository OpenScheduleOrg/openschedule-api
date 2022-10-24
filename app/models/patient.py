from sqlalchemy import Column, Date, String, CHAR
from sqlalchemy.orm import relationship

from . import db, TimestampMixin
from ..validations import Validator


class Patient(TimestampMixin, db.Model):

    __tablename__ = "patients"
    name = Column(String(255), nullable=False)
    cpf = Column(CHAR(11), nullable=False, unique=True)
    phone = Column(CHAR(10), nullable=False, unique=True)
    address = Column(String(255), default=None)
    birthdate = Column(Date, default=None)

    validators = {
        "name": Validator("name").required().length(2, 255),
        "cpf": Validator("cpf").required().cpf(),
        "phone": Validator("phone").required().phone(),
        "birthdate": Validator("birthdate").date(),
    }
