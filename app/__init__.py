"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, jsonify, abort, request
from flask_accepts import accepts, responds
from flask_praetorian import Praetorian, auth_required, roles_required
from flask_restplus import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from app.schemas import UserSchema, UserSchemaWithPassword


db = SQLAlchemy()
guard = Praetorian()
api = Api(title="PyData Flask API", version="0.1.0", prefix="/api", doc="/api")


def create_app(config_name: str) -> Flask:
    """Create the Flask application
    
    Args:
        config_name (str): Config name mapping to Config Class
    
    Returns:
        [Flask]: Flask Application
    """
    from app.config import config_by_name
    from app.models import User

    # Create the app
    app = Flask(__name__)

    # Log the current config name being used and setup app with the config
    app.logger: Logger
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)

    # Initialize Rest+ API
    api.init_app(app)

    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User)

    @app.route("/")
    def hello_world() -> str:  # pylint: disable=unused-variable

        return "Hello World!"

    @app.route("/login", methods=["POST"])
    def login():
        # Ignore the mimetype and always try to parse JSON.
        req = request.get_json(force=True)

        username = req.get("username", None)
        password = req.get("password", None)

        user = guard.authenticate(username, password)
        ret = {"access_token": guard.encode_jwt_token(user)}
        return (jsonify(ret), 200)

    # !!!!!!!ALERT!!!!!!!
    # This does not work. The users are a SQLAlchemy model that must be converted.
    @app.route("/uhoh", methods=["GET"])
    @auth_required
    def uh_oh():
        users: List[User] = User.query.all()
        print(type(users))
        print(users)
        return jsonify(users)

    # This works because Marshmallow is used to dump Python serialized object
    @app.route("/marsh", methods=["GET"])
    @auth_required
    def marsh():

        users = User.query.all()

        return jsonify(UserSchema(many=True).dump(users))

    @api.route("/restplus/user")
    class UserResource(Resource):
        @roles_required("admin")
        def get(self):

            users = User.query.all()

            return jsonify(UserSchema(many=True).dump(users))

    #
    # REST + Examples
    #

    # Create a namespace and attach to main API
    user_api = Namespace("User", description="User Resources")
    api.add_namespace(user_api, path="/user")

    # Attach routes to namespace
    @user_api.route("")
    class UserResourceNamespace(Resource):
        @roles_required("admin")
        def get(self):

            users = User.query.all()

            return jsonify(UserSchema(many=True).dump(users))

    @user_api.route("/<int:user_id>")
    class UserIdResourceNamespace(Resource):
        @roles_required("admin")
        def get(self, user_id: int):

            user = User.query.get(user_id)
            if not user:
                abort(404, "User was not found")

            return jsonify(UserSchema().dump(user))

    # With flask-accepts, you no longer have to manually dump on the return statement.
    # You can define all the request and response expectations on the route itself.
    @user_api.route("/flask-accepts-users")
    class UserResourceFlaskAccepts(Resource):
        @responds(schema=UserSchema, api=api, many=True)
        @roles_required("admin")
        def get(self):
            users = User.query.all()

            return users

    return app
