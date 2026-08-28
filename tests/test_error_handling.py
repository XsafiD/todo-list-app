"""Test error handling - 404, 403, 500 pages."""
import pytest
from flask import session


def test_404_page(client):
    """Test 404 Not Found page rendering."""
    response = client.get('/path-yang-tidak-ada')
    assert response.status_code == 404
    assert b'Halaman Tidak Ditemukan' in response.data
    assert b'Kembali ke Beranda' in response.data


def test_500_page(client, app):
    """Test 500 Internal Server Error page rendering."""
    # Create a route that intentionally raises an exception
    @app.route('/test-500-error')
    def test_500():
        raise Exception("Test exception for 500 page")

    with app.test_client() as test_client:
        response = test_client.get('/test-500-error')
        assert response.status_code == 500
        assert b'Terjadi Kesalahan Server' in response.data
        assert b'Kembali ke Beranda' in response.data
        assert b'Refresh Halaman' in response.data


def test_500_page_with_error_details(client, app):
    """Test 500 page includes error details in debug mode."""
    @app.route('/test-500-with-details')
    def test_500_details():
        raise ValueError("Test ValueError with details")

    with app.test_client() as test_client:
        response = test_client.get('/test-500-with-details')
        assert response.status_code == 500
        # In debug mode, error details should be shown
        assert b'Detail Error' in response.data or b'ValueError' in response.data


def test_403_page(client, app):
    """Test 403 Forbidden page rendering."""
    # Create a route that raises 403
    from werkzeug.exceptions import Forbidden

    @app.route('/test-403')
    def test_403():
        raise Forbidden("Access denied")

    with app.test_client() as test_client:
        response = test_client.get('/test-403')
        assert response.status_code == 403
        assert b'Akses Ditolak' in response.data
        assert b'Kembali ke Beranda' in response.data


def test_404_page_design_system(client):
    """Test 404 page follows DESIGN.md styling."""
    response = client.get('/another-non-existent-path')
    assert response.status_code == 404
    # Check for design system elements
    assert b'fa-compass' in response.data  # Compass icon
    assert b'Halaman Tidak Ditemukan' in response.data


def test_500_page_design_system(client, app):
    """Test 500 page follows DESIGN.md styling."""
    @app.route('/test-500-design')
    def test_500_design():
        raise Exception("Design test")

    with app.test_client() as test_client:
        response = test_client.get('/test-500-design')
        assert response.status_code == 500
        # Check for design system elements
        assert b'fa-triangle-exclamation' in response.data  # Warning icon
        assert b'Butuh Bantuan?' in response.data
        assert b'Screenshot halaman ini' in response.data


def test_500_page_contact_support_info(client, app):
    """Test 500 page includes contact support information."""
    @app.route('/test-500-contact')
    def test_500_contact():
        raise Exception("Contact support test")

    with app.test_client() as test_client:
        response = test_client.get('/test-500-contact')
        assert response.status_code == 500
        # Check for contact support info
        assert b'Screenshot halaman ini' in response.data
        assert b'URL yang kamu akses' in response.data
        assert b'Waktu kejadian' in response.data


def test_error_page_home_button_redirects_correctly(client):
    """Test home button on error pages redirects correctly."""
    # Test 404
    response = client.get('/non-existent-page')
    assert b'Kembali ke Beranda' in response.data
    # The button should redirect to dashboard if logged in, or login if not
    # Since we're not logged in, it should redirect to auth.login
    assert b'auth/login' in response.data or b'main.dashboard' in response.data


def test_error_page_responsive_design(client):
    """Test error pages are responsive (mobile-friendly)."""
    # Test 404
    response = client.get('/mobile-404-test')
    assert response.status_code == 404
    # Check for responsive classes (Tailwind)
    assert b'min-h-' in response.data or b'flex' in response.data
    assert b'max-w-xl' in response.data or b'max-w-md' in response.data
