try:
    from dotenv import load_dotenv
    load_dotenv()
finally:
    pass

import os


class Config():
    FLASK_ENV = os.environ.get("FLASK_ENV")
    APP_URI = os.environ.get("APP_URI")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE = int(os.environ.get("ACCESS_TOKEN_EXPIRE"))
    SESSION_TOKEN_EXPIRE = int(os.environ.get("SESSION_TOKEN_EXPIRE"))

    BCRYPT_ROUNDS = os.environ.get("BCRYPT_ROUNDS")
    BCRYPT_PEPPER = os.environ.get("BCRYPT_PEPPER")

    DEBUG = False
    TESTING = False

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(";")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


app_configs = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig
}
