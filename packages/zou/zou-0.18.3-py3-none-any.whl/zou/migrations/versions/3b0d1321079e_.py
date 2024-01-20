"""Add replies column

Revision ID: 3b0d1321079e
Revises: 1e2d77a2f0c4
Create Date: 2021-11-03 23:32:15.720557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3b0d1321079e"
down_revision = "1e2d77a2f0c4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comment",
        sa.Column(
            "replies", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("comment", "replies")
    # ### end Alembic commands ###
