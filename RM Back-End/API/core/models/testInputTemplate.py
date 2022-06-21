from flask_restx import reqparse, fields

# receipt data form
receipt_parser = reqparse.RequestParser()
receipt_parser.add_argument('TIN', location='form', type=str, required=True)
receipt_parser.add_argument('FS No', location='form', type=str, required=True)
receipt_parser.add_argument('Date', location='form', type=str, required=True)
receipt_parser.add_argument('Place', location='form', type=str, required=True)
receipt_parser.add_argument('Items', location='form', type=str, required=True)
receipt_parser.add_argument('Total', location='form', type=str, required=True)
receipt_parser.add_argument('Register ID', location='form', type=str, required=True)
receipt_parser.add_argument('Description', location='form', type=str, required=True)

login_model = {
    'email': fields.String,
    'password': fields.String,
}

items_model = {
    'name': fields.String,
    'quantity': fields.Float,
    'item_price': fields.Float
}

receipt_model = {
    'tin_number': fields.String,
    'fs_number': fields.String,
    'issued_date': fields.DateTime,
    'business_place_name': fields.String,
    'description': fields.String,
    'register_id': fields.String,
    'total_price': fields.Float,
}


def receipt_form(items):
    new_receipt_model = {
        'tin_number': fields.String,
        'fs_number': fields.String,
        'issued_date': fields.DateTime,
        'business_place_name': fields.String,
        'description': fields.String,
        'register_id': fields.String,
        "category_id": fields.String,
        'total_price': fields.Float,
        'Items': fields.List(
            fields.Nested(items)
        )
    }
    return new_receipt_model


receipt_identifier = {
    'receipt id': fields.String,
}


def expense_form(identifier):
    expense_template = {
        'receipt_list': fields.List(fields.Nested(identifier)),
        'title': fields.String,
        'note': fields.String,
    }

    return expense_template
