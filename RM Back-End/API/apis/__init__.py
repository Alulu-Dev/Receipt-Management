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

from .sessionControl import admin_session, customer_session
from .accountControl import admin_account, customer_account
from .reportControl import admin_report, customer_report

blueprint_v1 = Blueprint('api_v1', __name__)
api_v1 = Api(
    blueprint_v1,
    title='Alulu API',
    version='1.0',
    description='Alulu Application Customers API',
)
api_v1.add_namespace(customer_session)
api_v1.add_namespace(customer_account)
api_v1.add_namespace(customer_receipt)
api_v1.add_namespace(customer_verification)
api_v1.add_namespace(customer_report)
api_v1.add_namespace(price_management)
api_v1.add_namespace(prediction_management)
api_v1.add_namespace(file_upload)
api_v1.add_namespace(file_scan)

api_v1.add_namespace(api_test)
api_v1.add_namespace(test_api)


blueprint_v2 = Blueprint('api_v2', __name__)
api_v2 = Api(
    blueprint_v2,
    title='Alulu API',
    version='2.0',
    description='Alulu Application Admins API',
)
api_v2.add_namespace(admin_session)
api_v2.add_namespace(admin_account)
api_v2.add_namespace(admin_receipt)
api_v2.add_namespace(admin_verification)
api_v2.add_namespace(admin_report)
api_v2.add_namespace(tags_management)