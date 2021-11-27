try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

import os

class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
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


app_config = {"development": DevelopmentConfig, "test": TestingConfig, "production":ProductionConfig}
