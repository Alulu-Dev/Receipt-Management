# from flask import request
from flask_restx import Namespace, Resource
from flask_login import logout_user, login_user, login_required, current_user

from ..core.models import accountModel

session = Namespace('session', description="Endpoint to control current session login and logout")


@session.route("/login/<user_email>/<user_password>/")
class Login(Resource):
    @session.doc("log in user into system using email and password")
    def post(self, user_email, user_password):
        """
        logging in user into the system
        """
        try:

            user = accountModel.objects.get(email=user_email)
            # check user status before letting them log in
            if user.password == user_password:
                login_user(user)

                # return "Welcome", 202
                return current_user.username
            else:
                raise ConnectionError

        except ConnectionError:
            return "Invalid login detail", 401


@session.route("/logout/")
class Logout(Resource):
    @session.doc("log out user from the system")
    @login_required
    def post(self):
        """
        logging out of the system
        """
        logout_user()
        return "user logged out", 202
