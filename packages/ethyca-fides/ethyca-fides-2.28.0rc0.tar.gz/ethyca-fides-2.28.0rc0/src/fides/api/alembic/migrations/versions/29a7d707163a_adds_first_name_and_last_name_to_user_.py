"""adds first_name and last_name to user model

Revision ID: 29a7d707163a
Revises: 90070db16d05
Create Date: 2022-05-05 13:41:28.807920

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "29a7d707163a"
down_revision = "90070db16d05"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("fidesopsuser", sa.Column("first_name", sa.String(), nullable=True))
    op.add_column("fidesopsuser", sa.Column("last_name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("fidesopsuser", "last_name")
    op.drop_column("fidesopsuser", "first_name")
    # ### end Alembic commands ###
