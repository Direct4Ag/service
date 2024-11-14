import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import CropRotation, DroughtResistantSeedYield, Field


class Research(Base):
    """
    The Research table contains the information about the research done on a field.
    The way the table is structured, we can have multiple researches on a field, but it is not the case for now.
    However, 2 same type of research can be done on different fields but the data will be different so we need to keep track of it
    by allowing same name of research on different fields.

    """

    __tablename__ = "research"

    id: str = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    research_name: str = Column(String(200), nullable=False)
    research_area: str = Column(String(200), nullable=False)
    research_type: str = Column(String(200), nullable=False)
    research_pi: str = Column(String(200), nullable=True, default="")
    research_contact_info: str = Column(String(200), nullable=True, default="")
    research_introduction: str = Column(String(400), nullable=True, default="")
    research_conclusion: str = Column(String(400), nullable=True, default="")

    field_ref_id: str = Column(
        UUID(as_uuid=True), ForeignKey("fields.id"), nullable=False
    )

    field: "Field" = relationship("Field", back_populates="researches")

    drought_resistant_seed_yield: List["DroughtResistantSeedYield"] = relationship(
        "DroughtResistantSeedYield", back_populates="research", cascade="all, delete"
    )

    crop_rotation: List["CropRotation"] = relationship(
        "CropRotation", back_populates="research", cascade="all, delete"
    )
