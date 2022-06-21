from flask_restx import Namespace, Resource
from flask_login import login_required, current_user


from ...core.receiptControl import (request_verification, user_verification_request,
                                    check_receipt_verification_status)
from ...core.models import receipt_model, items_model

api = Namespace('request', description='Endpoint to management receipt data verification')

items_form = api.model('items', items_model)
receipt_form = api.model('receipt update', receipt_model)


@api.route('/<receipt_id>/')
class CreateUserVerificationRequest(Resource):
    @api.doc("Create a verification request for a receipt")
    @login_required
    def post(self, receipt_id):
        return request_verification(current_user.id, receipt_id)

    @login_required
    def get(self, receipt_id):
        return check_receipt_verification_status(receipt_id)


@api.route('/user/')
class DisplayUserVerificationRequests(Resource):
    @api.doc("Display requests this user has made along with it's status")
    @login_required
    def get(self):
        return user_verification_request(current_user)


