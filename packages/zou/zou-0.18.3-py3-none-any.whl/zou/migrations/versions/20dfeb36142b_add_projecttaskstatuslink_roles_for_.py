"""Add ProjectTaskStatusLink.roles_for_board

Revision ID: 20dfeb36142b
Revises: 5798d2c9020b
Create Date: 2024-01-12 17:22:30.688955

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "20dfeb36142b"
down_revision = "5798d2c9020b"
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
    with op.batch_alter_table(
        "project_task_status_link", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "roles_for_board",
                sa.ARRAY(sqlalchemy_utils.types.choice.ChoiceType(ROLE_TYPES)),
                nullable=True,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "project_task_status_link", schema=None
    ) as batch_op:
        batch_op.drop_column("roles_for_board")

    # ### end Alembic commands ###
