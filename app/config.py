""" Provide the capability to configure the app based on target environment. """

import os


class Config:
    """ Base config. """

    DEBUG: bool = False


class TestingConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = "my_precious_secret_key"
    TESTING: bool = True


class DevelopmentConfig(Config):
    """ A config to be used for development, use mocks so you don't need a DB. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_precious_development_secret_key")


class ProductionConfig(Config):
    """ Production config. """

    # Inherits defaults from parent.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dc89aa6c-93e7-474d-a55a-b2113b25fc16")


config_by_name = dict(  # pylint: disable=invalid-name
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
