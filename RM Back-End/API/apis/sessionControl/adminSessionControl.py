from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from flask_login import logout_user, login_required
from flask_jwt_extended import jwt_required, get_jwt_identity

from ...core.userControl import admin_login, admin_logout
from ...core.validators import admin_login_required
from ...core.models import login_model

session = Namespace('session', description="Endpoint to control current session login and logout")

login_from = session.model('login', login_model)


@session.route("/login/")
class Login(Resource):
    @session.doc("log in user into system using email and password")
    @session.expect(login_from)
    @cross_origin()
    def post(self):
        """
        logging in user into the system
        """
        try:
            return admin_login(request.json['email'], request.json['password'])
        except:
            return "Invalid logins", 500


@session.route("/logout/")
class Logout(Resource):
    @session.doc("log out user from the system")
    # @admin_login_required
    @jwt_required()
    @cross_origin()
    def post(self):
        """
        logging out of the system
        """
        current_user = get_jwt_identity()
        # return admin_logout(current_user)
        return current_user
