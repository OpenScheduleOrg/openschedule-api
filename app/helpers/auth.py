import jwt

from ..exceptions import AuthenticationException


def get_header_token(auth_header):
    """
    Obtain token from header
    """
    if auth_header and len((auth_header := auth_header.split(" "))) == 2:
        return auth_header[1]
    raise AuthenticationException("provide a valid access token")


def decode_token(token, secret_key, algo):
    """
    Decode jwt token and return payload or raise exception wether invalid
    """
    try:
        return jwt.decode(token, secret_key, algo)
    except jwt.ExpiredSignatureError as err:
        raise AuthenticationException("access token expired") from err
    except jwt.InvalidTokenError as err:
        raise AuthenticationException("access token invalid") from err
