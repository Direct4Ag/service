import uuid
from datetime import date  # noqa
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import CoverCrop


class CoverCropData(Base):
    """Table to record covercrop data in a row"""

    __tablename__ = "cover_crop_data"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    sampling_date: date = Column(Date, nullable=False)  # noqa: F811
    observed_cover_crop_biomass: float = Column(Float, nullable=True)
    predicted_cover_crop_biomass: float = Column(Float, nullable=True)
    cover_crop_biomass_unit: str = Column(String(50), nullable=True)

    observed_CN_ratio: float = Column(Float, nullable=True)
    predicted_CN_ratio: float = Column(Float, nullable=True)

    cover_crop_data_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("cover_crop.id"),
        nullable=False,
    )

    cover_crop: "CoverCrop" = relationship(
        "CoverCrop",
        back_populates="cover_crop_data",
        foreign_keys=[cover_crop_data_ref_id],
    )
