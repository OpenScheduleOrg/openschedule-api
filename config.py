try:
    from dotenv import load_dotenv
    load_dotenv()
finally:
    pass

import os


class Config():
    APP_URI = os.environ.get("APP_URI")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ALGO = str(os.environ.get("ALGO")).split(",")
    SESSION_TOKEN_EXPIRE = int(os.environ.get("SESSION_TOKEN_EXPIRE"))
    LONG_TOKEN_EXPIRE = int(os.environ.get("LONG_TOKEN_EXPIRE"))

    BCRYPT_ROUNDS = os.environ.get("BCRYPT_ROUNDS")
    BCRYPT_PEPPER = os.environ.get("BCRYPT_PEPPER")

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


app_config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig
}
