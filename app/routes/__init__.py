from flask import Blueprint

api = Blueprint("api", "api")

from app.routes import cliente, clinica, consulta, horario
