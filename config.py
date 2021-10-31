try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass


config = {"dev": DevelopmentConfig, "test": TestingConfig, "prod":ProductionConfig}
