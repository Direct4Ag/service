import uuid

from pydantic import BaseModel

from app.schemas.research import ResearchDetails


class SensorBase(BaseModel):
    """Base model for sensors"""

    depth: str
    sensor_type: str
    sensor_id: int


class SensorSummaryInDB(SensorBase):
    """Model for sensors in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class SensorSummary(SensorSummaryInDB):
    pass


class SensorDetailBase(SensorBase):
    research_ref_id: uuid.UUID


class SensorDetailInDB(SensorDetailBase):
    research: ResearchDetails
    id: uuid.UUID

    class Config:
        orm_mode = True


class SensorDetails(SensorDetailInDB):
    pass


class SensorCreate(SensorDetailBase):
    pass


class SensorUpdate(SensorDetailBase):
    pass
