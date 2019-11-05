from flask import Flask


def create_app(config_name):
    from app.config import config_by_name

    app = Flask(__name__)
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    @app.route("/")
    def hello_world():
        return "Hello World!"

    return app
