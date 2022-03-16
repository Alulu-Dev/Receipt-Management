from flask_restx import Namespace, Resource
from ..core.DatabaseModel import User

api = Namespace('Test', description='End point test')


@api.route('/')
class TestRoute(Resource):
    @api.doc('First Route')
    def get(self):
        """List all cats"""
        # user = User(
        #     title="test-101",
        #     year=1998,
        #     rated='R'
        # )
        # user.save()
        return "Running"
