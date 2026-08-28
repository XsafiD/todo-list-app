"""add tasks.archived_at

Revision ID: c7e2f4a1b8d3
Revises: b3f8c1a5d9e2
Create Date: 2026-08-28

Kolom `archived_at` (datetime nullable) untuk fitur Arsip — task done
yang diarsipkan manual dari Kanban. NULL = task aktif (belum terarsip).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c7e2f4a1b8d3'
down_revision: Union[str, None] = 'b3f8c1a5d9e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archived_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_column('archived_at')
