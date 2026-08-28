"""Custom Jinja2 filters — format tanggal & waktu (locale Indonesia)."""
from datetime import datetime

BULAN_SINGKAT = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
}


def fmt_datetime(value: datetime | None) -> str:
    """27 Agu 2026 14:30 — None/empty jadi '-'."""
    if not value:
        return "-"
    return f"{value.day:02d} {BULAN_SINGKAT[value.month]} {value.year} {value.hour:02d}:{value.minute:02d}"


def fmt_date(value: datetime | None) -> str:
    """27 Agu 2026 — None/empty jadi '-'."""
    if not value:
        return "-"
    return f"{value.day:02d} {BULAN_SINGKAT[value.month]} {value.year}"


def register_filters(app) -> None:
    app.add_template_filter(fmt_datetime, name="fmt_datetime")
    app.add_template_filter(fmt_date, name="fmt_date")
