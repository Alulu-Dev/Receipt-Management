from flask import request
from flask_login import login_required, current_user
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from tempfile import TemporaryDirectory

from ..core.receiptControl.imageUploading import upload_image_to_drive
from ..core.validators import check_file

api = Namespace('Receipt Control', description='End point test for file uploading')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/upload/<receipt_id>/')
class ReceiptUpload(Resource):
    @api.expect(upload_parser)
    @login_required
    def post(self, receipt_id):
        """
        upload receipt image to the system
        """
        if check_file(request):
            file = request.files['file']
            with TemporaryDirectory(prefix='file_holder') as tempdir:
                filename = secure_filename(file.filename)
                file.save(tempdir + '/' + filename)
                file_path = tempdir + "/" + file.filename
                # return file.mimetype

                # 2nd step
                return upload_image_to_drive(current_user.email, receipt_id, file_path, file.mimetype)
        else:
            return False, 406


class ReceiptModification(Resource):
    @api.doc("Display a given receipt details")
    def get(self):
        return "Receipt detail"

    @api.doc("Allow editing of receipt remainder helper note,"
             "receipt details can't be edit by end user")
    def put(self):
        return "Receipt edited"

    @api.doc("Delete a given receipt from the user database")
    def delete(self):
        return "Receipt Deleted"
