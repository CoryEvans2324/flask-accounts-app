from flask import (
    Blueprint,
    render_template,
    current_app
)

from flask_login import current_user, fresh_login_required, login_fresh

bp = Blueprint('core', __name__)

@bp.route('/')
def index():

    return render_template('index.html', fresh=login_fresh())

@bp.route('/test')
@fresh_login_required
def test():
    return 'OK'
