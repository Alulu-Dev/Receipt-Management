"""
MongoDB online database (MongoDB Atlas)
"""
from mongoengine import *
from datetime import datetime
from flask_login import UserMixin


class User(Document, UserMixin):
    username = StringField(required=True, unique=True, min_length=3)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = ImageField(collection_name='Avatars', null=True)
    data_created = DateTimeField(default=datetime.utcnow)
    type = StringField(required=True, default='Customer', enumerate=['Customer', 'Admin', 'SuperAdmin'])
    status = StringField(required=True, default='Active', enumerate=['Active', 'Blocked', 'Deleted'])
    receipt_count = IntField(required=True, default=0, min_value=0)

    meta = {
        'indexes': ['username', 'email'],
        'ordering': ['first_name']
    }


class AccountStatusLog(Document):
    subject = ReferenceField('User', required=True)
    status_change_from = StringField(required=True, enumerate=['Active', 'Blocked', 'Deleted'])
    status_change_to = StringField(required=True, enumerate=['Active', 'Blocked', 'Deleted'])
    remark = StringField(min_length=3, required=True)


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
    owner = ReferenceField('User', required=True)
    tin_number = StringField(required=True)
    fs_number = StringField(required=True, unique=True)
    issued_date = DateTimeField(required=True)
    business_place_name = StringField(required=True, max_length=50)
    description = StringField(max_length=100)
    total_price = FloatField(required=True)
    register_id = StringField(min_length=3, required=True)
    fraud_check = StringField(default='unchecked', enumerate= ['unchecked', 'checked', 'illegal'])
    items = ListField(ReferenceField('Items'))
    date_created_on = DateTimeField(default=datetime.utcnow)


class Items(Document):
    """
    Receipt ID
    Name
    Quantity
    Price
    Group / Standard Names
    """
    receipt_id = ReferenceField('Receipt', required=True)
    name = StringField(required=True, max_length=50)
    quantity = FloatField(required=True)
    item_price = FloatField(required=True)
    tag = ReferenceField('ItemsDictionary')


class ItemsDictionary(Document):
    """
    Standard Name / Tag
    default == uncategorized
    """
    tag = StringField(required=True, max_length=50)


class ExpenseSummary(Document):
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


class FraudReport(Document):
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
    fs_number = IntField(required=True, unique=True)
    total_price = FloatField(required=True)
    reported = BooleanField(required=True)
    issued_date = DateTimeField(required=True)


class PredictionReport(Document):
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


class PriceComparison(Document):
    """
    Item Tag
    Best Price
    Business PLace
    """
    tag = StringField(required=True, max_length=50)
    total_price = FloatField(required=True)
    business_place = StringField(required=True, max_length=50)


class UserRequest(Document):
    """
    User ID
    Request Resolved
    Receipt ID
    """
    user_id = ReferenceField('User', required=True)
    receipt_id = IntField(required=True)
    resolved = BooleanField(default=False, required=True)


class ERCARecord(Document):
    """
    TIN Number
    FS Number
    Total Price
    Date Issued
    """
    tin_number = IntField(required=True)
    fs_number = IntField(required=True, unique=True)
    total_price = FloatField(required=True)
    issued_date = DateTimeField(required=True)
