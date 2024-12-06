import uuid
from datetime import date

from pydantic import BaseModel


class CoverCropDataBase(BaseModel):
    """base model for CoverCropData base"""

    sampling_date: date
    observed_cover_crop_biomass: float
    predicted_cover_crop_biomass: float
    cover_crop_biomass_unit: str

    observed_CN_ratio: float
    predicted_CN_ratio: float


class CoverCropDataSummaryInDB(CoverCropDataBase):
    """Model for CoverCropData in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class CoverCropDataSummary(CoverCropDataSummaryInDB):
    pass


class CoverCropDataDetailBase(CoverCropDataBase):
    cover_crop_data_ref_id: uuid.UUID


class CoverCropDataDetailInDB(CoverCropDataDetailBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class CoverCropDataDetails(CoverCropDataDetailInDB):
    pass


class CoverCropDataCreate(CoverCropDataDetailBase):
    pass


class CoverCropDataUpdate(CoverCropDataDetailBase):
    pass
