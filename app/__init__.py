import os

from flask import Flask,  request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import app_config
from .exceptions import resource_not_found, internal_server_error, APIExceptionHandler, api_exception_handler

def create_app(app_config=app_config[os.environ.get("APP_CONFIG") or "production"]):
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:8080", "http://10.0.0.115:8080"], supports_credentials=True)
    app.config.from_object(app_config)

    from app.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app.routes import bp_api, bp_auth

    app.register_blueprint(bp_api)
    app.register_blueprint(bp_auth)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(APIExceptionHandler, api_exception_handler)

    return app
