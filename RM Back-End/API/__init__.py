from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

from .settings import MONGO_URI, ALULU_APP_MONGO_DATABASE, APP_SECRET_KEY
# from .apis import api as api_namespace
from .apis import blueprint_v1 as api_v1, blueprint_v2 as api_v2
from .core.models import accountModel

app = Flask(__name__)

app.secret_key = APP_SECRET_KEY
app.config["JWT_SECRET_KEY"] = APP_SECRET_KEY

app.config['MONGODB_SETTINGS'] = {
    'db': ALULU_APP_MONGO_DATABASE,
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)
login_manager = LoginManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return accountModel.objects.get(id=user_id)
    except:
        pass


# api_namespace.init_app(app)
app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_blueprint(api_v2, url_prefix='/api/v2')

app.run(debug=True)
