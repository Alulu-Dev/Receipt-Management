from flask_restx import Api
from .route_test import api as api_test
from .receiptUploader import api as file_upload
from .receiptScanning import api as file_scan
from .accountControl import api as account_management
from .sessionControl import session as session_management
from .tagsControl import api as tags_management
from .verificationControl import api as verification_management
from .receiptControl import api as receipt_management
from .reportControl import api as report_management
from .priceComparisonControl import api as price_management

# test endpoints
from .testApis.uploadReceiptData import api as test_api

api = Api(
    title='Testing Endpoints',
    version='1.0',
    description='To test the configuration settings',
)

api.add_namespace(session_management)
api.add_namespace(account_management)
api.add_namespace(report_management)
api.add_namespace(tags_management)
api.add_namespace(verification_management)
api.add_namespace(receipt_management)
api.add_namespace(price_management)

api.add_namespace(file_upload)
api.add_namespace(file_scan)

api.add_namespace(api_test)
api.add_namespace(test_api)
