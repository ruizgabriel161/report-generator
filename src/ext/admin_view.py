
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from flask_simplelogin import get_username, is_logged_in, login_required
from werkzeug.security import generate_password_hash
from wtforms import PasswordField

from src.ext.database import db
from src.models import User

# Proteger o admin com login via Monkey Patch
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()


def is_admin_user():
    username = get_username()
    user = User.query.filter_by(username=username).first()
    return user is not None and user.signature == "admin"


class UserAdmin(sqla.ModelView):
    column_list = ["username", "signature"]
    form_columns = ["username", "signature"]

    def on_model_change(self, form, model, is_created):
        print(f"form:{form}, model:{model}, is_created{is_created}")
        if "password" in form.data and form.data["password"] is not None:
            model.password = generate_password_hash(form.data["password"])

    def is_accessible(self):
        return is_admin_user()


def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(UserAdmin(model=User, session=db.session))
