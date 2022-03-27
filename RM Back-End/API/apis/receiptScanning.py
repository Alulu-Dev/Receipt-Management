from flask import request, send_file
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from tempfile import TemporaryDirectory

from ..core.receiptControl.imageScanning import scanner

api = Namespace('Receipt Scan', description='End point test for file scanning')

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

        # filename = secure_filename(file.filename)

        with TemporaryDirectory(prefix='file_holder') as tempdir:

            filename = secure_filename(file.filename)
            file.save(tempdir + '/' + filename)
            file_path = tempdir + "/" + file.filename
            # return send_file(scanner(file_path), mimetype='image/png')
            return scanner(file_path, file.filename, file.mimetype)

