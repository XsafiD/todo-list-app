"""Instance Flask extensions — dibuat di sini, di-init via init_app di application factory."""
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
