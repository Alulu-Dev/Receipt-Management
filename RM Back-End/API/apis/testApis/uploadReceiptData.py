from flask import request
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

from ...core.models import receipt_form, items_model
from ...core.receiptControl import upload_receipt
from ...core.fraudChecker import report_fraud

api = Namespace('test-api', description='upload receipt for test purposes')

items_form = api.model('items', items_model)
receipt_form = api.model('new receipt', receipt_form(items_form))

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/upload/')
class TestUploadReceipt(Resource):
    @api.expect(receipt_form)
    def post(self):
        """
         create a mock data receipt
        """
        # return request.json
        return upload_receipt(request.json)


@api.route('/upload-to-ecra/')
class TestUploadReceiptToECRA(Resource):
    @api.expect(upload_parser)
    def post(self):
        """
         create a mock data receipt
        """
        # return request.json
        return report_fraud(request.files['file'])
