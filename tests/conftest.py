import os
import tempfile

import pytest
from flask import json


from app import create_app
from config import app_config
from db import set_up_db

@pytest.fixture
def app():
    """
    Instancia da aplicação flask
    """
    db_fd, db_path = tempfile.mkstemp("db")
    config = app_config["test"]
    config.SQLALCHEMY_DATABASE_URI = "sqlite:///"+db_path
    app = create_app(app_config["test"])


    with app.app_context():
        set_up_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """
    Client para test de requisições
    """
    return app.test_client()



if __name__ == "__main__":
    app()
