"""
MongoDB online database (MongoDB Atlas)
"""
from mongoengine import *
from datetime import datetime
from flask_login import UserMixin


class User(Document, UserMixin):
    # username = StringField(required=True, unique=True, min_length=3)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = ImageField(collection_name='Avatars', null=True)
    data_created = DateTimeField(default=datetime.utcnow)
    account_type = StringField(required=True, default='Customer', enumerate=['Customer', 'Admin', 'SuperAdmin'])
    status = StringField(required=True, default='Active', enumerate=['Active', 'Blocked', 'Deleted'])
    receipt_count = IntField(required=True, default=0, min_value=0)
    deleted = BooleanField(default=False)
    deleted_on = DateTimeField()

    meta = {
        'indexes': ['account_type', 'email'],
        'ordering': ['first_name']
    }


class ActiveAdmins(Document):
    admin_id = ReferenceField('User', required=True)


class AccountStatusLog(Document):
    subject = ReferenceField('User', required=True)
    status_change_from = StringField(required=True, enumerate=['Active', 'Blocked', 'Deleted'])
    status_change_to = StringField(required=True, enumerate=['Active', 'Blocked', 'Deleted'])
    remark = StringField(min_length=3, required=True)
    logged_on = DateTimeField(default=datetime.utcnow)


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
    business_place_name = StringField(required=True, min_length=3)
    description = StringField(max_length=100)
    category_id = ReferenceField('Categories', required=True)
    total_price = FloatField(required=True)
    register_id = StringField(min_length=3, required=True)
    fraud_check = StringField(default='unchecked', enumerate=['unchecked', 'checked', 'illegal'])
    items = ListField(ReferenceField('Items'))
    date_created_on = DateTimeField(default=datetime.utcnow)
    deleted = BooleanField(default=False)
    deleted_on = DateTimeField()

    meta = {
        'indexes': ['business_place_name', 'owner'],
        'ordering': ['issued_date']
    }


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
    owner = ReferenceField('User', required=True)
    tag = StringField(required=True, max_length=50)
    result = ListField(required=True)
    created_date = DateTimeField(default=datetime.utcnow)


class UserRequest(Document):
    """
    User ID
    Request Resolved
    Receipt ID
    """
    user_id = ReferenceField('User', required=True)
    receipt_id = ReferenceField('Receipt', required=True)
    resolved = BooleanField(default=False, required=True)


class Categories(Document):
    category_name = StringField(required=True, unique=True, min_length=3)


class BudgetRecord(Document):
    user_id = ReferenceField('User', required=True)
    category_id = ReferenceField('Categories', required=True)
    budget_amount = FloatField(required=True)


class ExpenseSummaryByReceipts(Document):
    user_id = ReferenceField('User', required=True)
    receipt_id_list = ListField(ReferenceField('Receipt', required=True))
    total_price = FloatField(required=True)
    title = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=50)
