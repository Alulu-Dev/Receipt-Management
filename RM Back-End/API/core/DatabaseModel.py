"""
MongoDB online database (MongoDB Atlas)
"""
from mongoengine import *
from datetime import datetime


class User(Document):
    username = StringField(required=True, unique=True,  min_length=3)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50, enumerate=["go", "no"])
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = ImageField(collection_name='Avatars', null=True)
    data_created = DateTimeField(default=datetime.utcnow)
    status = StringField(required=True, default='Customer', enumerate=['Customer', 'Admin', 'SuperAdmin'])
    type = StringField(required=True, default='Active', enumerate=['Active', 'Blocked', 'Deleted'])

    meta = {
        'indexes': ['username', 'email'],
        'ordering': ['first_name']
    }


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
    Standard Name / Tag
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


class PredictionReport:
    """
    User ID
    Item Tag
    ProbabilityPercent
    Data Range
    """
    pass


class PriceComparison:
    """
    Item Tag
    Best Price
    Business PLace
    """
    pass


class UserRequest:
    """
    User ID
    Request Resolved
    Receipt ID
    """
    pass


class ERCARecord:
    """
    TIN Number
    FS Number
    Total Price
    Date Issued
    """
    pass
