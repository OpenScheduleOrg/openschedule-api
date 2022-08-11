import os
import enum
from hashlib import sha256
import hmac
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

from .exceptions import APIException


class AccessLevel(enum.Enum):
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


def gera_csrf_token(key):
    """
    Gera um csrf token para autorização via cookie
    """
    hash_csrf_token = sha256(os.urandom(64)).hexdigest()
    hmac_csrf_token = hmac.new(key, hash_csrf_token.encode("utf-8"), digestmod=sha256)

    return hmac_csrf_token.hexdigest()


def cria_token(usuario, exp: int or None = None, csrf_token: str or None = None):
    """
    Generate JWT token
    """
    payload = {
        "sub": usuario.id,
        "username": usuario.username,
        "nivel_acesso": usuario.nivel_acesso.value,
        "exp": datetime.now(
            tz=timezone.utc) + timedelta(seconds=(exp or current_app.config["SESSION_TOKEN_EXPIRE"])),
        "iat": datetime.now(tz=timezone.utc),
        "aud": current_app.config["APP_URI"]
    }
    if csrf_token:
        payload["csrf_token"] = csrf_token

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["ALGO"][0])

    return token


def verifica_token(token):
    """
    verify if token is valid and return the payload
    """

    options = {"require": ["exp", "sub", "aud"]}

    try:
        payload = jwt.decode(token,
                             current_app.config["JWT_SECRET_KEY"],
                             audience=current_app.config["APP_URI"],
                             algorithms=current_app.config["ALGO"],
                             options=options)

    except jwt.exceptions.ExpiredSignatureError as error:
        raise APIException(status="fail",
                                  message="Expired token.",
                                  status_code=401) from error
    except jwt.exceptions.PyJWTError as error:
        raise APIException(status="fail",
                                  message="Invalid token.",
                                  status_code=401) from error
    except Exception as error:
        raise APIException(status="error",
                                  message="Unexpected error.",
                                  status_code=500) from error

    return payload
