"""add_public_id_to_projects_tasks

Revision ID: 6287c4b72132
Revises: f6a3b7d2e5c8
Create Date: 2026-09-06 22:55:54.745626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '6287c4b72132'
down_revision: Union[str, None] = 'f6a3b7d2e5c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _generate_public_id() -> str:
    import secrets
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))


def upgrade() -> None:
    bind = op.get_bind()

    op.add_column('projects', sa.Column('public_id', sa.String(16), nullable=True))
    op.add_column('tasks', sa.Column('public_id', sa.String(16), nullable=True))

    projects = bind.execute(text('SELECT id FROM projects')).fetchall()
    for (project_id,) in projects:
        public_id = _generate_public_id()
        bind.execute(text('UPDATE projects SET public_id = :pid WHERE id = :id'), {'pid': public_id, 'id': project_id})

    tasks = bind.execute(text('SELECT id FROM tasks')).fetchall()
    for (task_id,) in tasks:
        public_id = _generate_public_id()
        bind.execute(text('UPDATE tasks SET public_id = :pid WHERE id = :id'), {'pid': public_id, 'id': task_id})

    op.alter_column('projects', 'public_id', existing_type=sa.String(16), nullable=False)
    op.alter_column('tasks', 'public_id', existing_type=sa.String(16), nullable=False)

    op.create_index('idx_projects_public_id', 'projects', ['public_id'], unique=True)
    op.create_index('idx_tasks_public_id', 'tasks', ['public_id'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_tasks_public_id', table_name='tasks')
    op.drop_index('idx_projects_public_id', table_name='projects')
    op.drop_column('tasks', 'public_id')
    op.drop_column('projects', 'public_id')
