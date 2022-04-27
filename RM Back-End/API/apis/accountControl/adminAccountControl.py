from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from flask_login import login_required

from ...core.userControl import (admin_signup, status_control, get_all_users)
from ...core.validators import (admin_role_required, )
from ...core.models import (id_form, status_form)
from ...core.validators import admin_login_required


api = Namespace('account', description="System admins account control endpoints")

status_form = api.model('ChangeStatus', status_form)


@api.route('/upgrade/user/')
class UpgradeUserToAdmin(Resource):
    @api.doc("Required Admin level clearance")
    @api.expect(id_form)
    @jwt_required()
    @cross_origin()
    def post(self):
        """
        Upgrade user access level to Admin
        """

        if request.form['userId']:
            print(1)
            return admin_signup(request.form['userId']), 200
        return False


@api.route('/modify/status/')
class AdminModifyUserAccount(Resource):
    @api.doc("User")
    @jwt_required()
    @api.expect(status_form)
    def put(self):
        """
        Admins change users account status when they violate rules and regulations
        """
        return status_control(request.json['user'], request.json['status'], request.json['reason'])


@api.route('/all-users/')
class AllUsersStatus(Resource):
    @api.doc(
        """
        Returns all users list with their basic data, account status
        """
    )
    @jwt_required()
    def get(self):
        return get_all_users()
