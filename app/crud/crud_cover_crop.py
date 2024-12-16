import app.schemas as schemas
from app.crud.base import CRUDBase
from app.models import CoverCrop, CoverCropData


class CRUDCoverCrop(
    CRUDBase[CoverCrop, schemas.CoverCropCreate, schemas.CoverCropUpdate]
):
    def get_cover_crop_data(self, db, id: str):
        return self.order_by(
            db.query(CoverCropData).filter(CoverCropData.cover_crop_data_ref_id == id),
            order_by=["sampling_date"],
        ).all()


cover_crop = CRUDCoverCrop(CoverCrop)
