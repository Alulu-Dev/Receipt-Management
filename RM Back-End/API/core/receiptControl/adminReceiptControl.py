from tempfile import TemporaryDirectory
from PIL import Image
from flask import  send_file
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
from mongoengine import DoesNotExist

from ...core.receiptControl import (receipt_data, receipt_image,)
from ...core.models import receipt_model, items_model, accountModel

api = Namespace('receipt', description="admin receipt control endpoint")

items_form = api.model('items', items_model)
receipt_form = api.model('receipt update', receipt_model)


@api.route('/get_data/<receipt_id>/')
class GetReceiptData(Resource):
    @api.doc("Get receipt data")
    @jwt_required()
    @cross_origin()
    def get(self, receipt_id):
        try:
            return receipt_data(receipt_id)
        except DoesNotExist:
            return "Receipt could not found"


@api.route('/get_image/<receipt_id>/')
class GetReceiptData(Resource):
    @api.doc("Get receipt image")
    @jwt_required()
    @cross_origin()
    def get(self, receipt_id):
        try:
            current_user_id = get_jwt_identity()
            current_user = accountModel.objects.get(id=current_user_id)
            with TemporaryDirectory(prefix='response') as tempdir:
                raw_bytes = receipt_image(current_user.email, receipt_id)
                image = Image.open(raw_bytes).convert("RGB")
                image.save(tempdir + '/' + 'image.jpg')
                img = tempdir + "/" + 'image.jpg'
                return send_file(img, mimetype='image/png')
        except FileNotFoundError:
            return "Receipt could not found", 501

