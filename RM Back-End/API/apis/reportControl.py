from flask import request
from flask_cors import cross_origin
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ..core.reportControl import (system_report, create_expense_report,
                                  get_expense_report, all_expense_report,
                                  delete_expense_report)
from ..core.models import expense_form, receipt_identifier
from ..core.validators import admin_role_required

api = Namespace('summary', description='Endpoint to generate and control reports')

identifier = api.model("receipt identifier", receipt_identifier)
expense_model = api.model("expense", expense_form(identifier))


@api.route('/system/')
class SystemUsageSummary(Resource):
    @api.doc('General Summary report generator')
    # @login_required
    # @admin_role_required
    @cross_origin()
    def get(self):
        """
         create a mock data receipt
        """
        try:
            return system_report(), 200
        except:
            return "Report failed to be generated", 500


@api.route('/user-expense/<report_id>')
class UserExpenseReport(Resource):
    @login_required
    def get(self, report_id):
        return get_expense_report(report_id)

    @login_required
    def delete(self, report_id):
        return delete_expense_report(report_id)


@api.route('/user-expense/')
class CreateUserExpenseReport(Resource):
    @api.expect(expense_model)
    @login_required
    def post(self):
        return create_expense_report(current_user.id,
                                     request.json['receipt_list'],
                                     request.json['title'],
                                     request.json['note'])

    @login_required
    def get(self, ):
        return all_expense_report(current_user.id)
