import uuid
from datetime import date  # noqa
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import CoverCropData, Research


class CoverCrop(Base):
    """The Cover Crop table contains the information about the Cover Crop."""

    __tablename__ = "cover_crop"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop: str = Column(String(50), nullable=True)

    planting_date: date = Column(Date, nullable=False)  # noqa: F811
    planting_method: str = Column(String(100), nullable=True)
    seeding_rate: float = Column(Float, nullable=True)
    seeding_rate_unit: str = Column(String(50), nullable=True)

    termination_date: date = Column(Date, nullable=False)  # noqa: F811

    cover_crop_research_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("research.id"),
        nullable=False,
    )

    research: "Research" = relationship(
        "Research",
        back_populates="cover_crop",
        foreign_keys=[cover_crop_research_ref_id],
    )

    cover_crop_data: "CoverCropData" = relationship(
        "CoverCropData",
        back_populates="cover_crop",
        cascade="all, delete",
    )
