from flask import request
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ..core.priceComparison import (price_compare, all_price_checks, price_check, get_all_item,
                                    update_comparison, delete_comparison)

api = Namespace('compare', description='Endpoint to management items price comparison')


@api.route('/items/')
class ComparableItems(Resource):
    @api.doc("""
                All recorded comparable items lists
                :return: list 
            """)
    @login_required
    def get(self):
        return get_all_item()


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
        return price_check(record_id, current_user.id)

    @login_required
    def put(self, record_id):
        return update_comparison(record_id, current_user.id)

    @login_required
    def delete(self, record_id):
        return delete_comparison(record_id, current_user)
