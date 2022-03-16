"""
MongoDB online database (MongoDB Atlas)
"""
from ast import List
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
    tin_number = IntField(required=True)
    fs_number = IntField(required=True,unique=True)
    issued_date = DateTimeField(required=True)
    business_place_name = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=50)
    total_price = FloatField(required=True)
    date_created_on = DateTimeField(default=datetime.utcnow)



    

    pass


class PurchasedItems(Document):
    """
    Receipt ID
    Name
    Quantity
    Price
    Group / Standard Names
    """
    receipt_id = IntField(required=True)
    name = StringField(required=True, max_length=50)
    quantity = IntField(required=True)
    item_price = FloatField(required=True)
    tag = ReferenceField('ItemsDictionary', required=True)



    pass


class ItemsDictionary(Document):
    """
    Standard Name / Tag
    default == uncategorized
    """
    tag = StringField(required=True, max_length=50)



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
    user_id = ReferenceField('User', required=True)
    receipt_id_list = ListField(ReferenceField('Receipt', required=True))
    total_price = FloatField(required=True)
    title = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=50)


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
    user_id = ReferenceField('User', required=True)
    tin_number = IntField(required=True)
    fs_number = IntField(required=True,unique=True)
    total_price = FloatField(required=True)
    reported = BooleanField(required=True)
    issued_date = DateTimeField(required=True)


    pass


class PredictionReport:
    """
    User ID
    Item Tag
    ProbabilityPercent
    Data Range
    """
    user_id = ReferenceField('User', required=True)
    tag = StringField(required=True, max_length=50)
    probability_percent = FloatField(required=True)
    date_range = ListField(DateTimeField(required=True), max_length=2)
    pass


class PriceComparison:
    """
    Item Tag
    Best Price
    Business PLace
    """
    tag = StringField(required=True, max_length=50)
    total_price = FloatField(required=True)
    business_place = StringField(required=True, max_length=50)
    pass


class UserRequest:
    """
    User ID
    Request Resolved
    Receipt ID
    """
    user_id = ReferenceField('User', required=True)
    receipt_id = IntField(required=True)
    request_resolved = BooleanField(required=True)


    pass



class ERCARecord:
    """
    TIN Number
    FS Number
    Total Price
    Date Issued
    """
    tin_number = IntField(required=True)
    fs_number = IntField(required=True,unique=True)
    total_price = FloatField(required=True)
    issued_date = DateTimeField(required=True)
    pass
