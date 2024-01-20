"""Add data field on entity links

Revision ID: 6eeaff945706
Revises: addbbefa7028
Create Date: 2022-04-08 16:17:32.473332

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6eeaff945706"
down_revision = "addbbefa7028"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "entity_link",
        sa.Column(
            "data", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("entity_link", "data")
    # ### end Alembic commands ###
