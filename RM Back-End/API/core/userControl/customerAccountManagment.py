from urllib3.exceptions import ResponseError

from ..models import accountModel


def create_new_customer(personal_info, profile_picture):
    try:
        print(personal_info)
        new_customer = accountModel()
        new_customer.username = personal_info['username']
        new_customer.first_name = personal_info['firstname']
        new_customer.last_name = personal_info['lastname']
        new_customer.email = personal_info['email']
        new_customer.password = personal_info['password']
        new_customer.profile_picture = profile_picture

        new_customer.save()
    # go to signin function
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
        account.delete()
        return True

    except ConnectionError:
        return "Data cannot be Removed", 500


def display_customer_account_details(account_id):
    try:
        account = accountModel.objects.get(id=account_id)
        response = {
            'username': account.username,
            'firstname': account.first_name,
            'lastname': account.last_name,
            'email': account.email,
            'receipt count': account.receipt_count
        }
        return {'user': response}
    except ResponseError:
        return "Data Couldn't Be Fetched", 500


def update_customer_account_details(account_id, new_data, new_image=None):
    try:
        account = accountModel.objects.get(id=account_id)

        if 'username' in new_data and new_data['username'] != account.username:
            account.username = new_data['username']
        if 'firstname' in new_data and new_data['firstname'] != account.first_name:
            account.first_name = new_data['firstname']
        if 'lastname' in new_data and new_data['lastname'] != account.last_name:
            account.last_name = new_data['lastname']
        if 'email' in new_data and new_data['email'] != account.email:
            account.email = new_data['email']
        if 'password' in new_data and new_data['password'] != account.password:
            account.email = new_data['password']

        if new_image:
            account.profile_picture = new_image

        account.save()
        display_customer_account_details(account_id)
    except ResponseError:
        return "Data Couldn't Be Fetched", 500
