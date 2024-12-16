import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_all_fields(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/fields/all")
    assert response.status_code == 200


def test_read_field_geojson(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/fields/geojson")
    assert response.status_code == 200


def test_read_field_details(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/fields/field_details")
    assert response.status_code == 200


# [0, 1] are the skip values to skip certain number of records
# This checks for the first 2 records
@pytest.mark.parametrize(
    "skip",
    [
        0,
        1,
    ],
)
def test_read_field_by_id(client: TestClient, skip: int, db: Session) -> None:
    fields = crud.field.get_multi(db, skip=skip, limit=1)
    field_id = None
    if fields:
        field_id = fields[0].id

    response = client.get(f"{settings.API_STR}/fields/{field_id}")
    assert response.status_code == 200


# [0, 1] are the skip values to skip certain number of records
# This checks for the first 2 records
@pytest.mark.parametrize(
    "skip",
    [
        0,
        1,
    ],
)
def test_read_field_research_by_id(client: TestClient, skip: int, db: Session) -> None:
    fields = crud.field.get_multi(db, skip=skip, limit=1)
    field_id = None
    if fields:
        field_id = fields[0].id

    response = client.get(f"{settings.API_STR}/fields/{field_id}/research")
    assert response.status_code == 200
