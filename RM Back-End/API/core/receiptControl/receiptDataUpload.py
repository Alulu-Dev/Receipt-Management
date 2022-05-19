from bson import ObjectId
from mongoengine import ValidationError
from urllib3.exceptions import ResponseError

from ..models import receiptDataModel, receiptItems, accountModel, Categories


def upload_receipt(receipt, user):
    # return receipt
    try:
        Categories.objects.get(id=ObjectId(receipt["category_id"]))

        new_receipt = receiptDataModel()
        new_receipt.owner = user
        new_receipt.tin_number = receipt['tin_number']
        new_receipt.fs_number = receipt['fs_number']
        new_receipt.issued_date = receipt['issued_date']
        new_receipt.business_place_name = receipt['business_place_name']
        new_receipt.description = receipt['description']
        new_receipt.register_id = receipt['register_id']
        new_receipt.category_id = ObjectId(receipt["category_id"])
        new_receipt.total_price = receipt['total_price']
        new_receipt.save()

        receipt_id = new_receipt.id
        list_of_items = []

        for items in receipt['Items']:
            item = receiptItems()
            item.receipt_id = receipt_id
            item.name = items['name']
            item.quantity = items['quantity']
            item.item_price = items['item_price']
            item.save()

            list_of_items.append(item.id)

        receiptDataModel.objects(id=receipt_id).update(
            set__items=list_of_items
        )

        user = accountModel.objects.get(id=user)
        user.update(set__receipt_count=(user.receipt_count+1))

        return "Receipt data uploaded", 200

    except ValidationError:
        return "receipt cannot be uploaded", 400
