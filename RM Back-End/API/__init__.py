from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from .settings import MONGO_URI, ALULU_APP_MONGO_DATABASE
from .apis import api as api_namespace

from .core.models import accountModel

app = Flask(__name__)

app.secret_key = 'alule-dev'

app.config['MONGODB_SETTINGS'] = {
    'db': ALULU_APP_MONGO_DATABASE,
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return accountModel.objects.get(id=user_id)


api_namespace.init_app(app)

app.run(debug=True)
