from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Farm, Field
import app.schemas as schemas


class CRUDDataSource(CRUDBase[Farm, schemas.FarmCreate, schemas.FarmUpdate]):
    def get_fields(self, db: Session, id: str) -> List[Field]:
        return self.order_by(
            db.query(Field).filter(Field.farm_ref_id == id),
            order_by=["field_name"],
        ).all()


farm = CRUDDataSource(Farm)
