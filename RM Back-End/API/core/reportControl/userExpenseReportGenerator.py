import calendar
from datetime import date

from bson import ObjectId
from flask_login import current_user
from mongoengine import DoesNotExist

from ..models import (receiptDataModel, ExpenseSummaryByReceipts,
                      receiptItems, BudgetRecord, Categories, )


def create_receipts_summary(user, receipt_list, title, note):
    new_summary = ExpenseSummaryByReceipts()
    new_summary.user_id = user
    new_summary.title = title
    new_summary.description = note
    receipt_id_list = []
    total_price = 0
    for receipt in receipt_list:
        receipt_id = ObjectId(receipt['receipt id'])

        receipt = receiptDataModel.objects.get(owner=user,
                                               id=receipt_id)
        receipt_id_list.append(receipt.id)
        total_price += receipt.total_price

    new_summary.receipt_id_list = receipt_id_list
    new_summary.total_price = total_price
    new_summary.save()

    return str(new_summary.id), 200


def create_expense_budget(user, budget, category):
    try:
        budget = int(budget)
        if budget < 0:
            raise ValueError
        Categories.objects.get(id=category)
        try:
            current_budget = BudgetRecord.objects.get(user_id=user, category_id= ObjectId(category))
            current_budget.update(budget_amount=budget)
        except DoesNotExist:
            new_budget = BudgetRecord()
            new_budget.user_id = user
            new_budget.category_id = ObjectId(category)
            new_budget.budget_amount = budget
            new_budget.save()

        return "successful creation", 200
    except:
        return "creation of budget failed", 500


def get_user_budget(user):
    try:
        budgets = BudgetRecord.objects(user_id=user)
        list_of_budget = []
        for budget in budgets:
            data = {
                "category_name": budget.category_id.category_name,
                "amount": budget.budget_amount
            }
            list_of_budget.append(data)
        return list_of_budget, 200
    except:
        return "fetching budget failed", 500


def get_expense_reports(summary_id):
    summary = ExpenseSummaryByReceipts.objects.get(id=summary_id, user_id=current_user.id)
    receipts = []
    for receipt in summary.receipt_id_list:
        items = []
        all_items = receiptItems.objects(receipt_id=receipt.id)
        for item in all_items:
            data = {
                "name": item.name,
                "quantity": item.quantity,
                "price": item.item_price
            }
            items.append(data)
        receipt_data = {
            'shop': receipt.business_place_name,
            'total price': receipt.total_price,
            'items': items
        }
        receipts.append(receipt_data)

    data = {
        'title': summary.title,
        'note': summary.description,
        'total price': summary.total_price,
        'receipts': receipts
    }
    return data


def get_all_expense_reports(user):
    reports = ExpenseSummaryByReceipts.objects(user_id=user)
    result = []
    for report in reports:
        data = {
            'id': str(report.id),
            'title': report.title,
            'note': report.description,
            'total price': report.total_price,
        }
        result.append(data)

    return result


def get_summary_by_category(user):
    try:
        categories = Categories.objects()
        user_receipts = receiptDataModel.objects(owner=user)
        list_of_summary = []
        total_expense = 0
        current_month = date.today().month
        current_year = date.today().year
        monthly_expense = [
            {
                "name": "Jan",
                "Total": 0
            }, {
                "name": "Feb",
                "Total": 0
            }, {
                "name": "Mar",
                "Total": 0
            }, {
                "name": "Apr",
                "Total": 0
            }, {
                "name": "May",
                "Total": 0
            }, {
                "name": "Jun",
                "Total": 0
            }, {
                "name": "Jul",
                "Total": 0
            }, {
                "name": "Aug",
                "Total": 0
            }, {
                "name": "Sep",
                "Total": 0
            }, {
                "name": "Oct",
                "Total": 0
            }, {
                "name": "Nov",
                "Total": 0
            }, {
                "name": "Dec",
                "Total": 0
            }

        ]
        for category in categories:
            data = {
                "cat_id": str(category.id),
                "category_name": category.category_name,
                "count": 0,
                "spent": 0,
                "budget": 0,
            }
            list_of_summary.append(data)
        for receipt in user_receipts:
            receipt_category = receipt.category_id
            receipt_date = receipt.issued_date
            category_name = receipt_category.category_name
            total = receipt.total_price

            for category_expense in list_of_summary:
                if category_expense["category_name"] == category_name and current_year == receipt_date.year:
                    if current_month == receipt_date.month:
                        try:
                            budget = BudgetRecord.objects.get(user_id=user, category_id=category_expense["cat_id"])
                            budget_amount = budget.budget_amount
                        except DoesNotExist:
                            budget_amount = 0
                        category_expense['count'] = category_expense['count'] + 1
                        category_expense['spent'] = round(category_expense['spent'] + total, 2)
                        category_expense["budget"] = budget_amount
                        total_expense += total
            month = receipt_date.month
            monthly_expense[month - 1]['Total'] = round(monthly_expense[month - 1]['Total'] + total, 2)

        return {
                   "total_expense": round(total_expense, 2),
                   "list_of_summary": list_of_summary,
                   "monthly_expense": monthly_expense,
                   "current_month_expense": monthly_expense[current_month - 1]
               }, 200
    except:
        return "Oops! Something went wrong", 501


def get_details_of_summary_by_category(user, category_id):
    """
    :return {"total": 0, "budget": 0, receipts= [{"name": "shop", "date": date, "total_price": 0}]}
    """
    try:
        category_id = ObjectId(category_id)
        user_receipts = receiptDataModel.objects(owner=user, category_id=category_id)
        category = Categories.objects.get(id=category_id)
        category_name = category.category_name
        current_month = date.today().month
        current_year = date.today().year
        list_of_receipts = []
        total = 0
        try:
            budget = BudgetRecord.objects.get(user_id=user, category_id=category_id)
            budget_amount = budget.budget_amount
        except DoesNotExist:
            budget_amount = 0
        for receipt in user_receipts:
            receipt_date = receipt.issued_date
            if current_month == receipt_date.month and current_year == receipt_date.year:
                total += receipt.total_price
                data = {
                    "id": str(receipt.id),
                    "name": receipt.business_place_name,
                    "date": receipt_date.strftime('%B %d, %y'),
                    "total_price": receipt.total_price,
                }
                list_of_receipts.append(data)
        details = {
            "total": round(total, 2),
            "category_name": category_name,
            "date": str(calendar.month_name[current_month]) + " " + str(current_year),
            "budget": budget_amount,
            "receipts": list_of_receipts
        }
        return details
    except:
        return "Oops! Something went wrong", 501


def delete_expense_report(summary_id):
    summary = ExpenseSummaryByReceipts.objects.get(id=summary_id, user_id=current_user.id)
    summary.delete()
    return "deleted", 200


def get_categories():
    try:
        categories = Categories.objects()
        list_of_categories = []
        for category in categories:
            data= {
                "id": str(category.id),
                "name": category.category_name
            }
            list_of_categories.append(data)

        return list_of_categories, 200
    except:
        return "Oops! somethings went wrong", 500