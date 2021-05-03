"""repository

Revision ID: c09a21b13b0c
Revises: f7c886c6084d
Create Date: 2021-04-27 16:08:18.733355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c09a21b13b0c'
down_revision = 'f7c886c6084d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("repository",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
                    sa.Column("name", sa.String(100), nullable=False),
                    sa.Column("private", sa.Boolean, nullable=False),
                    sa.Column("created_at", sa.DateTime, nullable=False),
                    sa.Column("updated_at", sa.DateTime, nullable=False),
                    sa.Column("size", sa.Integer, nullable=False),
                    sa.Column("stars", sa.Integer, nullable=False),
                    sa.Column("watchers", sa.Integer, nullable=False))


def downgrade():
    op.drop_table('repository')
    pass
