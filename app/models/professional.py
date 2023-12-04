from sqlalchemy import Column, String, CHAR

from . import db, TimestampMixin
from ..validations import Validator


class Professional(TimestampMixin, db.Model):

    __tablename__ = "professionals"
    name = Column(String(255), nullable=False)
    phone = Column(CHAR(10), nullable=False, unique=True)
    reg_number = Column(String(40))
    username = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(CHAR(87))

    validators = {
        "name": Validator("name").required().length(2, 255),
        "phone": Validator("phone").required().phone(),
        "reg_number": Validator("reg_number"),
        "username": Validator("username").required().length(5, 45),
        "email": Validator("email").required().email(),
        "password": Validator("password").length(6, 255),
    }

    validators_update = {
        **validators,
        "password": Validator("password").length(6, 255),
    }
