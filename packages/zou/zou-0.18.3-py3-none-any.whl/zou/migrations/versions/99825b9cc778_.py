"""empty message

Revision ID: 99825b9cc778
Revises: f0567e8d0c62
Create Date: 2018-05-17 03:45:15.913755

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "99825b9cc778"
down_revision = "f0567e8d0c62"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notification",
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("read", sa.Boolean(), nullable=False),
        sa.Column("change", sa.Boolean(), nullable=False),
        sa.Column(
            "person_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "author_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "comment_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "task_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["person.id"],
        ),
        sa.ForeignKeyConstraint(
            ["comment_id"],
            ["comment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["person.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "person_id", "author_id", "comment_id", name="notification_uc"
        ),
    )
    op.create_index(
        op.f("ix_notification_author_id"),
        "notification",
        ["author_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_comment_id"),
        "notification",
        ["comment_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_person_id"),
        "notification",
        ["person_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_task_id"),
        "notification",
        ["task_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notification_task_id"), table_name="notification")
    op.drop_index(op.f("ix_notification_person_id"), table_name="notification")
    op.drop_index(
        op.f("ix_notification_comment_id"), table_name="notification"
    )
    op.drop_index(op.f("ix_notification_author_id"), table_name="notification")
    op.drop_table("notification")
    # ### end Alembic commands ###
