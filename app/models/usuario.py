import re

from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship, validates

from flask import current_app
from passlib.hash import bcrypt

from . import db, TimestampMixin
from ..exceptions import APIException
from ..auth import AccessLevel


class Usuario(TimestampMixin, db.Model):
    __tablename__ = "usuario"

    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    foto = Column(String(255), nullable=True)
    nivel_acesso = Column(Enum(AccessLevel), nullable=False)
    username = Column(String(10), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    clinica_id = Column(Integer, ForeignKey('clinica.id'))

    clinica = relationship("Clinica", back_populates="usuarios")

    @validates("username")
    def valida_username(self, key, username):
        """
        validate password and encrypt password
        """
        if not username:
            raise APIException("username is required",
                                      detail={key: "required"})

        if not re.match(r"[A-Za-z0-9._-]{5,}", username):
            raise APIException(
                "This username is not valid",
                detail={key: "invalid"})

        return username

    @validates("password")
    def encrypt_password(self, key, password):
        """
        validate password and encrypt password
        """
        if not password:
            raise APIException("password is required",
                                      detail={key: "required"})

        if re.match(r":", password):
            raise APIException(
                "Password must be contain 8 or more caracteres",
                detail={key: "invalid"})

        return bcrypt.using(
            rounds=current_app.config["BCRYPT_ROUNDS"]).hash(current_app.config["BCRYPT_PEPPER"] +
                                                             password)

    def match_password(self, password):
        """
        Verify if passwords match
        """

        return bcrypt.verify(current_app.config["BCRYPT_PEPPER"] + password,
                             self.password)
