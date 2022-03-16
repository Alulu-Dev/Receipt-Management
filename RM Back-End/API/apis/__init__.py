from flask_restx import Api
from .route_test import api as api1

api = Api(
    title='Testing Endpoints',
    version='1.0',
    description='To test the configuration settings',
)


api.add_namespace(api1)
