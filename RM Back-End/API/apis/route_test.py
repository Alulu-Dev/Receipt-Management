from flask_restx import Namespace, Resource
from core.DatabaseModel import User

api = Namespace('Test', description='End point test')


@api.route('/')
class TestRoute(Resource):
    @api.doc('First Route')
    def get(self):
        """List all cats"""
        user = User(
            username = "AluluSuperAdmin",
            first_name = "Eshtaol",
            last_name = "Girma",
            email = "westegb@gmail.com",
            password = "abc123",
            profile_picture = "..alulu.jpg",
            status = "Active",
            type = "SuperAdmin",
           
        )
        user.save()
        return "Running"

