from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from mongoengine import ValidationError
from werkzeug.utils import secure_filename
from tempfile import TemporaryDirectory
from flask_login import current_user, login_required

from ..core.userControl import (user_signup, admin_signup, delete_account,
                                get_customer, update_customer, status_control,
                                )
from ..core.validators import (check_file, check_signup_form, admin_role_required, check_update_form,
                               CustomValidationException, CustomFileValidationException)
from ..core.models import signup_form, update_form, id_form, status_form

api = Namespace('account', description="Endpoint to create, update and delete accounts on the system")

status_form = api.model('ChangeStatus', status_form)


@api.route('/signup/user/')
class RegisterNewCustomer(Resource):
    @api.expect(signup_form)
    def post(self):
        """
        Create a system user account and log in automatically
        """
        try:
            if check_file(request) and check_signup_form(request.form):
                file = request.files['file']
                with TemporaryDirectory(prefix='file_holder') as tempdir:
                    filename = secure_filename(file.filename)
                    file.save(tempdir + '/' + filename)
                    file_path = tempdir + "/" + file.filename
                    return user_signup(request.form, file_path)
            return "User Not Create", 400
        except (CustomValidationException, CustomFileValidationException, ValidationError) as e:
            return e.message, 400


@api.route('/upgrade/user/')
class UpgradeUserToAdmin(Resource):
    @api.doc("Required Admin level clearance")
    @api.expect(id_form)
    @login_required
    @admin_role_required
    def post(self):
        """
        Upgrade user access level to Admin
        """

        if request.form['userId']:
            return admin_signup(request.form['userId']), 200
        return False


@api.route('/modify/status/')
class AdminModifyUserAccount(Resource):
    @api.doc("User")
    @login_required
    @admin_role_required
    @api.expect(status_form)
    def put(self):
        """
        Admins change users account status when they violate rules and regulations
        """
        return status_control(request.json['user'], request.json['status'], request.json['reason'])


@api.route('/user/')
class UserAccountControl(Resource):
    @api.doc("Get account details")
    @cross_origin()
    @login_required
    def get(self):
        """
        Get account details
        """
        return get_customer(current_user.id)

    @api.doc("Remove account from the system by setting it's status to removed and "
             "deleting it after 30 days with all it's data")
    @login_required  # will be replaced by login_required
    def delete(self):
        """
        Remove account from the system
        """
        if delete_account(current_user.id):
            return "Account Deleted", 200
        else:
            return False, 400

    @api.doc("Update account details")
    @api.expect(update_form)
    @login_required
    def put(self):
        """
        Modify account details
        """
        if check_update_form(request.form):
            if 'file' in request.files and check_file(request):
                file = request.files['file']
                with TemporaryDirectory(prefix='file_holder') as tempdir:
                    filename = secure_filename(file.filename)
                    file.save(tempdir + '/' + filename)
                    file_path = tempdir + "/" + file.filename

                    return update_customer(current_user.id, request.form, file_path)

            return update_customer(current_user.id, request.form)

        return "Invalid inputs", 400
