from flask_restx import Namespace, Resource

from ..core.receiptControl import (create_tag, add_tag, remove_tag)

api = Namespace('tags', description='Endpoint to management tags aka formal names for products')


@api.route('/create/<tag_name>/')
class CreateTag(Resource):
    @api.doc("Create A formal common name for products with standard spellings")
    def post(self, tag_name):
        return tag_name


@api.route('/create/<tag_name>/')
class CreateTag(Resource):
    @api.doc("Create A formal common name for products with standard spellings")
    def post(self, tag_name):
        return create_tag(tag_name)
    
    
@api.route('/tag/add/<tag>/<item>/')
class AddTagToItem(Resource):
    @api.doc("Create a formal for items")
    def post(self, tag, item):
        add_tag(tag, item)
        
@api.route('/tag/remove/<tag>/<item>/')
class AddTagToItem(Resource):
    @api.doc("Create a formal for items")
    def post(self, tag, item):
        return remove_tag(tag, item)