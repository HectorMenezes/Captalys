"""empty message

Revision ID: f7c886c6084d
Revises: 
Create Date: 2021-04-24 19:19:25.051290

"""
import sqlalchemy as sa
from alembic import op

from src.models.user import ProviderType

# revision identifiers, used by Alembic.
revision = 'f7c886c6084d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=False),
                    sa.Column("login", sa.String(100), nullable=False),
                    sa.Column("email", sa.String(100), nullable=True),
                    sa.Column("twitter_username", sa.String(20), nullable=True),
                    sa.Column('provider', sa.Enum(ProviderType), nullable=False))


def downgrade():
    op.drop_table('user')
    pass
