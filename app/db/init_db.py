import argparse
import datetime
import json
import logging

import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame
from sqlalchemy import text

from app import PROJECT_ROOT, crud
from app.core.config import get_settings
from app.db import base  # noqa: F401
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Data Import")

settings = get_settings()

parser = argparse.ArgumentParser()
parser.add_argument("--testing", action="store_true")
args = parser.parse_args()


def parse_date(date_string):
    """
    Converts a date string in 'MM/DD/YY' format to a datetime.date object.

    Args:
    date_string (str): The date string to parse, expected in 'MM/DD/YY' format.

    Returns:
    datetime.date: A date object representing the parsed date.

    Raises:
    ValueError: If the date_string is not in the expected format or is invalid.
    """
    # Parse the date string using strptime with the appropriate format
    try:
        date_object = datetime.datetime.strptime(date_string, "%m/%d/%y").date()
        return date_object
    except ValueError as e:
        # Raise an error with a more descriptive message
        raise ValueError(
            f"Invalid date or format: {date_string}. Expected format is MM/DD/YY."
        ) from e


class Data:
    def __init__(self, test_mode: bool) -> None:
        self.db = SessionLocal()

        self.data_path = PROJECT_ROOT / ("data" if not test_mode else "test_data")
        farm_data_path = self.data_path / "data.json"

        with open(farm_data_path) as f:
            self.data = json.load(f)["dataArray"]

    def insert_data(self) -> None:
        # truncate all tables
        logger.info("Truncating all tables")
        truncate_query = text("TRUNCATE TABLE farms RESTART IDENTITY CASCADE;")
        self.db.execute(truncate_query)

        for farm in self.data:
            logger.info(f"Importing farm: {farm['name']}")

            # Insert Farm
            obj_in = {
                "farm_name": farm["name"],
                "location_name": farm["location"],
            }
            # farm_in = schemas.FarmCreate(
            #     **obj_in
            # )  # might cause issue since no ID is provided
            farm_in_db = crud.farm.create(self.db, obj_in=obj_in)

            # extract polygon data
            field_shapes: GeoDataFrame = gpd.read_file(
                self.data_path / "shapefiles" / farm["polygon"]
            )
            # convert the coordinate reference system to EPSG 4326
            if field_shapes.crs.to_epsg() != 4326:
                field_shapes = field_shapes.to_crs(4326)

            field_shapes["centroid"] = (
                gpd.GeoSeries.concave_hull(field_shapes)
                .to_crs("+proj=cea")
                .centroid.to_crs(4326)
            )

            # Insert Fields
            for field in farm["fields"]:
                logger.info(f"Importing field: {field['fieldName']}")
                field_shape = str(
                    field_shapes[field_shapes["name"] == field["fieldName"]][
                        "geometry"
                    ].values[0]
                )
                field_coordinate = str(
                    field_shapes[field_shapes["name"] == field["fieldName"]][
                        "centroid"
                    ].values[0]
                )
                obj_in = {
                    "field_name": field["fieldName"],
                    "field_shape": field_shape,
                    "farm_ref_id": farm_in_db.id,
                    "coordinates": field_coordinate,
                }

                field_in_db = crud.field.create(self.db, obj_in=obj_in)

                # Insert Researches

                for research in field["research"]:
                    logger.info(
                        f"Importing research {research['researchName']} for field: {field['fieldName']}"
                    )

                    obj_in = {
                        "research_name": research["researchName"],
                        "research_area": research["researchArea"],
                        "research_type": research["researchType"],
                        "research_pi": research["research_pi"],
                        "research_contact_info": research["research_contact_info"],
                        "research_introduction": research["research_introduction"],
                        "research_conclusion": research["research_conclusion"],
                        "field_ref_id": field_in_db.id,
                    }

                    research_in = crud.research.create(self.db, obj_in=obj_in)

                    if research["researchKey"] == "cover_crop_data":
                        logger.info(
                            f"Importing Cover Crop Data for research: {research['researchName']}"
                        )
                        for cover_crop in research["cover_crop_data"]:
                            obj_in = {
                                "crop": cover_crop["crop"],
                                "planting_date": parse_date(
                                    cover_crop["planting_date"]
                                ),
                                "planting_method": cover_crop["planting_method"],
                                "seeding_rate": cover_crop["seeding_rate"],
                                "seeding_rate_unit": cover_crop["seeding_rate_unit"],
                                "termination_date": parse_date(
                                    cover_crop["termination_date"]
                                ),
                                "cover_crop_research_ref_id": research_in.id,
                            }
                            cover_crop_in = crud.cover_crop.create(
                                self.db, obj_in=obj_in
                            )

                            for d in cover_crop["data"]:
                                logger.info(
                                    f"Importing cover crop data for cover crop: {cover_crop['crop']}"
                                )
                                obj_in = {
                                    "observed_cover_crop_biomass": d[
                                        "observed_cover_crop_biomass"
                                    ],
                                    "sampling_date": parse_date(d["sampling_date"]),
                                    "predicted_cover_crop_biomass": d[
                                        "predicted_cover_crop_biomass"
                                    ],
                                    "cover_crop_biomass_unit": d[
                                        "cover_crop_biomass_unit"
                                    ],
                                    "observed_CN_ratio": d["observed_CN_ratio"],
                                    "predicted_CN_ratio": d["predicted_CN_ratio"],
                                    "cover_crop_data_ref_id": cover_crop_in.id,
                                }
                                crud.cover_crop_data.create(self.db, obj_in=obj_in)

                    if research["researchKey"] == "crop_rotation_yield":
                        logger.info(
                            f"Importing Crop Rotation Data for research: {research['researchName']}"
                        )
                        for crop_rotation in research["crop_rotation_yield"]:
                            obj_in = {
                                "planting_date": parse_date(
                                    crop_rotation["planting_date"]
                                ),
                                "harvest_date": parse_date(
                                    crop_rotation["harvest_date"]
                                ),
                                "crop": crop_rotation["crop"],
                                "crop_yield": crop_rotation["crop_yield"],
                                "yield_unit": crop_rotation["yield_unit"],
                                "seeding_rate": crop_rotation["seeding_rate"],
                                "seeding_rate_unit": crop_rotation["seeding_rate_unit"],
                                "total_fertilizer_applied": crop_rotation[
                                    "total_fertilizer_applied"
                                ],
                                "total_fertilizer_applied_unit": crop_rotation[
                                    "total_fertilizer_applied_unit"
                                ],
                                "crop_rot_research_ref_id": research_in.id,
                            }
                            crop_rot = crud.crop_rotation.create(self.db, obj_in=obj_in)

                            # Insert Fertilizers
                            for fertilizer in crop_rotation["fertilizer"]:
                                logger.info(
                                    f"Importing fertilizer for crop rotation: {crop_rotation['planting_date']}"
                                )
                                obj_in = {
                                    "fertilizer_date": parse_date(
                                        fertilizer["fertilizer_date"]
                                    ),
                                    "fertilizer_rate": fertilizer["fertilizer_rate"],
                                    "fertilizer_rate_unit": fertilizer[
                                        "fertilizer_rate_unit"
                                    ],
                                    "fertilizer_type": fertilizer["fertilizer_type"],
                                    "fertilizer_application_description": fertilizer[
                                        "description"
                                    ],
                                    "crop_rot_ref_id": crop_rot.id,
                                }

                                crud.fertilizer.create(self.db, obj_in=obj_in)

                    if research["researchKey"] == "cover_crop_data":
                        pass

                    if research["researchKey"] == "drs_yield_data":
                        logger.info(
                            f"Importing DRS Yield Data for research: {research['researchName']}"
                        )
                        for drs_yield in research["drs_yield_data"]:
                            obj_in = {
                                "replicate": drs_yield["replicate"],
                                "line": drs_yield["line"],
                                "planting_date": parse_date(drs_yield["planting_date"]),
                                "harvest_date": parse_date(drs_yield["harvest_date"]),
                                "crop_yield": drs_yield["crop_yield"],
                                "yield_unit": drs_yield["yield_unit"],
                                "research_ref_id": research_in.id,
                            }
                            crud.drs_yield.create(self.db, obj_in=obj_in)

                    # Insert Sensors
                    for sensor in research["sensors"]:
                        logger.info(
                            f"Importing sensor {sensor['sensorId']} for research: {research['researchName']}"
                        )
                        obj_in = {
                            "depth": sensor["depth"],
                            "sensor_id": sensor["sensorId"],
                            "sensor_type": sensor["sensorType"],
                            "research_ref_id": research_in.id,
                        }

                        crud.sensor.create(self.db, obj_in=obj_in)


if __name__ == "__main__":
    logger.info("Creating initial data")
    data = Data(test_mode=args.testing)
    data.insert_data()
    logger.info("Initial data created")
