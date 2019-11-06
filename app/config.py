""" Provide the capability to configure the app based on target environment. """
# Flask-SqlALchemy configs: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
import os
from typing import Dict


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base config. """

    DEBUG: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = "top secret"
    JWT_ACCESS_LIFESPAN: Dict[str, int] = {"hours": 24}
    JWT_REFRESH_LIFESPAN: Dict[str, int] = {"days": 30}


class TestingConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{BASEDIR}/app-test.db"
    SECRET_KEY: str = "my_precious_secret_key"
    TESTING: bool = True


class DevelopmentConfig(Config):
    """ A config to be used for development, use mocks so you don't need a DB. """

    # Override defaults from parent.
    #
    SERVER_NAME: str = "localhost:5000"
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_precious_development_secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL


class ProductionConfig(Config):
    """ Production config. """

    # Inherits defaults from parent.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dc89aa6c-93e7-474d-a55a-b2113b25fc16")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL


config_by_name = dict(  # pylint: disable=invalid-name
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
