import os

from flask import Flask,  request
from flask_sqlalchemy import SQLAlchemy
from config import app_config

from app.common.exc import resource_not_found, APIExceptionHandler, api_exception_handler

def create_app(app_config=app_config[os.environ.get("APP_CONFIG") or "production"]):
    app = Flask(__name__)
    app.config.from_object(app_config)

    from app.models import db
    db.init_app(app)

    from app.routes import api

    app.register_blueprint(api)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(APIExceptionHandler, api_exception_handler)

    return app
