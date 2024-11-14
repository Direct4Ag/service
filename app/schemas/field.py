"""Pydantic models for representing fields"""

import json
import uuid
from typing import List

from geoalchemy2 import WKBElement
from pydantic import BaseModel, Field, validator

from app.schemas.farm import FarmSummary


class FieldBase(BaseModel):
    """Base model for fields"""

    field_name: str
    coordinates: List[float] = Field(min_items=2, max_items=2)

    @validator("coordinates", pre=True)
    def to_point(cls, value: WKBElement) -> List[float]:
        """Convert the WKBElement received from SQLAlchemy to a list of long and lat."""
        return json.loads(value.data)["coordinates"]


class FieldSummaryInDB(FieldBase):
    """Model for farms in DB"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class FieldSummary(FieldSummaryInDB):
    pass


class FieldDetailBase(FieldBase):
    farm_ref_id: uuid.UUID


class FieldDetailInDB(FieldDetailBase):
    farm: FarmSummary
    id: uuid.UUID

    class Config:
        orm_mode = True


class FieldDetails(FieldDetailInDB):
    pass


# class FieldCreate(FieldDetailBase):
#     field_shape: str


class FieldCreate(BaseModel):
    """Model for creating fields"""

    field_name: str
    coordinates: str
    farm_ref_id: uuid.UUID
    field_shape: str


class FieldUpdate(FieldDetailBase):
    field_shape: str


class FieldGeoJSON(BaseModel):
    """Model for fields in GeoJSON format"""

    type: str = "FeatureCollection"
    features: List[dict]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NitrateConcentrationGeostreamsData(BaseModel):
    """Model for Geostreams data"""

    nitrate_concentration_data: list
    year: int

    class Config:
        arbitrary_types_allowed = True


class SoilMoistureGeostreamsData(BaseModel):
    """Model for Geostreams data"""

    depth_soil_moisture_data: dict

    class Config:
        arbitrary_types_allowed = True


class WeatherGeostreamsData(BaseModel):
    """Model for Geostreams data"""

    weather_data: dict

    class Config:
        arbitrary_types_allowed = True


class Years(BaseModel):
    """Model for Geostreams data"""

    years: list

    class Config:
        arbitrary_types_allowed = True
