from bson import ObjectId
from mongoengine import ValidationError
from urllib3.exceptions import ResponseError

from ..models import receiptDataModel, receiptItems


def upload_receipt(receipt):
    # return receipt
    try:
        new_receipt = receiptDataModel()
        new_receipt.owner = ObjectId('6231c3773b3e717238f04daa')
        new_receipt.tin_number = receipt['tin_number']
        new_receipt.fs_number = receipt['fs_number']
        new_receipt.issued_date = receipt['issued_date']
        new_receipt.business_place_name = receipt['business_place_name']
        new_receipt.description = receipt['description']
        new_receipt.register_id = receipt['register_id']
        new_receipt.total_price = receipt['total_price']
        new_receipt.save()

        receipt_id = new_receipt.id
        list_of_items = []

        for items in receipt['Items']:
            print(str(type(items['quantity'])))
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
        # call fraud checker function
        return "Receipt data uploaded"

    except ValidationError:
        return "receipt cannot be uploaded"
