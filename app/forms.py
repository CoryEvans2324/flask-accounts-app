from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import TelField, EmailField


class SignIn(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignIn2FA(FlaskForm):
    code = StringField('2FA Code', validators=[DataRequired()])
