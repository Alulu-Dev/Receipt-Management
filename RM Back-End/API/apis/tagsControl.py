from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from ..core.receiptControl import (create_tag, add_tag, remove_tag, get_all_tags, get_all_items)

api = Namespace('tags', description='Endpoint to management tags aka formal names for products')


@api.route('/create/<tag_name>')
class CreateTag(Resource):
    @api.doc("Create A formal common name for products with standard spellings")
    @jwt_required()
    @cross_origin()
    def post(self, tag_name):
        return create_tag(tag_name)


@api.route('/add-tag/<tag>/<item>')
class AddTagToItem(Resource):
    @api.doc("Create a formal for items")
    @jwt_required()
    @cross_origin()
    def post(self, tag, item):
        return add_tag(tag, item)


@api.route('/remove-tag/<tag>/<item>')
class AddTagToItem(Resource):
    @api.doc("Remove a formal for items")
    @jwt_required()
    @cross_origin()
    def post(self, tag, item):
        return remove_tag(tag, item)


@api.route("/get/tags/")
class GetAllTags(Resource):
    @api.doc("Get all defined formal names")
    @jwt_required()
    @cross_origin()
    def get(self):
        return get_all_tags()


@api.route("/get/items/")
class GetAllItems(Resource):
    @api.doc("Get all items recorded")
    @jwt_required()
    @cross_origin()
    def get(self):
        return get_all_items()
