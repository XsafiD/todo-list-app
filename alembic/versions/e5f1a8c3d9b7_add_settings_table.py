"""add settings table

Revision ID: e5f1a8c3d9b7
Revises: c7e2f4a1b8d3
Create Date: 2026-08-28

Tabel `settings` key-value untuk konfigurasi aplikasi (toggle arsip
otomatis + state last run). Default `auto_archive_enabled` = false
ditangani di code (SettingService), tanpa seed data.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5f1a8c3d9b7'
down_revision: Union[str, None] = 'c7e2f4a1b8d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='uq_settings_name')
    )
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.create_index('idx_settings_name', ['name'], unique=True)


def downgrade() -> None:
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.drop_index('idx_settings_name')
    op.drop_table('settings')
