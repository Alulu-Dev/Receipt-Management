from flask import request
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ..core.prediction import get_prediction

api = Namespace('predict', description='Endpoint to management future purchase probabilities')


@api.route('/items/')
class UserPreviousItems(Resource):
    @api.doc("""
                All recorded purchased items lists
                :return: list 
            """)
    @login_required
    def get(self):
        return get_prediction(current_user.id)
