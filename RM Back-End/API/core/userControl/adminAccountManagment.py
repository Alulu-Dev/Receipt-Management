from bson import ObjectId
from mongoengine import ValidationError
from urllib3.exceptions import ResponseError

from ..models import accountModel, StatusLog


def upgrade_customer_to_admin(user_id):
    try:
        user_account = accountModel.objects.get(id=user_id)
        user_account.update_one(set_type='Admin')

        return "Upgraded to Admin", 200

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
        elif action == 'block':
            user_account.update(status='Blocked')
        elif action == 'delete':
            user_account.update(status='Deleted')
        else:
            raise ValidationError

        log.status_change_to = user_account.status
        log.remark = note

        log.save()

        return "Account status changed", 200

    except ValidationError:
        return "User status not modified", 500
