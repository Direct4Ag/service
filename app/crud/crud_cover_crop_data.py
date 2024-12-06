import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import CoverCropData


class CRUDCoverCropData(
    CRUDBase[CoverCropData, schemas.CoverCropDataCreate, schemas.CoverCropDataUpdate]
):
    pass


cover_crop_data = CRUDCoverCropData(CoverCropData)
