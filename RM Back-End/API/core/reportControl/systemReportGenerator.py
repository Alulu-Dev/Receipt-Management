from datetime import date
from ..models import accountModel, receiptDataModel, UserRequest, FraudReport


def total_uploaded_receipts():
    all_receipts = receiptDataModel.objects.all()

    return  len(all_receipts)


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
    data = {
        'January': 0,
        'February': 0,
        'March': 0,
        'April': 0,
        'May': 0,
        'June': 0,
        'July': 0,
        'August': 0,
        'September': 0,
        'October': 0,
        'November': 0,
        'December': 0
    }
    all_users = accountModel.objects()
    current_year = date.today().year
    for user in all_users:
        if user.status == "Active" or user.status == "Blocked":
            if user.data_created.year == current_year:
                month = user.data_created.month
                data[list(data)[month-1]] = data[list(data)[month-1]] + 1

    return data


def formatted_system_report():
    total_users = total_registered_users()
    monthly_count = users_count_per_month()
    total_receipts = total_uploaded_receipts()
    total_fraud = total_fraud_receipts_caught()
    total_request = total_request_unresolved()
    data = {
        "Total Users": total_users,
        "Total Receipts": total_receipts,
        "Total Fraud Case": total_fraud,
        "Total Requests": total_request,
        "monthly Registry": monthly_count,
    }

    return data
