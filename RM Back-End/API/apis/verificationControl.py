from tempfile import TemporaryDirectory
from PIL import Image
from flask import request, send_file
from flask_restx import Namespace, Resource
from flask_login import login_required, current_user
from mongoengine import ValidationError

from ..core.receiptControl import (receipt_data, receipt_image, receipt_update, item_update,
                                   request_verification, user_verification_request,
                                   all_verification_request, check_receipt_verification_status)
from ..core.models import receipt_model, items_model
from ..core.validators import admin_role_required

api = Namespace('request', description='Endpoint to management receipt data verification')

items_form = api.model('items', items_model)
receipt_form = api.model('receipt update', receipt_model)


@api.route('/<receipt_id>/')
class CreateUserVerificationRequest(Resource):
    @api.doc("Create a verification request for a receipt")
    @login_required
    def post(self, receipt_id):
        return request_verification(current_user.id, receipt_id)

    def get(self, receipt_id):
        return check_receipt_verification_status(receipt_id)


@api.route('/user/')
class DisplayUserVerificationRequests(Resource):
    @api.doc("Display requests this user has made along with it's status")
    @login_required
    def get(self):
        return user_verification_request(current_user)


@api.route('/all/')
class DisplayVerificationRequests(Resource):
    @api.doc("Display request all user has sent along with it's status")
    @login_required
    @admin_role_required
    def get(self):
        return all_verification_request()


@api.route('/get_data/<receipt_id>/')
class GetReceiptData(Resource):
    @api.doc("Get receipt data")
    def get(self, receipt_id):
        try:
            return receipt_data(receipt_id)
        except ValidationError:
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


@api.route('/update_receipt/<receipt_id>/')
class UpdateReceiptData(Resource):
    @api.doc("verify manually and update receipt detail")
    @login_required
    @admin_role_required
    @api.expect(receipt_form)
    def put(self, receipt_id):
        return receipt_update(receipt_id, request)


@api.route('/update_item/<item_id>/')
class UpdateReceiptData(Resource):
    @api.doc("verify manually and update items details")
    @login_required
    @admin_role_required
    @api.expect(items_form)
    def put(self, receipt_id):
        return item_update(receipt_id, request)