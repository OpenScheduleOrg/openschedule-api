import os
from time import time, sleep

import jwt
import pytest

from app.auth import getToken, validateToken, TOKEN_EXPIRE, ALGO
from app.exceptions import APIExceptionHandler

jwt_secret_key = os.environ.get("JWT_SECRET_KEY")


def test_get_token():
    payload = {"id": 1, "username": "foo", "password": "bar"}

    token = getToken(*payload.values(), None)

    expected_payload = jwt.decode(token, jwt_secret_key, algorithms=[ALGO])

    assert payload["id"] == expected_payload["id"]
    assert payload["username"] == expected_payload["username"]


def test_validate_token():
    payload = {"exp": time() + TOKEN_EXPIRE}

    token = jwt.encode(payload, jwt_secret_key, algorithm=ALGO)

    validateToken(token)

    with pytest.raises(APIExceptionHandler,
                       match="Expired token.") as exc_info:
        payload["exp"] = time()
        sleep(1)
        token = jwt.encode(payload, jwt_secret_key, algorithm=ALGO)
        validateToken(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.status == "fail"

    with pytest.raises(APIExceptionHandler,
                       match="Invalid token.") as exc_info:
        payload["exp"] = time() + TOKEN_EXPIRE
        token = jwt.encode(payload, "secret", algorithm=ALGO)
        validateToken(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.status == "fail"
