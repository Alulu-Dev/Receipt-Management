from bson import ObjectId
import json
from datetime import datetime
from mongoengine import ValidationError
from ...core.validators import check_file
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from urllib3.exceptions import ResponseError

from ..models import receiptDataModel, receiptItems, accountModel, Categories
from ...core.receiptControl.imageUploading import upload_image_to_drive


def upload_receipt(receipt, user):
    # return receipt
    try:
        Categories.objects.get(id=ObjectId(receipt.form["category_id"]))

        new_receipt = receiptDataModel()
        new_receipt.owner = user
        new_receipt.tin_number = receipt.form['tin_number']
        new_receipt.fs_number = receipt.form['fs_number']
        new_receipt.issued_date = datetime.strptime(receipt.form['issued_date'], "%Y-%m-%d %H:%M:%S")
        new_receipt.business_place_name = receipt.form['business_place_name']
        new_receipt.description = receipt.form['description']
        new_receipt.register_id = receipt.form['register_id']
        new_receipt.category_id = ObjectId(receipt.form["category_id"])
        new_receipt.total_price = float(receipt.form['total_price'])
        new_receipt.save()

        new_receipt_id = new_receipt.id
        list_of_items = []
        items1 = receipt.form['Items'][1:]
        items2 = items1[:-1]
        itmes = items2.split("~")
        for item in itmes:
            if item != "~" or item[0] != "":
                res = item.split(",")
                item_object = receiptItems()
                item_object.receipt_id = new_receipt_id
                if len(res) == 1:
                    break
                print(res)
                for i in res[:-1]:
                    if "name" in i:
                        x = i.split(" ")
                        x.pop(0)
                        name = " ".join(x)
                        item_object.name = name
                        continue
                    if "quantity" in i:
                        x = i.split(" ")
                        item_object.quantity = float(x[-1])
                        continue
                    if "item_price" in i:
                        x = i.split(" ")
                        item_object.item_price = float(x[-1][:-1])
                        continue

                item_object.save()
                print(item_object.id)

                list_of_items.append(item_object.id)
        print(111)
        receiptDataModel.objects(id=new_receipt_id).update(
            set__items=list_of_items
        )
        print(13)

        user = accountModel.objects.get(id=user)
        user.update(set__receipt_count=(user.receipt_count + 1))

        # if check_file(receipt):
        file = receipt.files['file']
        with TemporaryDirectory(prefix='file_holder') as tempdir:
            filename = secure_filename(file.filename)
            file.save(tempdir + '/' + filename)
            file_path = tempdir + "/" + file.filename
            # return file.mimetype

            # 2nd step
            return upload_image_to_drive(user.email, new_receipt_id, file_path, file.mimetype)
        # else:
        #     return False, 406

    except ValidationError:
        return "receipt cannot be uploaded", 400
