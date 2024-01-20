"""create unique constraint project_id, field_name on MetadataDescriptor

Revision ID: 29df910f04a4
Revises: 8588f254d6b8
Create Date: 2022-11-04 13:46:15.819315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_utils import UUIDType, ChoiceType
from sqlalchemy.ext.declarative import declarative_base
from zou.migrations.utils.base import BaseMixin
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "29df910f04a4"
down_revision = "8588f254d6b8"
branch_labels = None
depends_on = None

base = declarative_base()


class Department(base, BaseMixin):
    """
    Studio department like modeling, animation, etc.
    """

    __tablename__ = "department"
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    color = sa.Column(sa.String(7), nullable=False)


department_metadata_descriptor_link = sa.Table(
    "department_metadata_descriptor_link",
    base.metadata,
    sa.Column(
        "metadata_descriptor_id",
        UUIDType(binary=False),
        sa.ForeignKey("metadata_descriptor.id"),
    ),
    sa.Column(
        "department_id", UUIDType(binary=False), sa.ForeignKey("department.id")
    ),
)


class MetadataDescriptor(base, BaseMixin):
    """
    This models allow to identify which metadata are available for a given
    project and a given entity type.
    """

    __tablename__ = "metadata_descriptor"

    project_id = sa.Column(
        UUIDType(binary=False),
        sa.ForeignKey("project.id"),
        nullable=False,
        index=True,
    )
    entity_type = sa.Column(sa.String(60), nullable=False, index=True)
    name = sa.Column(sa.String(120), nullable=False)
    field_name = sa.Column(sa.String(120), nullable=False)
    choices = sa.Column(postgresql.JSONB(astext_type=sa.Text()))
    for_client = sa.Column(sa.Boolean(), default=False, index=True)
    departments = orm.relationship(
        "Department", secondary=department_metadata_descriptor_link
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "project_id", "entity_type", "name", name="metadata_descriptor_uc"
        ),
    )


PROJECT_STYLES = [
    ("2d", "2D Animation"),
    ("3d", "3D Animation"),
    ("2d3d", "2D/3D Animation"),
    ("vfx", "VFX"),
    ("stop-motion", "Stop Motion"),
    ("motion-design", "Motion Design"),
    ("archviz", "Archviz"),
    ("commercial", "Commercial"),
    ("catalog", "Catalog"),
]


class Project(base, BaseMixin):
    __tablename__ = "project"

    name = sa.Column(sa.String(80), nullable=False, unique=True, index=True)
    code = sa.Column(sa.String(80))
    description = sa.Column(sa.Text())
    shotgun_id = sa.Column(sa.Integer)
    file_tree = sa.Column(postgresql.JSONB(astext_type=sa.Text()))
    data = sa.Column(postgresql.JSONB(astext_type=sa.Text()))
    has_avatar = sa.Column(sa.Boolean(), default=False)
    fps = sa.Column(sa.String(10))
    ratio = sa.Column(sa.String(10))
    resolution = sa.Column(sa.String(12))
    production_type = sa.Column(sa.String(20), default="short")
    production_style = sa.Column(ChoiceType(PROJECT_STYLES))
    start_date = sa.Column(sa.Date())
    end_date = sa.Column(sa.Date())
    man_days = sa.Column(sa.Integer)
    nb_episodes = sa.Column(sa.Integer, default=0)
    episode_span = sa.Column(sa.Integer, default=0)
    max_retakes = sa.Column(sa.Integer, default=0)
    is_clients_isolated = sa.Column(sa.Boolean(), default=False)

    project_status_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("project_status.id"), index=True
    )


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    distinct_metadata_descriptors = session.query(
        MetadataDescriptor.entity_type,
        MetadataDescriptor.project_id,
        MetadataDescriptor.field_name,
    ).distinct()
    for metadata_descriptor in distinct_metadata_descriptors:
        metadata_descriptors_found = (
            session.query(MetadataDescriptor)
            .filter_by(
                entity_type=metadata_descriptor.entity_type,
                project_id=metadata_descriptor.project_id,
                field_name=metadata_descriptor.field_name,
            )
            .all()
        )
        for metadata_descriptor_to_remove in metadata_descriptors_found[1:]:
            session.delete(metadata_descriptor_to_remove)
    session.commit()
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "metadata_descriptor_uc2",
        "metadata_descriptor",
        ["project_id", "entity_type", "field_name"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "metadata_descriptor_uc2", "metadata_descriptor", type_="unique"
    )
    # ### end Alembic commands ###
