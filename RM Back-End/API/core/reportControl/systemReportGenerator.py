from datetime import date

from mongoengine import ValidationError, NotUniqueError

from ..models import (accountModel, receiptDataModel, UserRequest, FraudReport,
                      Categories)


def total_uploaded_receipts():
    all_receipts = receiptDataModel.objects.all()

    return len(all_receipts)


def total_fraud_receipts_caught():
    all_fraud_cases = FraudReport.objects.all()

    return len(all_fraud_cases)


def total_request_unresolved():
    all_requests = UserRequest.objects()
    total = 0
    for request in all_requests:
        if not request.resolved:
            total += 1
    return total


def total_registered_users():
    all_users = accountModel.objects()
    total = 0

    for user in all_users:
        if user.status == "Active" or user.status == "Blocked":
            total += 1
    return total


def users_count_per_month():
    data = [
        {
            "name": "Jan",
            "Active User": 0
        }, {
            "name": "Feb",
            "Active User": 0
        }, {
            "name": "Mar",
            "Active User": 0
        }, {
            "name": "Apr",
            "Active User": 0
        },{
            "name": "May",
            "Active User": 0
        }, {
            "name": "Jun",
            "Active User": 0
        }, {
            "name": "Jul",
            "Active User": 0
        }, {
            "name": "Aug",
            "Active User": 0
        }, {
            "name": "Sep",
            "Active User": 0
        }, {
            "name": "Oct",
            "Active User": 0
        }, {
            "name": "Nov",
            "Active User": 0
        }, {
            "name": "Dec",
            "Active User": 0
        }

    ]
    all_users = accountModel.objects()
    current_year = date.today().year
    for user in all_users:
        if user.status == "Active" or user.status == "Blocked":
            if user.data_created.year == current_year and user.account_type != "SuperAdmin":
                month = user.data_created.month
                data[month - 1]['Active User'] = data[month - 1]['Active User'] + 1
                # data[list(data)[month - 1]] = data[list(data)[month - 1]] + 1

    return data


def formatted_system_report():
    total_users = total_registered_users()
    monthly_count = users_count_per_month()
    total_receipts = total_uploaded_receipts()
    total_fraud = total_fraud_receipts_caught()
    total_request = total_request_unresolved()
    data = {
        "Total Users": total_users - 1,
        "Total Receipts": total_receipts,
        "Total Fraud Case": total_fraud,
        "Total Requests": total_request,
        "monthly Registry": monthly_count,
    }

    return data


def add_expense_category(cat_name):
    try:
        category = Categories()
        category.category_name = cat_name
        category.save()
        return "Created category", 201
    except (ValidationError, NotUniqueError):
        return "creation failed", 500

