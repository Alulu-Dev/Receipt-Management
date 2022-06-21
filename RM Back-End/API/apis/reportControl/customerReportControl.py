from flask import request
from flask_cors import cross_origin
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from ...core.reportControl import (create_expense_report, get_expense_report, all_expense_report,
                                   delete_expense_report, summary_by_category, expense_budget,
                                   details_of_summary, get_user_budget, get_categories)
from ...core.models import expense_form, receipt_identifier

api = Namespace('summary', description='Endpoint to generate and control reports')

identifier = api.model("receipt identifier", receipt_identifier)
expense_model = api.model("expense", expense_form(identifier))


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


@api.route('/user-category-summary/')
class UserExpenseSummaryReport(Resource):
    @login_required
    def get(self):
        return summary_by_category(current_user.id)


@api.route('/user-category-details/<category>')
class UserExpenseSummaryDetail(Resource):
    @login_required
    def get(self, category):
        return details_of_summary(current_user.id, category)


@api.route('/user-add-budget/<category>/<budget>')
class UserExpenseBudget(Resource):
    @api.doc("Create a budget for an expense category")
    @login_required
    def post(self, category, budget):
        return expense_budget(current_user.id, budget, category)


@api.route("/user-budget")
class UserBudget(Resource):
    @api.doc("Get user budget record")
    @login_required
    def get(self):
        return get_user_budget(current_user.id)


@api.route("/categories")
class ExpenseCategories(Resource):
    @api.doc("Get all categories for expense")
    @login_required
    def get(self):
        return get_categories()