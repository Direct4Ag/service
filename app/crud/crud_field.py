import json
from typing import List

from geoalchemy2.functions import ST_AsGeoJSON
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Field, Research, Sensors
from app.schemas import FieldCreate, FieldUpdate


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    def get_research(self, db: Session, id: str) -> List[Research]:
        return self.order_by(
            db.query(Research).filter(Research.field_ref_id == id),
            order_by=["research_area"],
        ).all()

    def get_sensors(self, db: Session, id: str) -> List[Sensors]:
        return self.order_by(
            db.query(Sensors).filter(Sensors.field_ref_id == id),
            order_by=["depth"],
        ).all()

    def get_field_geojson(self, db: Session) -> dict:
        # Use ST_AsGeoJSON function to convert the geometry column to GeoJSON
        query = db.query(
            Field.id,
            Field.field_name,
            ST_AsGeoJSON(Field.field_shape).label("shape_jeojson"),
        ).all()

        # Create and return GeoJSON response
        geojson_response = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": json.loads(row.shape_jeojson),
                    "properties": {
                        "id": str(row.id),
                        "name": row.field_name,
                        # Add more properties as needed
                    },
                    "id": i + 1,
                }
                for i, row in enumerate(query)
            ],
        }

        return geojson_response


field = CRUDField(Field)
