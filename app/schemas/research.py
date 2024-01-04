"""Pydantic models for representing fields"""

from typing import List
import json

from pydantic import BaseModel

from app.schemas.field import FieldSummary


class ResearchBase(BaseModel):
    """Base model for researches"""

    id: str
    research_name: str
    research_area: str
    research_type: str


class ResearchSummaryInDB(ResearchBase):
    """Model for research in DB"""

    class Config:
        orm_mode = True


class ResearchSummary(ResearchSummaryInDB):
    pass


class ResearchDetailBase(ResearchBase):
    field_ref_id: str


class ResearchDetailInDB(ResearchDetailBase):
    # field: FieldDetails
    field: FieldSummary

    class Config:
        orm_mode = True


class ResearchDetails(ResearchDetailInDB):
    pass


class ResearchCreate(ResearchDetailBase):
    pass


class ResearchUpdate(ResearchDetailBase):
    pass
