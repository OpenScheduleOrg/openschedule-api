import pytest
from flask import testing
from werkzeug.datastructures import Headers

import jwt

from db import set_up_db
from app import create_app
from app.config import app_configs


class TestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key_headers = Headers({
            'Authorization': "Bearer " + jwt.encode({
                'id': 1,
                'name': "Test",
                'username': "test",
                'email': "test@test.com",
                'admin': True,
            }, app_configs["test"].JWT_SECRET_KEY, "HS256")
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


@pytest.fixture(name="app")
def fixture_app():
    """
    Instantiate flask application
    """
    config = app_configs["test"]
    flask_app = create_app(config)
    flask_app.test_client_class = TestClient

    yield flask_app


@pytest.fixture(name="client")
def fixture_client(app):
    """
    Client a flask test client
    """
    with app.app_context():
        set_up_db()
    return app.test_client()


if __name__ == "__main__":
    fixture_app()
