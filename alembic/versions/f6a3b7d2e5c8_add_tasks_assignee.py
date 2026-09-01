"""add tasks.assignee

Revision ID: f6a3b7d2e5c8
Revises: d4b9f6a2c8e1
Create Date: 2026-09-01

Kolom `tasks.assignee` — Penanggung Jawab task (teks bebas,
bukan relasi; contoh "Divisi Ekraf"). Nullable: task tanpa
penanggung jawab tetap valid. Ditampilkan sebagai badge di
detail task.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f6a3b7d2e5c8'
down_revision: Union[str, None] = 'd4b9f6a2c8e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('assignee', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'assignee')
