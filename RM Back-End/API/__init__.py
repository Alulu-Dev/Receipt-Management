from flask import Flask
from flask_mongoengine import MongoEngine
from .settings import MONGO_URI
from .apis import api as api_namespace

app = Flask(__name__)
# app.config['MONGODB_SETTINGS'] = {
#     'host': MONGO_URI,
#     'db': 'ReceiptManagement'
# }
app.config['MONGODB_SETTINGS'] = {
    'db': 'ReceiptManagement',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)
api_namespace.init_app(app)
app.run(debug=True)
