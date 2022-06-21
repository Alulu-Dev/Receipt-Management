from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from ...core.receiptControl import (receipt_update, item_update, all_verification_request, )
from ...core.models import receipt_model, items_model

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
    @jwt_required()
    @api.expect(receipt_form)
    @cross_origin()
    def put(self, receipt_id):
        return receipt_update(receipt_id, request.json)


@api.route('/update_item/<item_id>/')
class UpdateReceiptData(Resource):
    @api.doc("verify manually and update items details")
    @jwt_required()
    @api.expect(items_form)
    @cross_origin()
    def put(self, item_id):
        return item_update(item_id, request.json)
