# from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from flask_login import logout_user, login_required

from ...core.userControl import user_login

session = Namespace('session', description="Endpoint to control current session login and logout")


@session.route("/login/<user_email>/<user_password>/")
class Login(Resource):
    @session.doc("log in user into system using email and password")
    def post(self, user_email, user_password):
        """
        logging in user into the system
        """
        return user_login(user_email, user_password)


@session.route("/logout/")
class Logout(Resource):
    @session.doc("log out user from the system")
    @login_required
    # @cross_origin()
    def post(self):
        """
        logging out of the system
        """
        logout_user()
        return "user logged out", 202
