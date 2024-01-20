"""Add data to task

Revision ID: 306266361f4f
Revises: 98c90621cf58
Create Date: 2019-11-21 16:56:35.682543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "306266361f4f"
down_revision = "98c90621cf58"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_build_job_playlist_id"),
        "build_job",
        ["playlist_id"],
        unique=False,
    )
    op.drop_index("ix_login_log_created_at", table_name="login_log")
    op.add_column(
        "task",
        sa.Column(
            "data", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    op.alter_column(
        "task_type",
        "for_entity",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "task_type",
        "short_name",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(length=20),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "task_type",
        "short_name",
        existing_type=sa.String(length=20),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    op.alter_column(
        "task_type",
        "for_entity",
        existing_type=sa.String(length=30),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    op.drop_column("task", "data")
    op.create_index(
        "ix_login_log_created_at", "login_log", ["created_at"], unique=False
    )
    op.drop_index(op.f("ix_build_job_playlist_id"), table_name="build_job")
    # ### end Alembic commands ###
