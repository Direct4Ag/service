import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_all_research(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/research/all")
    assert response.status_code == 200


def test_read_research_details(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_STR}/research/research_details")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "skip",
    [
        0,
        1,
    ],
)
def test_read_research_by_id(client: TestClient, skip: int, db: Session) -> None:
    research = crud.research.get_multi(db, skip=skip, limit=1)
    research_id = None
    if research:
        research_id = research[0].id

    response = client.get(f"{settings.API_STR}/research/{research_id}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "research_area,research_type",
    [
        ("Nitrogen Conservation", "Cover Crop"),
        ("Water Resource Management", "Irrigation Strategies"),
    ],
)
def test_read_research_by(
    client: TestClient, research_area: str, research_type: str, db: Session
) -> None:
    response = client.get(
        f"{settings.API_STR}/research/researchby/?research_area={research_area}&research_type={research_type}"
    )
    assert response.status_code == 200


@pytest.mark.parametrize("skip", [3])
def test_read_research_sensors_by_id(
    client: TestClient, skip: int, db: Session
) -> None:
    researches = crud.research.get_multi(db, skip=skip, limit=1)
    research_id = None
    if researches:
        research_id = researches[0].id

    response = client.get(f"{settings.API_STR}/research/{research_id}/sensors")
    assert response.status_code == 200
