"""add users table

Revision ID: b3f8c1a5d9e2
Revises: a2546b8ec0d1
Create Date: 2026-08-27

Tabel `users` untuk autentikasi berbasis DB (migrasi Flask).
Skema 5 tabel lain TIDAK berubah.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b3f8c1a5d9e2'
down_revision: Union[str, None] = 'a2546b8ec0d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username', name='uq_users_username')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('idx_users_username', ['username'], unique=True)


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('idx_users_username')
    op.drop_table('users')
