"""AuthService — verifikasi kredensial Actor (User) via database.

Contract: validasi gagal → return None (bukan raise) agar controller bisa
membedakan "kredensial salah" (UX flash) dari error sistem.
"""
from app.models import User


class AuthService:
    """Operasi autentikasi user (stateless)."""

    def verify_login(self, username: str, password: str) -> User | None:
        """Return User bila username+password cocok, selain itu None."""
        user = User.get_by_username(username)
        if user is None or not user.verify_password(password):
            return None
        return user


auth_service = AuthService()
