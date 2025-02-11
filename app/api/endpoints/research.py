from collections import defaultdict
from typing import Any, List, Optional

import numpy as np
import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


def get_vpd(T, RH, elevation=0):
    T_kelv = T + +273.16
    e_st = 1013.246

    p_h = (
        e_st * (1 - (0.0065 * elevation) / 288.15) ** 5.255
    )  # calculate mean atmospheric air pressure at given elevation

    A = -0.58002206 * 10**4 / T_kelv
    B = 0.13914993 * 10**1
    C = -0.48640239 * 10 ** (-1) * T_kelv
    D = 0.41764768 * 10 ** (-4) * T_kelv**2
    E = -0.14452093 * 10 ** (-7) * T_kelv**3
    F = 0.65459673 * 10**1 * np.log(T_kelv)
    # log_e_sat = -0.58002206 * 10**4 / T_kelv + 0.13914993 * 10**1 - 0.48640239 * 10**(-1) * T_kelv + 0.41764768 * 10**(-4) * T_kelv**2 - 0.14452093 * 10**(-7) * T_kelv**3 + 0.65459673 * 10**1 * np.log10(T_kelv)
    e_sat = np.exp(A + B + C + D + E + F) / 100

    e_air = e_sat * RH / 100

    e_sat_site = e_sat * p_h / e_st
    e_air_site = e_air * p_h / e_st

    vpd = e_sat_site - e_air_site

    return round(vpd / 10, 3)


# write a function to convert temperature to Celsius from Fahrenheit
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0 / 9.0


def get_geostream_uris(
    sensors: List[models.Sensors], sensor_type: str, year: str
) -> List[dict]:
    data_endpoints = []
    for sensor in sensors:
        uri = f"{settings.GEOSTREAMS_API_STR}cache/day/{sensor.sensor_id}?since={year}-01-01T00:00:00&until={year}-12-31T00:00:00"
        if sensor.sensor_type == sensor_type:
            if sensor_type == "soil_moisture":
                data_endpoints.append(
                    {
                        "depth": sensor.depth,
                        "uri": uri,
                    }
                )
            elif sensor_type in ["weather", "nitrogen_conc"]:
                data_endpoints.append(uri)
    return data_endpoints


@router.get("/all", response_model=List[schemas.ResearchSummary])
def read_research(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve research."""
    research = crud.research.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return research


@router.get("/research_details", response_model=List[schemas.ResearchDetails])
def read_research_details(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    order_by: Optional[List[str]] = Query(None),
) -> Any:
    """Retrieve research."""
    research = crud.research.get_multi(db, skip=skip, limit=limit, order_by=order_by)
    return research


@router.get("/{research_id}", response_model=schemas.ResearchDetails)
def read_research_by_id(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get a research by id."""
    research = crud.research.get(db, id=research_id)
    if not research:
        raise HTTPException(
            status_code=404, detail=f"Research not found: ${research_id}"
        )
    return research


@router.get("/researchby/", response_model=Optional[List[schemas.ResearchSummary]])
def read_research_by(
    research_area: Optional[str] = None,
    research_type: Optional[str] = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get research by research area or research type."""
    research = crud.research.get_research_by(
        db, research_area=research_area, research_type=research_type
    )
    return research


@router.get("/{research_id}/sensors", response_model=List[schemas.SensorSummary])
def read_field_sensors(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the sensors for the given research id."""
    sensors = crud.research.get_sensors(db, id=research_id)
    return sensors


@router.post("/sensors", response_model=schemas.SensorSummary)
def create_sensor(
    sensor_in: schemas.SensorCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create a new sensor."""
    sensor = crud.sensor.create(db, obj_in=sensor_in)
    return sensor


@router.delete("/sensors/{sensor_id}", response_model=schemas.SensorSummary)
def delete_sensor(
    sensor_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete a sensor."""
    sensor = crud.sensor.delete(db, id=sensor_id)
    return sensor


@router.get("/{research_id}/sensors/get-years", response_model=schemas.Years)
def get_years(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the sensors for the given field id."""
    sensors = crud.research.get_sensors(db, id=research_id)
    years = []
    for sensor in sensors:
        if sensor.sensor_type == "weather":
            uri = f"{settings.GEOSTREAMS_API_STR}cache/year/{sensor.sensor_id}"
            response = requests.get(uri)
            data = response.json()
            years.extend([d["year"] for d in data["properties"]["avg_air_temp"]])
    years = [str(y) for y in sorted(list(set(years)))]

    return {"years": years}


@router.get(
    "/{research_id}/sensors/get-geostreams-data/nitrate-conc/{year}",
    response_model=schemas.NitrateConcentrationGeostreamsData,
)
def read_field_sensors_nitrate_concentration_geostreams_data(
    research_id: str,
    year: str,
    db: Session = Depends(deps.get_db),
):
    """Get all the sensors for the given field id."""
    sensors = crud.research.get_sensors(db, id=research_id)
    print(sensors)
    nitrate_data_endpoints = get_geostream_uris(sensors, "nitrogen_conc", year)
    print(nitrate_data_endpoints)
    nitrate_data = []

    for nitrate_data_endpoint in nitrate_data_endpoints:
        response = requests.get(nitrate_data_endpoint)
        data = response.json()
        nitrate_data.extend(
            [
                {
                    "average": d["average"],
                    "year": d["year"],
                    "month": d["month"],
                    "day": d["day"],
                    "label": d["label"],
                }
                for d in data["properties"]["nitrate_conc"]
            ]
        )

    return {"nitrate_concentration_data": nitrate_data, "year": year}


@router.get(
    "/{research_id}/sensors/get-geostreams-data/soil-moisture/{year}",
    response_model=schemas.SoilMoistureGeostreamsData,
)
def read_field_sensors_soil_moisture_geostreams_data(
    research_id: str,
    year: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the sensors for the given field id."""
    sensors = crud.research.get_sensors(db, id=research_id)
    soil_data_endpoints = get_geostream_uris(sensors, "soil_moisture", year)
    soil_data = defaultdict(dict)
    for soil_data_endpoint in soil_data_endpoints:
        response = requests.get(soil_data_endpoint["uri"])
        data = response.json()
        soil_data[soil_data_endpoint["depth"]] = {
            "data": [
                {
                    "average": d["average"],
                    "year": d["year"],
                    "month": d["month"],
                    "day": d["day"],
                    "label": d["label"],
                }
                for d in data["properties"]["soil_moisture"]
            ]
        }

    return {"depth_soil_moisture_data": soil_data}


@router.get(
    "/{research_id}/sensors/get-geostreams-data/weather/{year}",
    response_model=schemas.WeatherGeostreamsData,
)
def read_field_sensors_weather_geostreams_data(
    research_id: str,
    year: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Get all the sensors for the given field id."""
    sensors = crud.research.get_sensors(db, id=research_id)
    weather_data_endpoints = get_geostream_uris(sensors, "weather", year)
    weather_data = defaultdict(dict)
    # Only written assuming 1 sensor per field change its shape if need to accomodate multiple sensors
    for weather_data_endpoint in weather_data_endpoints:
        response = requests.get(weather_data_endpoint)
        data = response.json()

        temp_avg_air = [
            {
                "average": d["average"],
                "year": d["year"],
                "month": d["month"],
                "day": d["day"],
                "label": d["label"],
            }
            for d in data["properties"]["avg_air_temp"]
        ]
        temp_avg_air.sort(key=lambda x: x["label"])

        temp_rel_hum = [
            {
                "average": d["average"],
                "year": d["year"],
                "month": d["month"],
                "day": d["day"],
                "label": d["label"],
            }
            for d in data["properties"]["avg_rel_hum"]
        ]
        temp_rel_hum.sort(key=lambda x: x["label"])

        temp_precip = [
            {
                "average": round(d["average"] * 25.4, 2),  # convert to mm
                "year": d["year"],
                "month": d["month"],
                "day": d["day"],
                "label": d["label"],
            }
            for d in data["properties"]["precip"]
        ]
        temp_precip.sort(key=lambda x: x["label"])

        # calculate VPD
        vpd_data = []
        for i in zip(temp_avg_air, temp_rel_hum):
            vpd = get_vpd(fahrenheit_to_celsius(i[0]["average"]), i[1]["average"])
            vpd_data.append(
                {
                    "average": vpd,
                    "year": i[0]["year"],
                    "month": i[0]["month"],
                    "day": i[0]["day"],
                    "label": i[0]["label"],
                }
            )

        weather_data["avg_air_temp"] = temp_avg_air
        weather_data["avg_vpd"] = vpd_data
        weather_data["precipitation"] = temp_precip
        weather_data["year"] = year

    return {"weather_data": weather_data}


@router.post("/", response_model=schemas.ResearchDetails)
def create_research(
    research_in: schemas.ResearchCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Create new research."""
    research = crud.research.create(db, obj_in=research_in)
    return research


@router.delete("/{research_id}", response_model=schemas.ResearchDetails)
def delete_research(
    research_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Delete research."""
    research = crud.research.delete(db, id=research_id)
    return research
