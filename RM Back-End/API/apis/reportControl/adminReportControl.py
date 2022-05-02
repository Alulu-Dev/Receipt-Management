from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ...core.reportControl import system_report, add_expense_category
from ...core.models import expense_form, receipt_identifier

api = Namespace('summary', description='Endpoint to generate and control reports')

identifier = api.model("receipt identifier", receipt_identifier)
expense_model = api.model("expense", expense_form(identifier))


@api.route('/system/')
class SystemUsageSummary(Resource):
    @api.doc('General Summary report generator')
    @jwt_required()
    @cross_origin()
    def get(self,):
        """
         create a mock data receipt
        """
        try:
            return system_report(), 200
        except:
            return "Report failed to be generated", 500


@api.route('/category/<name>')
class ExpenseCCategory(Resource):
    @api.doc('Create Summary Category')
    @jwt_required()
    @cross_origin()
    def post(self, name):
        return add_expense_category(name)
