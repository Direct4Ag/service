"""Pydantic models for representing farms"""

import uuid

from pydantic import BaseModel


class FarmBase(BaseModel):
    """Base model for farms"""

    farm_name: str
    location_name: str


class FarmSummaryInDB(FarmBase):
    """Model for farms in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class FarmSummary(FarmSummaryInDB):
    pass


class FarmCreate(FarmBase):
    pass


class FarmUpdate(FarmBase):
    pass
