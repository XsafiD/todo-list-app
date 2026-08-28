"""tests/test_auth.py — TC: autentikasi (login, proteksi, logout)."""


class TestAuthLogin:
    """TC-01: Login berhasil & gagal."""

    def test_login_page_tanpa_session_tampil(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"Masuk" in response.data

    def test_login_kredensial_salah_flash_error(self, client):
        response = client.post("/auth/login", data={"username": "tester", "password": "salah"})
        assert response.status_code == 200
        assert b"Username atau password salah" in response.data

    def test_login_berhasil_redirect_dashboard(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "tester", "password": "pass12345"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

    def test_login_sudah_login_redirect_dashboard(self, client, login_user):
        response = client.get("/auth/login", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["Location"] == "/"


class TestAuthProteksi:
    """TC-02: Endpoint dilindungi redirect ke login bila belum ada session."""

    def test_dashboard_tanpa_login_redirect(self, client):
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]

    def test_project_list_tanpa_login_redirect(self, client):
        response = client.get("/projects/", follow_redirects=False)
        assert response.status_code == 302

    def test_task_list_tanpa_login_redirect(self, client):
        response = client.get("/tasks/", follow_redirects=False)
        assert response.status_code == 302


class TestAuthLogout:
    """TC-03: Logout menghapus session."""

    def test_logout_redirect_login(self, client, login_user):
        response = client.post("/auth/logout", follow_redirects=False)
        assert response.status_code == 302
        # Session hilang → akses berikutnya diminta login lagi
        follow = client.get("/", follow_redirects=False)
        assert "/auth/login" in follow.headers["Location"]
