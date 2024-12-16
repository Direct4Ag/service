"""Pydantic models for representing Cover Crop"""

import uuid
from datetime import date
from typing import List

from pydantic import BaseModel

from app.schemas.cover_crop_data import CoverCropDataDetails
from app.schemas.research import ResearchSummary


class CoverCropBase(BaseModel):
    """Base model for Cover Crop"""

    crop: str

    planting_date: date
    planting_method: str
    seeding_rate: float
    seeding_rate_unit: str

    termination_date: date

    cover_crop_research_ref_id: uuid.UUID


class CoverCropSummaryInDB(CoverCropBase):
    """Model for Cover Crop in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class CoverCropSummary(CoverCropSummaryInDB):
    pass


class CoverCropDetailBase(CoverCropBase):
    cover_crop_research_ref_id: uuid.UUID


class CoverCropDetailInDB(CoverCropDetailBase):
    research: ResearchSummary
    cover_crop_data: List[CoverCropDataDetails]
    id: uuid.UUID

    class Config:
        orm_mode = True


class CoverCropDetails(CoverCropDetailInDB):
    pass


class CoverCropCreate(CoverCropDetailBase):
    pass


class CoverCropUpdate(CoverCropDetailBase):
    pass
