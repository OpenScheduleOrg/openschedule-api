import enum
import re

from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship, validates

from flask import current_app
from passlib.hash import bcrypt

from . import db, TimestampMixin
from ..exceptions import APIExceptionHandler


class NivelAcesso(enum.Enum):
    """
        Enum with access level
    """
    CLINICA_READ = 0b0000000001
    CLINICA_WRITE = 0b0000000010
    USUARIO_READ = 0b0000000100
    USUARIO_WRITE = 0b0000001000
    CONSULTA_READ = 0b0000010000
    CONSULTA_WRITE = 0b0000100000
    CLIENTE_READ = 0b0001000000
    CLIENTE_WRITE = 0b0010000000
    HORARIO_READ = 0b0100000000
    HORARIO_WRITE = 0b1000000000

    ADMIN = CLINICA_READ + CLINICA_WRITE + USUARIO_READ + \
        USUARIO_WRITE + CONSULTA_READ + \
        CONSULTA_WRITE + CLIENTE_READ + \
        CLIENTE_WRITE + HORARIO_READ + HORARIO_WRITE

    CLINICA_ADMIN = CLINICA_READ + USUARIO_READ + USUARIO_WRITE + \
        CONSULTA_READ + CONSULTA_WRITE + CLIENTE_READ + \
        CLIENTE_WRITE + HORARIO_READ + HORARIO_WRITE

    FUNCIONARI0 = CLINICA_READ + USUARIO_READ + CONSULTA_READ + \
        CONSULTA_WRITE + CLIENTE_READ + CLIENTE_WRITE +\
        HORARIO_READ + HORARIO_WRITE


class Usuario(TimestampMixin, db.Model):
    __tablename__ = "usuario"

    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    foto = Column(String(255), nullable=True)
    nivel_acesso = Column(Enum(NivelAcesso), nullable=False)
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
            raise APIExceptionHandler("username is required",
                                      detail={key: "required"})

        if not re.match(r"[A-Za-z0-9._-]{5,}", username):
            raise APIExceptionHandler(
                "This username is not valid",
                detail={key: "invalid"})

        return username

    @validates("password")
    def encrypt_password(self, key, password):
        """
        validate password and encrypt password
        """
        if not password:
            raise APIExceptionHandler("password is required",
                                      detail={key: "required"})

        if re.match(r":", password):
            raise APIExceptionHandler(
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
