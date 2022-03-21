from flask_restx import reqparse, fields
from werkzeug.datastructures import FileStorage


# input data format for signup
signup_input_parser = reqparse.RequestParser()
signup_input_parser.add_argument('username', location='form', type=str, required=True)
signup_input_parser.add_argument('firstname', location='form', type=str, required=True)
signup_input_parser.add_argument('lastname', location='form', type=str, required=True)
signup_input_parser.add_argument('email', location='form', type=str, required=True)
signup_input_parser.add_argument('password', location='form', type=str, required=True)
signup_input_parser.add_argument('file', location='files', type=FileStorage, required=True)

# input data format for updating details
update_input_parser = reqparse.RequestParser()
update_input_parser.add_argument('username', location='form', type=str)
update_input_parser.add_argument('firstname', location='form', type=str)
update_input_parser.add_argument('lastname', location='form', type=str)
update_input_parser.add_argument('email', location='form', type=str)
update_input_parser.add_argument('password', location='form', type=str)
update_input_parser.add_argument('file', location='files', type=FileStorage)

# input data format for upgrading user access level
account_id_parser = reqparse.RequestParser()
account_id_parser.add_argument('userId', location='form', type=str, required=True)

# status change form
status = {
    'user': fields.String,
    'status': fields.String,
    'reason': fields.String,
}