from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config[os.environ.get("APP_CONFIG") or "production"])
db = SQLAlchemy(app)

from app import routes
