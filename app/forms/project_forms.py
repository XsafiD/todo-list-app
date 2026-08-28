"""Form Project."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp

HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"


class ProjectForm(FlaskForm):
    """Dipakai untuk create & edit — field sama, cukup satu form."""

    name = StringField("Nama Project", validators=[
        DataRequired(message="Nama project wajib diisi."),
        Length(min=1, max=255, message="Nama maksimal 255 karakter."),
    ])
    color = StringField("Warna", validators=[
        DataRequired(message="Warna wajib diisi."),
        Regexp(HEX_COLOR_PATTERN, message="Format warna harus hex, mis. #3B82F6."),
    ], default="#3B82F6")
    icon = StringField("Ikon (nama Font Awesome)", validators=[
        Optional(),
        Length(max=50, message="Nama ikon maksimal 50 karakter."),
    ], description="Tanpa prefix, mis. briefcase")
