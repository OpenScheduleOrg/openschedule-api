from sqlalchemy import Column, String, CHAR, Integer, ForeignKey

from . import db, TimestampMixin
from ..validations import Validator


class User(TimestampMixin, db.Model):

    __tablename__ = "users"
    name = Column(String(255), nullable=False)
    username = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(CHAR(87))
    picture = Column(String(255))

    clinic_id = Column(Integer, ForeignKey('clinics.id'), nullable=False)

    validators = {
        "name": Validator("name").required().length(2, 255),
        "username": Validator("username").required().length(5, 45),
        "email": Validator("email").required().email(),
        "password": Validator("password").length(6, 255),
        "clinic_id": Validator("clinic_id").required().number(),
    }

    validators_update = {
        "name": Validator("name").length(2, 255),
        "username": Validator("username").length(5, 45),
        "email": Validator("email").email(),
        "password": Validator("password").length(6, 255),
        "clinic_id": Validator("clinic_id").number(),
    }
