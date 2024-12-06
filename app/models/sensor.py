import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Research


class Sensors(Base):
    "Table to map the sensors to the fields"
    __tablename__ = "sensors"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    depth: str = Column(String(200), nullable=True, default="")
    sensor_type: str = Column(String(200), nullable=True, default="")
    sensor_id: int = Column(Integer, nullable=False)

    research_ref_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("research.id"),
        nullable=False,
    )

    research: "Research" = relationship(
        "Research",
        back_populates="sensors",
        foreign_keys=[research_ref_id],
    )
