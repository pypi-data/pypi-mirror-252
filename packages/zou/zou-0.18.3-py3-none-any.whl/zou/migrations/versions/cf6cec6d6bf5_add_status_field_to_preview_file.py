"""add status field to preview file

Revision ID: cf6cec6d6bf5
Revises: ffeed4956ab1
Create Date: 2021-01-18 23:16:58.046608

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "cf6cec6d6bf5"
down_revision = "ffeed4956ab1"
branch_labels = None
depends_on = None

STATUSES = [
    ("processing", "Processing"),
    ("ready", "Ready"),
    ("broken", "Broken"),
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "preview_file",
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(STATUSES),
            nullable=True,
            default="processing",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preview_file", "status")
    # ### end Alembic commands ###
