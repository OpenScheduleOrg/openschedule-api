import os
import decimal
from datetime import date

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

from app.models import db, set_up_data
from app.docs import swagger_template, swagger_config
from app.json import CustomJSONProvider

from .config import app_configs
from .exceptions import resource_not_found, internal_server_error, \
    APIException, api_exception_handler, ValidationException, validation_exception_handler, \
    AuthenticationException, authentication_exception_handler, \
    AuthorizationException, authorization_exception_handler


def create_app(app_config=app_configs[os.environ.get("APP_CONFIG")
                                      or "production"]):
    """
    Instancing flask app
    """
    app = Flask(__name__)
    CORS(app, origins=app_config.CORS_ORIGINS, supports_credentials=True)
    app.config.from_object(app_config)

    Swagger(app, template=swagger_template, config=swagger_config)

    app.json = CustomJSONProvider(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        set_up_data(db)

    from app.routes import bp_api, bp_auth

    app.register_blueprint(bp_api)
    app.register_blueprint(bp_auth)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(Exception, internal_server_error)
    app.register_error_handler(APIException, api_exception_handler)
    app.register_error_handler(ValidationException,
                               validation_exception_handler)
    app.register_error_handler(AuthenticationException,
                               authentication_exception_handler)
    app.register_error_handler(AuthorizationException,
                               authorization_exception_handler)

    return app
