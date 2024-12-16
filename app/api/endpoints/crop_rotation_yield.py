from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.CropRotationSummary])
def read_crop_rotation(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve all crop rotation."""
    crop_rotation = crud.crop_rotation.get_multi(
        db, skip=skip, limit=limit, order_by=order_by
    )
    return crop_rotation


@router.get("/crop_rotation_details", response_model=List[schemas.CropRotationDetails])
def read_crop_rotation_details(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve crop rotation."""
    crop_rotation = crud.crop_rotation.get_multi(
        db, skip=skip, limit=limit, order_by=order_by
    )
    return crop_rotation


@router.get(
    "/by_research_id/{research_id}", response_model=List[schemas.CropRotationDetails]
)
def read_crop_rotation_by_research_id(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get crop rotation by research id."""
    crop_rotation = crud.crop_rotation.order_by(
        db.query(models.CropRotation).filter(
            models.CropRotation.crop_rot_research_ref_id == research_id
        ),
        order_by=["id"],
    ).all()
    if not crop_rotation:
        raise HTTPException(
            status_code=404,
            detail=f"Crop rotation not found for {research_id}",
        )
    return crop_rotation


@router.get("/by_id/{crop_rotation_id}", response_model=schemas.CropRotationDetails)
def read_crop_rotation_by_id(
    crop_rotation_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get crop rotation by id."""
    crop_rotation = crud.crop_rotation.get(db, id=crop_rotation_id)
    if not crop_rotation:
        raise HTTPException(
            status_code=404,
            detail=f"Crop rotation not found for {crop_rotation_id}",
        )
    return crop_rotation


@router.post("/", response_model=schemas.CropRotationDetails)
def create_crop_rotation(
    crop_rotation_in: schemas.CropRotationCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create new crop rotation."""
    crop_rotation = crud.crop_rotation.create(db, obj_in=crop_rotation_in)
    return crop_rotation


@router.delete("/{crop_rotation_id}", response_model=schemas.CropRotationDetails)
def delete_crop_rotation(
    crop_rotation_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete crop rotation."""
    crop_rotation = crud.crop_rotation.delete(db, id=crop_rotation_id)
    if not crop_rotation:
        raise HTTPException(
            status_code=404,
            detail=f"Crop rotation not found for {crop_rotation_id}",
        )
    return crop_rotation
