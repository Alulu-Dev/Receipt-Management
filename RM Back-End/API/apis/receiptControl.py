from tempfile import TemporaryDirectory
from PIL import Image
from flask import request, send_file
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource
from mongoengine import ValidationError, DoesNotExist

from ..core.receiptControl import (receipt_data, receipt_image, all_receipt,
                                   delete_receipt)
from ..core.models import receipt_model, items_model

api = Namespace('receipt', description="Endpoint to control receipt records")

items_form = api.model('items', items_model)
receipt_form = api.model('receipt update', receipt_model)


@api.route('/')
class GetAllReceipt(Resource):
    @api.doc("Get all receipts")
    @login_required
    def get(self):
        """
        Get all receipts under a given user
        """
        try:
            return all_receipt(current_user.id)
        except DoesNotExist:
            return "Receipt could not found"


@api.route('/get_data/<receipt_id>/')
class GetReceiptData(Resource):
    @api.doc("Get receipt data")
    @login_required
    def get(self, receipt_id):
        try:
            return receipt_data(receipt_id)
        except DoesNotExist:
            return "Receipt could not found"


@api.route('/get_image/<receipt_id>/')
class GetReceiptData(Resource):
    @api.doc("Get receipt image")
    @login_required
    def get(self, receipt_id):
        try:
            with TemporaryDirectory(prefix='response') as tempdir:
                raw_bytes = receipt_image(current_user.username, receipt_id)
                image = Image.open(raw_bytes).convert("RGB")
                image.save(tempdir + '/' + 'image.jpg')
                img = tempdir + "/" + 'image.jpg'
                return send_file(img, mimetype='image/png')
        except FileNotFoundError:
            return "Receipt could not found", 501


@api.route('/delete/<receipt_id>/')
class DeleteReceipt(Resource):
    @api.doc("Delete receipt")
    @login_required
    def delete(self, receipt_id):
        try:
            return delete_receipt(receipt_id)
        except DoesNotExist:
            return "Receipt could not found"
