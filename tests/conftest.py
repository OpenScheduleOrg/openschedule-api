import pytest

from db import set_up_db
from app import create_app
from app.config import app_configs


@pytest.fixture(name="app")
def fixture_app():
    """
    Instantiate flask application
    """
    config = app_configs["test"]
    flask_app = create_app(config)

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
