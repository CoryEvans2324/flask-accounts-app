from flask import (
    Blueprint,
    flash,
    render_template,
    url_for,
    request,
    redirect,
    session
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_fresh,
    login_required,
    confirm_login
)

from is_safe_url import is_safe_url
import pyotp

from app import forms, models

bp = Blueprint('user', __name__, url_prefix='/u')

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = forms.SignIn()
    if form.validate_on_submit():

        u = models.User.objects(email=form.email.data).first()
        if not u:
            flash('Username or password is incorrect.', 'error')
            return render_template('user/signin.html', form=form)

        # The User provide a 2FA code to make the session fresh
        login_user(u, remember=True, fresh=False)

        return redirect(url_for('user.signin2fa'))

    return render_template('user/signin.html', form=form)

@bp.route('/2fa', methods=['GET', 'POST'])
@login_required
def signin2fa():
    next_url = session.pop('next', '/')
    if not is_safe_url(next_url):
        next_url = '/'

    if login_fresh():
        return redirect(next_url)

    form = forms.SignIn2FA()

    if form.validate_on_submit():
        # Check 2FA code
        
        confirm_login()
        session.permanent = True

        return redirect(next_url)
    
    return render_template('user/2fa.html', form=form)

@bp.route('/2fa-setup', methods=['GET', 'POST'])
@login_required
def setup2fa():
    user = models.User.objects.get(id=current_user.id)
    if not user.otpSecret:
        user.otpSecret = pyotp.random_base32()
        user.save()

    uri = pyotp.TOTP(
        s=user.otpSecret,
    ).provisioning_uri(name=user.email, issuer_name='ExampleIssuer')

    return render_template('user/setup-2fa.html', secret=user.otpSecret, uri=uri)

@bp.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect('/')

def generate_otpauth_uri(username, secret) -> str:
    return f'otpauth://totp/ExampleAppName:{username}?secret={secret}?issuer=ExampleIssuer'