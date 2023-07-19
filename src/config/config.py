import os
from decouple import config
from datetime import timedelta

VERSION = 1.0

# uri = config("DATABASE_URL")  # or other relevant config var
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    Swagger = {"tittle": "Motorcycle API", "uiversion": 3}


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "TestSecretKey"
    JWT_SECRET_KEY = "TestJWTSecretKey"


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


config_dict = {"dev": DevConfig, "testing": TestConfig, "production": ProdConfig}
