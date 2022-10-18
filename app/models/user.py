from sqlalchemy import Column, String, CHAR
from sqlalchemy.orm import relationship

from . import db, TimestampMixin
from ..validations import Validator


class User(TimestampMixin, db.Model):

    __tablename__ = "users"
    name = Column(String(255), nullable=False)
    username = Column(String(45), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(CHAR(87), nullable=False)

    validators = {
        "name": Validator("name").required().length(2, 255),
        "username": Validator("username").required().length(5, 45),
        "email": Validator("email").required().email(),
        "password": Validator("password").required().length(6, 255),
    }
