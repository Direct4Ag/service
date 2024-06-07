"""add drs yield table

Revision ID: 11252b877df4
Revises: d1d18f24e794
Create Date: 2024-04-25 18:33:22.716935+00:00

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "11252b877df4"
down_revision = "d1d18f24e794"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "drought_resistant_seed_yield",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("replicate", sa.Integer(), nullable=True),
        sa.Column("line", sa.String(length=200), nullable=False),
        sa.Column("planting_date", sa.Date(), nullable=False),
        sa.Column("harvest_date", sa.Date(), nullable=False),
        sa.Column("yield_amount", sa.Float(), nullable=False),
        sa.Column("research_ref_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["research_ref_id"],
            ["research.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("drought_resistant_seed_yield")
    # ### end Alembic commands ###
