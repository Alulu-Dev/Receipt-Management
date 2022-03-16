"""
MongoDB online database (MongoDB Atlas)
"""
from mongoengine import *
from datetime import datetime


class UserType(Document):
    user_type = IntField(min_value=0, max_value=2)
    type_description = StringField(required=True)
#     0 for customer, 1 for admin, 2 for superAdmin


class UserStatus(Document):
    user_status = IntField(min_value=0, max_value=2)
    status_description = StringField(required=True)
#     0 for active, 1 for blocked, 2 for deleted


class User(Document):
    username = StringField(required=True, unique=True,  min_length=3)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50, enumerate=["go", "no"])
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = ImageField(collection_name='Avatars', null=True)
    data_created = DateTimeField(default=datetime.utcnow)
    # status = ReferenceField('UserStatus', required=True)
    # type = ReferenceField('UserType', required=True)
    status = StringField(required=True, default='Customer', enumerate=['Customer', 'Admin', 'SuperAdmin'])
    type = StringField(required=True, default='Active', enumerate=['Active', 'Blocked', 'Deleted'])

    meta = {
        'indexes': ['username', 'email'],
        'ordering': ['first_name']
    }


# class ProfileAvatar:
#     pass
#
#
class Receipt(Document):
    """
    TIN Number
    FS Number
    Issued Date
    Business Place Name
    Description
    Total Price
    Date Created On
    """
    pass


class PurchasedItems(Document):
    """
    Receipt ID
    Name
    Quantity
    Price
    Group / Standard Names
    """
    pass


class ItemsDictionary(Document):
    """
    Standard Name
    default == uncategorized
    """
    pass
#
# class ReceiptImages:
#     pass
#
#


class ExpenseSummary:
    """
    User ID
    Receipt ID List
    Total Price
    Title
    Description
    """
    pass
#
#


class FraudReport:
    """
    User ID
    TIN Number
    FS Number
    Total Price
    Reported
    Date Issued

    """
    pass
#
#
# class PredictionReport:
#     pass
#
#
# class PriceComparison:
#     pass
#
#
# class UserRequest:
#     pass
#
#
# class ReceiptItems:
#     pass
#
#


class ERCARecord:
    """
    TIN Number
    FS Number
    Total Price
    Date Issued
    """
    pass
