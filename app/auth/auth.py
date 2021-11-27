from time import time

import jwt

from . import JWT_SECRET_KEY, TOKEN_EXPIRE, ALGO
from ..exceptions import APIExceptionHandler

def getToken(id: int, username: str, password: str, exp: int or None ):

    token = jwt.encode({"id": id, "username": username,"password": password, "exp": time() + (exp or TOKEN_EXPIRE)}, JWT_SECRET_KEY, algorithm=ALGO)

    return token


def validateToken(token):

    options = {"require": ["exp"]}

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGO], options=options )

    except jwt.exceptions.ExpiredSignatureError:
        raise APIExceptionHandler(status="fail", message="Expired token.", status_code=401)
    except jwt.exceptions.PyJWTError as e:
        raise APIExceptionHandler(status="fail", message="Invalid token.", status_code=401)
    except Exception as e:
        raise APIExceptionHandler(status="error", message="Unexpected error.", status_code=500)

    return payload
