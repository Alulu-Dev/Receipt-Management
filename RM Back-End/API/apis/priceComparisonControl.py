from flask import request
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ..core.priceComparison import price_compare, all_price_checks, price_check

api = Namespace('compare', description='Endpoint to management items price comparison')


@api.route('/<item_id>/')
class CreateUserVerificationRequest(Resource):
    @api.doc("compare all records for best price")
    @login_required
    def post(self, item_id):
        return price_compare(item_id, current_user.id)


@api.route('/results/')
class GetAllPreviousResults(Resource):
    @login_required
    def get(self):
        return all_price_checks(current_user.id)


@api.route('/results/<record_id>/')
class GetPreviousResults(Resource):
    @login_required
    def get(self, record_id):
        return price_check(record_id)
