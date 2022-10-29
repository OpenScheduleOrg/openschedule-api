from functools import wraps
from flask import request, current_app

from ..helpers.auth import get_header_token, decode_token
from ..exceptions import AuthorizationException
from ..constants import ResponseMessages


def token_required(f):
    """
    Verify if user is authtenticated and token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = get_header_token(request.headers.get("Authorization"))

        payload = decode_token(auth_token,
                               current_app.config["JWT_SECRET_KEY"], "HS256")
        return f(
            {
                "id": payload["id"],
                "name": payload["name"],
                "admin": payload["admin"]
            }, *args, **kwargs)

    return decorated


def only_admin(f):
    """
    Verify if user is admin
    """

    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user["admin"]:
            raise AuthorizationException(ResponseMessages.ONLY_ADMIN)

        return f(current_user, *args, **kwargs)

    return decorated
