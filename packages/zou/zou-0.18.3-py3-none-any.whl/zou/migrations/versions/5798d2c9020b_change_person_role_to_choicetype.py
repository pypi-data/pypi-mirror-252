"""Change person.role to ChoiceType

Revision ID: 5798d2c9020b
Revises: 693cc511d28d
Create Date: 2024-01-12 16:34:19.194350

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "5798d2c9020b"
down_revision = "693cc511d28d"
branch_labels = None
depends_on = None

ROLE_TYPES = [
    ("user", "Artist"),
    ("admin", "Studio Manager"),
    ("supervisor", "Supervisor"),
    ("manager", "Production Manager"),
    ("client", "Client"),
    ("vendor", "Vendor"),
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.VARCHAR(length=30),
            type_=sqlalchemy_utils.types.choice.ChoiceType(ROLE_TYPES),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sqlalchemy_utils.types.choice.ChoiceType(ROLE_TYPES),
            type_=sa.VARCHAR(length=30),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
