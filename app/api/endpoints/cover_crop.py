from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.CoverCropSummary])
def read_cover_crop(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve all cover crop."""
    cover_crop = crud.cover_crop.get_multi(
        db, skip=skip, limit=limit, order_by=order_by
    )
    print(cover_crop)
    return cover_crop


@router.get(
    "/by_research_id/{research_id}", response_model=List[schemas.CoverCropDetails]
)
def read_cover_crop_by_research_id(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get cover crop by research id."""
    cover_crop = crud.cover_crop.order_by(
        db.query(models.CoverCrop).filter(
            models.CoverCrop.cover_crop_research_ref_id == research_id
        ),
        order_by=["id"],
    ).all()
    if not cover_crop:
        raise HTTPException(
            status_code=404,
            detail=f"Cover crop not found for {research_id}",
        )
    return cover_crop


@router.get("/by_id/{cover_crop_id}", response_model=schemas.CoverCropDetails)
def read_cover_crop_by_id(
    cover_crop_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get cover crop by id."""
    cover_crop = crud.cover_crop.get(db, id=cover_crop_id)
    if not cover_crop:
        raise HTTPException(
            status_code=404,
            detail=f"Cover crop not found: {cover_crop_id}",
        )
    return cover_crop


@router.post("/", response_model=schemas.CoverCropDetails)
def create_cover_crop(
    cover_crop_in: schemas.CoverCropCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create new cover crop."""
    cover_crop = crud.cover_crop.create(db, obj_in=cover_crop_in)
    return cover_crop


@router.delete("/{cover_crop_id}", response_model=schemas.CoverCropDetails)
def delete_cover_crop(
    cover_crop_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete cover crop by id."""
    cover_crop = crud.cover_crop.delete(db, id=cover_crop_id)
    if not cover_crop:
        raise HTTPException(
            status_code=404,
            detail=f"Cover crop not found: {cover_crop_id}",
        )
    return cover_crop


@router.post("/data", response_model=schemas.CoverCropDataDetails)
def add_cover_crop_data(
    cover_crop_data_in: schemas.CoverCropDataCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Add cover crop data."""
    cover_crop_data = crud.cover_crop_data.create(db, obj_in=cover_crop_data_in)
    return cover_crop_data


@router.delete(
    "/data/{cover_crop_data_id}", response_model=schemas.CoverCropDataDetails
)
def delete_cover_crop_data(
    cover_crop_data_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete cover crop data."""
    cover_crop_data = crud.cover_crop_data.delete(db, id=cover_crop_data_id)
    if not cover_crop_data:
        raise HTTPException(
            status_code=404,
            detail=f"Cover crop data not found: {cover_crop_data_id}",
        )
    return cover_crop_data


@router.get("/{cover_crop_id}/data", response_model=List[schemas.CoverCropDataDetails])
def get_cover_crop_data(
    cover_crop_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get cover crop data."""
    cover_crop_data = crud.cover_crop.get_cover_crop_data(db, id=cover_crop_id)
    return cover_crop_data
