"""empty message

Revision ID: f7c886c6084d
Revises: 
Create Date: 2021-04-24 19:19:25.051290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7c886c6084d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=False),
                    sa.Column("username", sa.String(100), nullable=False),
                    sa.Column("email", sa.String(100), nullable=True),
                    sa.Column("twitter", sa.String(20), nullable=True))


def downgrade():
    pass
