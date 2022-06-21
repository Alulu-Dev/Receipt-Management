from functools import wraps
import jwt
from bson import ObjectId

from flask import request, current_app, jsonify
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from mongoengine import DoesNotExist

from ..models import accountModel, ActiveAdmins
from API.settings import APP_SECRET_KEY


def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not (current_user.account_type == "SuperAdmin" or current_user.account_type == "Admin"):
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def admin_login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return current_app.login_manager.unauthorized()
        try:
            data = jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
            current_admin = accountModel.objects.get(id=ObjectId(data['admin_id']))
            try:
                ActiveAdmins.objects.get(admin_id=current_admin.id)
            except DoesNotExist:
                return current_app.login_manager.unauthorized()
        except:
            return current_app.login_manager.unauthorized()

        return func(admin=current_admin, *args, **kwargs)
    return decorator
