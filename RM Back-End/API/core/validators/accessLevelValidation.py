from functools import wraps

from flask import request, current_app
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS


def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.type == "SuperAdmin": # or not current_user.type == "SuperAdmin":
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
