import datetime

from flask import send_file
from mongoengine import DoesNotExist
from urllib3.exceptions import ResponseError
from flask_login import login_user, current_user, logout_user

from ..models import accountModel, receiptDataModel, UserRequest


def create_new_customer(personal_info, profile_picture):
    try:
        print(12)
        new_customer = accountModel()
        new_customer.first_name = personal_info['firstname']
        new_customer.last_name = personal_info['lastname']
        new_customer.email = personal_info['email']
        new_customer.password = personal_info['password']
        new_customer.profile_picture = profile_picture

        new_customer.save()
        # go to signin function
        user_id = new_customer.id
        user = accountModel.objects.get(id=user_id)
        return user_login(user.email, user.password)

    except ResponseError:
        return "Data cannot be Created", 500


def remove_customer_account(account_id):
    """
    * user can remove their account and
    * admins can remove users when they violate regulations
    will be updated to change status to deleted and once 30 days pass to actually delete the data
    """
    try:
        account = accountModel.objects.get(id=account_id)
        account.deleted = True
        account.deleted_on = datetime.datetime.utcnow
        receipts = receiptDataModel.objects(owner=account_id)

        for receipt in receipts:
            receipt.deleted = True
            receipt.deleted_on = datetime.datetime.utcnow

        logout_user()
        return True

    except ConnectionError:
        return "Data cannot be Removed", 500


def display_customer_account_details(account_id):
    try:
        account = accountModel.objects.get(id=account_id)
        delta = datetime.datetime.today()
        day = account.data_created
        difference = delta - day
        request_count = len(UserRequest.objects(user_id=account_id))
        response_data = {
            "id": str(account.id),
            "firstname": account.first_name,
            "lastname": account.last_name,
            "email": account.email,
            "receipt count": account.receipt_count,
            "request count": request_count,
            "days with us": difference.days,
        }
        response = send_file(account.profile_picture, mimetype='image/jgp')
        response.headers['data'] = response_data
        return response
    except ResponseError:
        return "Data Couldn't Be Fetched", 500


def update_customer_account_details(account_id, new_data, new_image=None):
    # try:
        new_data = new_data.to_dict(flat=False)
        account = accountModel.objects.get(id=account_id)

        if "firstname" in new_data and new_data['firstname'][0] != account.first_name:
            account.first_name = new_data['firstname'][0]
        if 'lastname' in new_data and new_data['lastname'][0] != account.last_name:
            account.last_name = new_data['lastname'][0]
        if 'email' in new_data and new_data['email'][0] != account.email:
            account.email = new_data['email'][0]
        if 'old-password' in new_data and new_data['old-password'][0] == account.password:
            if 'password' in new_data and new_data['password'][0] != account.password:
                account.passwords = new_data['password'][0]
        if new_image is not None:
            account.profile_picture = new_image

        account.save()
        return display_customer_account_details(account_id)
    # except ResponseError:
    #     return "Data Couldn't Be Fetched", 500


def user_login(user_email, user_password):
    try:

        user = accountModel.objects.get(email=user_email)
        # check user status before letting them log in
        if user.status == "Active":
            if user.password == user_password:
                login_user(user)

                return current_user.first_name
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
    except DoesNotExist:
        return "Invalid login detail", 401
