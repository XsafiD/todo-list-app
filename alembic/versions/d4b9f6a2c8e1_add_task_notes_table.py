"""add task_notes table

Revision ID: d4b9f6a2c8e1
Revises: e5f1a8c3d9b7
Create Date: 2026-09-01

Tabel `task_notes` — catatan timeline proses di detail task.
Append-only (tambah + hapus); baris ikut terhapus bersama task
(FK CASCADE). Urutan tampil (terbaru dulu) ditangani NoteService.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4b9f6a2c8e1'
down_revision: Union[str, None] = 'e5f1a8c3d9b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('task_notes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('task_notes', schema=None) as batch_op:
        batch_op.create_index('idx_task_notes_task_id', ['task_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('task_notes', schema=None) as batch_op:
        batch_op.drop_index('idx_task_notes_task_id')
    op.drop_table('task_notes')
