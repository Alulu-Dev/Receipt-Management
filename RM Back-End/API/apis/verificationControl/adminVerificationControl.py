from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from flask_login import login_required

from ...core.receiptControl import (receipt_update, item_update, all_verification_request, )
from ...core.models import receipt_model, items_model
from ...core.validators import  admin_login_required

api = Namespace('request', description='Endpoint to management receipt data verification')

items_form = api.model('items', items_model)
receipt_form = api.model('receipt update', receipt_model)


@api.route('/all/')
class DisplayVerificationRequests(Resource):
    @api.doc("Display request all user has sent along with it's status")
    @jwt_required()
    def get(self):
        return all_verification_request()


@api.route('/update_receipt/<receipt_id>/')
class UpdateReceiptData(Resource):
    @api.doc("verify manually and update receipt detail")
    @admin_login_required
    @api.expect(receipt_form)
    def put(self, receipt_id):
        return receipt_update(receipt_id, request)


@api.route('/update_item/<item_id>/')
class UpdateReceiptData(Resource):
    @api.doc("verify manually and update items details")
    @admin_login_required
    @api.expect(items_form)
    def put(self, receipt_id):
        return item_update(receipt_id, request)
