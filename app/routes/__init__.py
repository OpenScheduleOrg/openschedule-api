from flask import Blueprint, jsonify, request

bp_api = Blueprint("api", "api", url_prefix="/api")
bp_auth = Blueprint("auth", "auth", url_prefix="/auth")

from . import patient, clinic, auth, user, professional, specialty, acting
