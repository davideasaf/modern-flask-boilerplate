"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger

from flask import Flask


def create_app(config_name):
    """Create the Flask application
    
    Args:
        config_name (Config): A Config class for the Flask application to use
    
    Returns:
        [Flask]: Flask Application
    """
    from app.config import config_by_name

    app = Flask(__name__)
    app.logger: Logger
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    @app.route("/")
    def hello_world() -> str:  # pylint: disable=unused-variable
        return "Hello World!"

    return app
