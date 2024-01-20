"""Add PreviewBackground

Revision ID: c49e41f1298b
Revises: 7748d3d22925
Create Date: 2023-11-09 13:40:21.446542

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "c49e41f1298b"
down_revision = "7748d3d22925"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "preview_background_file",
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("archived", sa.Boolean(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=True),
        sa.Column("original_name", sa.String(length=250), nullable=True),
        sa.Column("extension", sa.String(length=6), nullable=True),
        sa.Column("file_size", sa.BigInteger(), nullable=True),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "preview_background_file", schema=None
    ) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_preview_background_file_is_default"),
            ["is_default"],
            unique=False,
        )

    op.create_table(
        "project_preview_background_file_link",
        sa.Column(
            "project_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "preview_background_file_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["preview_background_file_id"],
            ["preview_background_file.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("project_id", "preview_background_file_id"),
    )
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "default_preview_background_file_id",
                sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                default=uuid.uuid4,
                nullable=True,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_project_default_preview_background_file_id"),
            ["default_preview_background_file_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            None,
            "preview_background_file",
            ["default_preview_background_file_id"],
            ["id"],
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.drop_constraint(
            "project_default_preview_background_file_id_fkey",
            type_="foreignkey",
        )
        batch_op.drop_index(
            batch_op.f("ix_project_default_preview_background_file_id")
        )
        batch_op.drop_column("default_preview_background_file_id")

    op.drop_table("project_preview_background_file_link")
    with op.batch_alter_table(
        "preview_background_file", schema=None
    ) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_preview_background_file_is_default")
        )

    op.drop_table("preview_background_file")
    # ### end Alembic commands ###
