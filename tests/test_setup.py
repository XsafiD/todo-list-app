"""tests/test_setup.py — TC: setup awal (first-run) saat tabel users kosong."""
from app.extensions import db
from app.models import User


class TestSetupMode:
    """TC-01: Belum ada user → semua route redirect ke /auth/setup."""

    def test_setup_page_tampil_saat_users_kosong(self, bare_client):
        response = bare_client.get("/auth/setup")
        assert response.status_code == 200
        assert b"Buat Akun" in response.data

    def test_dashboard_redirect_ke_setup(self, bare_client):
        response = bare_client.get("/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/setup" in response.headers["Location"]

    def test_login_redirect_ke_setup(self, bare_client):
        response = bare_client.get("/auth/login", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/setup" in response.headers["Location"]

    def test_health_tetap_public_saat_setup_mode(self, bare_client):
        response = bare_client.get("/health")
        assert response.status_code == 200


class TestSetupSubmit:
    """TC-02: POST setup valid → user dibuat, tanpa auto-login."""

    def test_setup_berhasil_redirect_login_tanpa_session(self, bare_client):
        response = bare_client.post(
            "/auth/setup",
            data={"username": "admin", "password": "rahasia123", "confirm_password": "rahasia123"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]

        user = User.get_by_username("admin")
        assert user is not None
        assert user.verify_password("rahasia123")

        with bare_client.session_transaction() as sess:
            assert "user_id" not in sess  # tidak auto-login

    def test_login_bisa_langsung_setelah_setup(self, bare_client):
        bare_client.post(
            "/auth/setup",
            data={"username": "admin", "password": "rahasia123", "confirm_password": "rahasia123"},
        )
        response = bare_client.post(
            "/auth/login",
            data={"username": "admin", "password": "rahasia123"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

    def test_konfirmasi_password_tidak_cocok_ditolak(self, bare_client):
        response = bare_client.post(
            "/auth/setup",
            data={"username": "admin", "password": "rahasia123", "confirm_password": "beda12345"},
        )
        assert response.status_code == 200
        assert b"tidak cocok" in response.data
        assert db.session.query(User.id).first() is None

    def test_password_pendek_ditolak(self, bare_client):
        response = bare_client.post(
            "/auth/setup",
            data={"username": "admin", "password": "pendek", "confirm_password": "pendek"},
        )
        assert response.status_code == 200
        assert b"8-72 karakter" in response.data
        assert db.session.query(User.id).first() is None


class TestSetupMatinya:
    """TC-03: Setelah ada user → /auth/setup 404 permanen, alur normal."""

    def test_setup_404_setelah_ada_user(self, client):
        response = client.get("/auth/setup")
        assert response.status_code == 404

    def test_setup_post_404_setelah_ada_user(self, client):
        response = client.post(
            "/auth/setup",
            data={"username": "lain", "password": "rahasia123", "confirm_password": "rahasia123"},
        )
        assert response.status_code == 404
        assert User.get_by_username("lain") is None  # tidak ada user baru

    def test_dashboard_normal_redirect_login_setelah_ada_user(self, client):
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]
