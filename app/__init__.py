import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

def create_app(app_config=app_config[os.environ.get("APP_CONFIG") or "production"]):
    app = Flask(__name__)
    app.config.from_object(app_config)
    db = SQLAlchemy(app)

    from app.models import db
    db.init_app(app)

    from app.routes import api

    app.register_blueprint(api)

    return app
