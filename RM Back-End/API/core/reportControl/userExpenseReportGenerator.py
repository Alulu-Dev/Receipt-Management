from ..models import receiptDataModel, ExpenseSummary, receiptItems


def create_receipts_summary(user, receipt_list, title, note):
    new_summary = ExpenseSummary()
    new_summary.user_id = user
    new_summary.title = title
    new_summary.description = note
    receipt_id_list = []
    total_price = 0
    for receipt in receipt_list:
        fs_number = receipt['fs number']
        register_id = receipt['register id']

        receipt = receiptDataModel.objects.get(owner=user,
                                               fs_number=fs_number,
                                               register_id=register_id)
        receipt_id_list.append(receipt.id)
        total_price += receipt.total_price

    new_summary.receipt_id_list = receipt_id_list
    new_summary.total_price = total_price
    new_summary.save()

    return get_expense_reports(new_summary.id), 200


def get_expense_reports(summary_id):
    summary = ExpenseSummary.objects.get(id=summary_id)
    receipts = []
    for receipt in summary.receipt_id_list:
        items = []
        all_items = receiptItems.objects(receipt_id=receipt.id)
        for item in all_items:
            data = {
                "name ": item.name,
                "quantity ": item.quantity,
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
    reports = ExpenseSummary.objects(user_id=user)
    result = []
    for report in reports:
        data = {
            'title': report.title,
            'note': report.description,
            'total price': report.total_price,
        }
        result.append(data)

    return result


def delete_expense_report(summary_id):
    summary = ExpenseSummary.objects.get(id=summary_id)
    summary.delete()
    return "deleted", 200
