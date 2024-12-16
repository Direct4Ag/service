"""add cover crop table and alter sensors table

Revision ID: fdc61a8e5f29
Revises: 3460305f5ebe
Create Date: 2024-11-21 21:45:30.576959+00:00

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "fdc61a8e5f29"
down_revision = "3460305f5ebe"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cover_crop",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("crop", sa.String(length=50), nullable=True),
        sa.Column("planting_date", sa.Date(), nullable=False),
        sa.Column("planting_method", sa.String(length=100), nullable=True),
        sa.Column("seeding_rate", sa.Float(), nullable=True),
        sa.Column("seeding_rate_unit", sa.String(length=50), nullable=True),
        sa.Column("termination_date", sa.Date(), nullable=False),
        sa.Column("observed_cover_crop_biomass", sa.Float(), nullable=True),
        sa.Column("sampling_date", sa.Date(), nullable=True),
        sa.Column("predicted_cover_crop_biomass", sa.Float(), nullable=True),
        sa.Column("cover_crop_biomass_unit", sa.String(length=50), nullable=True),
        sa.Column("observed_CN_ratio", sa.Float(), nullable=True),
        sa.Column("predicted_CN_ratio", sa.Float(), nullable=True),
        sa.Column(
            "cover_crop_research_ref_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["cover_crop_research_ref_id"],
            ["research.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "sensors",
        sa.Column("research_ref_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.drop_constraint("sensors_field_ref_id_fkey", "sensors", type_="foreignkey")
    op.create_foreign_key(None, "sensors", "research", ["research_ref_id"], ["id"])
    op.drop_column("sensors", "field_ref_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sensors",
        sa.Column(
            "field_ref_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "sensors", type_="foreignkey")
    op.create_foreign_key(
        "sensors_field_ref_id_fkey", "sensors", "fields", ["field_ref_id"], ["id"]
    )
    op.drop_column("sensors", "research_ref_id")
    op.drop_table("cover_crop")
    # ### end Alembic commands ###