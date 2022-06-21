import json
from tempfile import TemporaryDirectory

import requests
from PIL import Image
from flask import send_file
from werkzeug.utils import secure_filename

from ..receiptControl import receipt_image
from ..models import receiptDataModel, FraudReport


def report_illegal_receipts(receipt):
    """
    curl -X 'POST' \
          'http://127.0.0.1:5000/report/check/' \
          -H 'accept: application/json' \
          -H 'Content-Type: multipart/form-data' \
          -F 'receipt=@qoutes.png;type=image/png'
    """
    try:
        # file = request.files['receipt']
        # with TemporaryDirectory(prefix='file_holder') as tempdir:
        #     filename = secure_filename(file.filename)
        #     file.save(tempdir + '/' + filename)
        #     file_path = tempdir + "/" + file.filename
        # file = receipt.files['file']
        with TemporaryDirectory(prefix='response') as tempdir:
            filename = secure_filename(receipt.filename)
            receipt.save(tempdir + '/' + filename)
            file_path = tempdir + "/" + receipt.filename

            header1 = {'accept': 'application/json',
                       'Content-Type': 'multipart/form-data'
                       }
            header2 = 'Content-Type: multipart/form-data'
            payload = 'receipt=@'+file_path+';type=image/png'

            r = requests.post('http://127.0.0.1:9000/report/check/',
                              data=payload, headers=header1)

            return r.status_code
    except FileNotFoundError:
        return "Receipt could not found", 501


def check_legality_of_receipts():
    """
        tin-number, fs-number, register-id, total-price, issued-date
        """

    all_receipts = receiptDataModel.objects(fraud_check='unchecked')
    for receipt in all_receipts:
        payload = {
            "tin_number": receipt.tin_number,
            "register_id": receipt.register_id,
            "fs_number": receipt.fs_number,
            "issued_date": receipt.issued_date.strftime("%Y-%m-%d %H:%M:%S"),
            "total_price": receipt.total_price
        }
        response = requests.post('http://127.0.0.1:9000/fraud/check/',
                                 headers={
                                     'accept': 'application/json',
                                     'Content-Type': 'application/json'
                                 },
                                 data=json.dumps(payload))

        if response.status_code == 200:
            if response.json():
                receipt.update(set__fraud_check='checked')
                return 'chekced'
            else:
                new_fraud = FraudReport()
                new_fraud.user_id = receipt.owner
                new_fraud.receipt_id = receipt.id
                receipt.update(set__fraud_check='illegal')
                return 'illegal'

        return response.json()
