import pytest

from app import create_app
from app.auth import cria_token
from config import app_config
from db import set_up_db, session, select, Usuario


@pytest.fixture
def app():
    """
    Instancia da aplicação flask
    """
    config = app_config["test"]
    app = create_app(config)

    with app.app_context():
        set_up_db()

    yield app


@pytest.fixture
def client(app):
    """
    Client para test de requisições
    """
    return app.test_client()


@pytest.fixture
def access_token(app):
    """
    Client para test de requisições
    """
    with app.app_context():
        usuario = session.execute(select(Usuario)).scalars().first()

        access_token = cria_token(usuario)

    return access_token


if __name__ == "__main__":
    app()
