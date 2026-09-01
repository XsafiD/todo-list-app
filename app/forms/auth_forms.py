"""Form autentikasi."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username wajib diisi.")])
    password = PasswordField("Password", validators=[DataRequired(message="Password wajib diisi.")])


class SetupForm(FlaskForm):
    """Setup awal — buat akun pertama (hanya sekali, saat tabel user masih kosong)."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username wajib diisi."),
            Length(min=3, max=255, message="Username 3-255 karakter."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password wajib diisi."),
            Length(min=8, max=72, message="Password 8-72 karakter."),
        ],
    )
    confirm_password = PasswordField(
        "Konfirmasi Password",
        validators=[
            DataRequired(message="Konfirmasi password wajib diisi."),
            EqualTo("password", message="Konfirmasi password tidak cocok."),
        ],
    )
