"""change foreign key name

Revision ID: 558cd9fe79bc
Revises: 100839656a13
Create Date: 2024-07-22 17:29:45.539526+00:00

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "558cd9fe79bc"
down_revision = "100839656a13"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "crop_rotation",
        sa.Column(
            "crop_rot_research_ref_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
    )
    op.drop_constraint(
        "crop_rotation_research_ref_id_fkey", "crop_rotation", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "crop_rotation", "research", ["crop_rot_research_ref_id"], ["id"]
    )
    op.drop_column("crop_rotation", "research_ref_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "crop_rotation",
        sa.Column(
            "research_ref_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "crop_rotation", type_="foreignkey")
    op.create_foreign_key(
        "crop_rotation_research_ref_id_fkey",
        "crop_rotation",
        "research",
        ["research_ref_id"],
        ["id"],
    )
    op.drop_column("crop_rotation", "crop_rot_research_ref_id")
    # ### end Alembic commands ###