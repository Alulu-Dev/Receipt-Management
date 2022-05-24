import datetime
import jwt
from bson import ObjectId
from flask import jsonify
from flask_jwt_extended import create_access_token
from mongoengine import ValidationError, DoesNotExist
from urllib3.exceptions import ResponseError

from API.settings import APP_SECRET_KEY
from ..models import accountModel, StatusLog, ActiveAdmins


def upgrade_customer_to_admin(user_id):
    try:
        user_account = accountModel.objects.get(id=user_id)
        user_account.update(account_type='Admin')

        return "Upgraded to Admin"

    except ResponseError:
        return "User not upgraded to Admin", 500


def change_account_status(user_id, action, note):
    try:
        user_account = accountModel.objects.get(id=user_id)
        log = StatusLog()
        log.subject = ObjectId(user_id)
        log.status_change_from = user_account.status
        if action == 'activate':
            user_account.update(status='Active')
            log.status_change_to = "Active"
        elif action == 'block':
            user_account.update(status='Blocked')
            log.status_change_to = "Blocked"
        elif action == 'delete':
            user_account.update(status='Deleted')
            log.status_change_to = "Deleted"
        else:
            raise ValidationError


        log.remark = note

        log.save()

        return "Account status changed", 200

    except ValidationError:
        return "User status not modified", 500


def get_all_users():
    try:
        users = accountModel.objects()
        list_of_users = []
        key = 0
        for user in users:
            if user.account_type != "SuperAdmin":
                key += 1
                data = {
                    "key": key,
                    "name": user.first_name + " " + user.last_name,
                    "id": str(user.id),
                    "numOfReceipts": user.receipt_count,
                    "tags": [user.status],
                }
                list_of_users.append(data)
        return list_of_users, 200
    except:
        return "Oops Somethings went wrong", 501


def admin_login(user_email, user_password):
    try:
        user = accountModel.objects.get(email=user_email)
        try:
            ActiveAdmins.objects.get(admin_id=user.id)
            return "Only One Login Per account allowed", 400
        except DoesNotExist:
            if user.status == "Active" and (user.account_type == "Admin" or user.account_type == "SuperAdmin"):
                if user.password == user_password:
                    access_token = create_access_token(identity=str(user.id))
                    return jsonify(access_token=access_token)
                else:
                    raise DoesNotExist
            elif user.status == "Blocked":
                return "Your account is Blocked! \n " \
                       "Contact the Administrator \n " \
                       "Email: westegb@gmail.com", 401
            elif user.status == "Deleted":
                return "This Account does not Exist Anymore!" \
                       "Contact the Administrator \n " \
                       "Email: westegb@gmail.com", 401
            else:
                raise DoesNotExist
    except DoesNotExist:
        return "Invalid login detail", 401


def admin_logout(admin_id):
    try:
        admin = ActiveAdmins.objects.get(admin_id=admin_id)
        admin.delete()
        return "GoodBye!", 200
    except DoesNotExist:
        return "Oops! somethings went wrong", 501
