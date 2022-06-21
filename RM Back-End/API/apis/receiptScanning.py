from flask import request, send_file
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from tempfile import TemporaryDirectory
from flask_login import login_required, current_user

from ..core.receiptControl.imageScanning import scanner
from ..core.models import upload_receipt as receipt
from ..core.receiptControl import upload_receipt

api = Namespace('upload', description='End point test for file scanning')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/Scan')
class ReceiptScan(Resource):

    @api.expect(upload_parser)
    def post(self):
        """
        scan receipt image
        """
        if 'file' not in request.files:
            return "no file found"
        file = request.files['file']

        if file.filename == '':
            return 'no file found'

        with TemporaryDirectory(prefix='file_holder') as tempdir:

            filename = secure_filename(file.filename)
            file.save(tempdir + '/' + filename)
            file_path = tempdir + "/" + file.filename
            return scanner(file_path, file.filename, file.mimetype)


@api.route("/upload")
class ReceiptUpload(Resource):
    @login_required
    @api.expect(receipt)
    def post(self):
        """
        upload receipt data with image
        :return:
        """
        return upload_receipt(request, current_user.id)
