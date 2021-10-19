from flask import (
    Flask,
    session,
    redirect,
    request,
    url_for,
    current_app
)

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
# from flask_session import Session

from app import models

bcrypt = Bcrypt()
db = MongoEngine()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.settings.Config')

    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    # app.session_interface = MongoEngineSessionInterface(db)

    login_manager.login_view = 'user.signin'
    login_manager.refresh_view = 'user.signin2fa'

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    register_blueprints(app)

    return app

@login_manager.user_loader
def user_loader(user_id):
    return models.User.get(user_id)

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     session.update({'next': request.full_path})
#     if current_user.is_anonymous:
#         # Not logged in at all
#         return redirect(url_for('user.signin'))

#     # logged in but not fresh
#     return redirect(url_for('user.signin2fa'))

def register_blueprints(app: Flask):
    from app.views import (
        core,
        user
    )

    app.register_blueprint(core.bp)
    app.register_blueprint(user.bp)