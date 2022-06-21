from datetime import datetime

from mongoengine import DoesNotExist

from ..models import receiptDataModel, receiptItems, UserRequest


def delete_receipt_permanently(receipt):
    try:
        today = datetime.today()
        receipts = receiptDataModel.objects(deleted=True)

        for receipt in receipts:
            day = receipt.date_created_on
            delta = today - day
            if delta.days > 30:
                items = receiptItems.objects(receipt_id=receipt.id)
                for item in items:
                    item.delete()

                requests = UserRequest.objects(receipt_id=receipt.id)
                for request in requests:
                    request.delete()
                receipt.delete()
        return True

    except DoesNotExist:
        pass


def delete_receipt(receipt_id):
    try:
        receipt = receiptDataModel.objects.get(id=receipt_id)
        receipt.update(deleted=True)
        receipt.update(set__deleted_on=datetime.utcnow)
        return True, 200

    except:
        return "Data cannot be Removed", 500
