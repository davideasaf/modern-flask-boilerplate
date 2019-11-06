"User Controller"
from flask import abort, jsonify
from flask_accepts import responds
from flask_praetorian import roles_required
from flask_restplus import Namespace, Resource

from app import api
from app.models import User
from app.schemas import UserSchema

# Create a namespace and attach to main API
user_api = Namespace("User", description="User Resources")

#
# REST + Examples
#

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
    @responds(schema=UserSchema(many=True), api=api)
    @roles_required("admin")
    def get(self):
        users = User.query.all()

        return users
