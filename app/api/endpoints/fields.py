from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.FieldSummary])
def read_field(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve fields."""
    fields = crud.field.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return fields


@router.get("/geojson", response_model=schemas.FieldGeoJSON)
def read_field_geojson(
    db: Session = Depends(deps.get_db),
) -> Any:
    """Retrieve fields."""
    fields_jeojson = crud.field.get_field_geojson(db)
    return fields_jeojson


@router.get("/field_details", response_model=List[schemas.FieldDetails])
def read_field_details(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Get a field by id."""
    fields = crud.field.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return fields


@router.get("/{field_id}", response_model=schemas.FieldDetails)
def read_field_by_id(
    field_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a field by id."""
    field = crud.field.get(db, id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail=f"Field not found: ${field_id}")
    return field


@router.get("/{field_id}/research", response_model=List[schemas.ResearchSummary])
def read_field_research(
    field_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the research for the given field id."""
    research = crud.field.get_research(db, id=field_id)
    return research


@router.post("/", response_model=schemas.FieldSummary)
def create_field(
    field_in: schemas.FieldCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create a new field."""
    field = crud.field.create(db, obj_in=field_in)
    return field


@router.delete("/{field_id}", response_model=schemas.FieldSummary)
def delete_field(
    field_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete a field."""
    field = crud.field.delete(db, id=field_id)
    return field
