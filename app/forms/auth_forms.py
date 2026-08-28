"""Form autentikasi."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username wajib diisi.")])
    password = PasswordField("Password", validators=[DataRequired(message="Password wajib diisi.")])
