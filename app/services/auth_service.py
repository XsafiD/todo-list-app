"""AuthService — verifikasi kredensial & setup akun pertama Actor (User).

Contract: validasi login gagal → return None (bukan raise) agar controller
bisa membedakan "kredensial salah" (UX flash) dari error sistem.
Setup ulang gagal (sudah ada user) → raise ValueError.
"""
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User


class AuthService:
    """Operasi autentikasi user (stateless)."""

    def verify_login(self, username: str, password: str) -> User | None:
        """Return User bila username+password cocok, selain itu None."""
        user = User.get_by_username(username)
        if user is None or not user.verify_password(password):
            return None
        return user

    def has_any_user(self) -> bool:
        """True bila sudah ada minimal satu user (setup awal selesai)."""
        return db.session.query(User.id).first() is not None

    def create_first_user(self, username: str, password: str) -> User:
        """Buat user pertama (setup awal) — tanpa login otomatis.

        Raises:
            ValueError: sudah ada user (setup hanya sekali) — termasuk race
                double-submit yang kalah di unique constraint username.
        """
        if self.has_any_user():
            raise ValueError("Setup sudah dilakukan — akun pertama telah dibuat.")

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Setup sudah dilakukan — akun pertama telah dibuat.") from None
        return user


auth_service = AuthService()
