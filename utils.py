from copy import deepcopy
from loguru import logger
import os
import pandas as pd
import time
from typing import Callable, Dict, List


def retry_function(
    function: Callable, n_retries: int = 3, raise_error: bool = True
) -> Callable:
    """Retry a function n_retries times before raising an exception."""

    def wrapper(*args, **kwargs):
        for retry in range(n_retries):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                if retry < n_retries - 1:
                    logger.warning(
                        f"Failed to execute function '{function.__name__}', retry: {retry + 1}. Error: {e}"
                    )
                    time.sleep(2 * (retry + 1))
                else:
                    error_msg = f"Failed to execute function '{function.__name__}' after {n_retries} retries. Error: {e}"
                    logger.error(error_msg)
                    if raise_error:
                        raise Exception(error_msg) from e

    return wrapper


def convert_prop_search_to_dicts(
    station_property_links: List, stations_zone_df: pd.DataFrame
) -> List[Dict]:
    """Convert the search results to a list of dictionaries."""
    property_links_dicts = []
    for res in station_property_links:
        station, property_links = res
        station_n = station.split(" Station")[0]
        zone = stations_zone_df[stations_zone_df["name"] == station_n]["zone"].values[0]
        for link in property_links:
            link_dict = {"station": station_n, "zone": zone, "link": link}
            property_links_dicts.append(link_dict)

    # Remove None values
    property_links_dicts = [
        element for element in property_links_dicts if element is not None
    ]

    return property_links_dicts


def update_database(property_infos: List[Dict]) -> None:
    """Save the property information to the database."""

    # Remove duplicates and keep properties with the shortest distance to the closest station
    logger.info("Removing duplicate properties and keeping the closest to the station")
    property_infos_filtered = [p for p in property_infos if p is not None]
    property_infos_no_duplicates = []
    for p1 in property_infos_filtered:
        p_min_distance = deepcopy(p1)
        for p2 in property_infos_filtered:
            if (
                p_min_distance["link"] == p2["link"]
                and p2["distance_to_closest_station"]
                < p_min_distance["distance_to_closest_station"]
            ):
                p_min_distance = deepcopy(p2)

        property_infos_no_duplicates.append(p_min_distance)

    if os.path.exists("database.csv"):
        # Load the existing database
        db = pd.read_csv("database.csv")
        new_db = pd.DataFrame(property_infos_no_duplicates)

        for _, new_row in new_db.iterrows():
            db = db[db["link"] != new_row["link"]]  # Remove duplicates
            db = db._append(new_row, ignore_index=True)  # Add new row

    else:
        db = pd.DataFrame(property_infos_no_duplicates)

    # Save the database
    db = db.sort_values(by=["station", "price"], ascending=True)
    db.to_csv("database.csv", index=False)
    logger.info("Database saved successfully")
