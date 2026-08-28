"""Custom exception classes untuk aplikasi Dashboardku.

Custom exceptions memungkinkan handling error yang spesifik
dan memberikan pesan error yang jelas ke user.
"""
from typing import Optional


class BaseAppException(Exception):
    """Base exception untuk semua application exceptions.

    Attributes:
        message: Pesan error yang user-friendly
        status_code: HTTP status code
        payload: Additional data (untuk API response)
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        payload: Optional[dict] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> dict:
        """Convert exception ke dict untuk JSON response."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        rv['error'] = self.__class__.__name__
        return rv


class BusinessError(BaseAppException):
    """Error ketika business logic gagal.

    Digunakan untuk error yang diharapkan dalam alur bisnis
    (misalnya resource tidak ditemukan, validasi gagal).

    Status code default: 400 Bad Request
    """

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class ValidationError(BusinessError):
    """Error ketika input validation gagal."""

    def __init__(self, message: str = "Validasi gagal", errors: Optional[dict] = None):
        payload = {'errors': errors} if errors else None
        super().__init__(message, 400)
        if payload:
            self.payload.update(payload)


class ResourceNotFoundError(BusinessError):
    """Error ketika resource tidak ditemukan."""

    def __init__(self, message: str = "Resource tidak ditemukan"):
        super().__init__(message, 404)


class DuplicateResourceError(BusinessError):
    """Error ketika resource sudah ada (duplicate)."""

    def __init__(self, message: str = "Resource sudah ada"):
        super().__init__(message, 409)


class InvalidStateError(BusinessError):
    """Error ketika state transition tidak valid."""

    def __init__(self, message: str = "Transisi status tidak valid"):
        super().__init__(message, 400)
