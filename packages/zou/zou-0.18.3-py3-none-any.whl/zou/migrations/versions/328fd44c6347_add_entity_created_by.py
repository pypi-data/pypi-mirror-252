"""Add entity.created_by

Revision ID: 328fd44c6347
Revises: 269d41bfb73f
Create Date: 2023-12-17 23:07:37.629894

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "328fd44c6347"
down_revision = "269d41bfb73f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_by",
                sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                default=uuid.uuid4,
                nullable=True,
            )
        )
        batch_op.create_foreign_key(None, "person", ["created_by"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("entity", schema=None) as batch_op:
        batch_op.drop_constraint("entity_created_by_fkey", type_="foreignkey")
        batch_op.drop_column("created_by")

    # ### end Alembic commands ###
