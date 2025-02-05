"""new todo table

Revision ID: 87f476b34ec6
Revises: cba4d6770991
Create Date: 2024-10-25 15:59:00.809472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f476b34ec6'
down_revision: Union[str, None] = 'cba4d6770991'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=False)
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todos_description'), 'todos', ['description'], unique=False)
    op.create_index(op.f('ix_todos_id'), 'todos', ['id'], unique=False)
    op.create_index(op.f('ix_todos_title'), 'todos', ['title'], unique=False)
    op.create_table('todo_tag_association',
    sa.Column('todo_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['todo_id'], ['todos.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_tag_association')
    op.drop_index(op.f('ix_todos_title'), table_name='todos')
    op.drop_index(op.f('ix_todos_id'), table_name='todos')
    op.drop_index(op.f('ix_todos_description'), table_name='todos')
    op.drop_table('todos')
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    # ### end Alembic commands ###
