import os

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGO = "HS256"

TOKEN_EXPIRE = 30 * 86400
REMEMBER_EXPIRE = 365 * 2 * 84560

from .auth import getToken, validateToken

