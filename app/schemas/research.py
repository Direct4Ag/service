"""Pydantic models for representing fields"""

import uuid

from pydantic import BaseModel

from app.schemas.field import FieldDetails


class ResearchBase(BaseModel):
    """Base model for researches"""

    research_name: str
    research_area: str
    research_type: str
    research_pi: str
    research_contact_info: str
    research_introduction: str
    research_conclusion: str


class ResearchSummaryInDB(ResearchBase):
    """Model for research in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class ResearchSummary(ResearchSummaryInDB):
    pass


class ResearchDetailBase(ResearchBase):
    field_ref_id: uuid.UUID


class ResearchDetailInDB(ResearchDetailBase):
    field: FieldDetails
    # field: FieldSummary
    id: uuid.UUID

    class Config:
        orm_mode = True


class ResearchDetails(ResearchDetailInDB):
    pass


class ResearchCreate(ResearchDetailBase):
    pass


class ResearchUpdate(ResearchDetailBase):
    pass
