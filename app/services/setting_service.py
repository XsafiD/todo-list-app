"""SettingService — akses konfigurasi aplikasi (key-value, typed).

Kontrak return: `get` → `str | None`, `get_bool`/`get_int` → tipe dengan
default. `set` = upsert + commit (nilai str/bool/int dinormalisasi ke str).
"""
from app.extensions import db
from app.models import Setting

# ── Kunci setting yang dikenal — jaga sinkron dengan scheduler & UI ──
AUTO_ARCHIVE_ENABLED = "auto_archive_enabled"
AUTO_ARCHIVE_LAST_RUN_AT = "auto_archive_last_run_at"
AUTO_ARCHIVE_LAST_RUN_COUNT = "auto_archive_last_run_count"


class SettingService:
    """CRUD konfigurasi aplikasi (single-user)."""

    def get(self, name: str) -> str | None:
        row = db.session.scalar(db.select(Setting).where(Setting.name == name))
        return row.value if row else None

    def get_bool(self, name: str, default: bool = False) -> bool:
        value = self.get(name)
        if value is None:
            return default
        return value.lower() in {"1", "true", "yes"}

    def get_int(self, name: str, default: int = 0) -> int:
        value = self.get(name)
        try:
            return int(value) if value is not None else default
        except ValueError:
            return default

    def set(self, name: str, value: str | bool | int) -> None:
        """Upsert satu setting — bool → "true"/"false", int → str."""
        if isinstance(value, bool):
            normalized = "true" if value else "false"
        else:
            normalized = str(value)
        row = db.session.scalar(db.select(Setting).where(Setting.name == name))
        if row is None:
            db.session.add(Setting(name=name, value=normalized))
        else:
            row.value = normalized
        db.session.commit()


setting_service = SettingService()
