from tempfile import TemporaryDirectory

import requests
from PIL import Image
from flask import send_file
from werkzeug.utils import secure_filename

from ..receiptControl import receipt_image


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


def check_legality_of_receipts(receipt):

    pass
