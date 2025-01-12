from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
import pandas as pd
from tqdm import tqdm

from config import config
from functions_search import search_retry
from functions_rightmove import get_property_info_retry
from utils import convert_prop_search_to_dicts, update_database


if __name__ == "__main__":
    # --- READ CONFIGURATION PARAMETERS ---
    # Load configuration parameters from config.py file
    try:
        radius = config["radius"]
        max_price = config["max_price"]
        min_num_bedrooms = config["min_num_bedrooms"]
        max_zone = config["max_zone"]
        concurrent_searches = config["concurrent_searches"]
        stations = config["stations"] if "stations" in config else None
    except Exception as e:
        logger.error(f"Parameter missing in config file: {e}")
        raise Exception(f"Parameter missing in config file: {e}") from e

    # --- GET LIST OF STATIONS ---
    # If stations are not provided in the config file,
    # load them from the stations file and search for all night tube stations
    stations_df = pd.read_csv("tube_stations/stations_night_tube_filtered.csv")
    if stations is None:
        # Filter stations by zone
        stations_zone_df = stations_df[stations_df["zone"] <= max_zone]
        stations = stations_zone_df["name"].unique().tolist()
    else:
        stations_zone_df = stations_df[stations_df["name"].isin(stations)]

    # --- SEARCH FOR PROPERTIES NEAR STATIONS IN PARALLEL ---
    # Run the search function for stations in parallel using ThreadPoolExecutor
    # Loops over function 'search_retry'
    params_all = [
        (station + " Station", radius, max_price, min_num_bedrooms)
        for station in stations
    ]
    station_property_links = []
    with ThreadPoolExecutor(max_workers=concurrent_searches) as executor:
        futures = [executor.submit(search_retry, *params) for params in params_all]
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Station searched: "
        ):
            station_property_links.append(future.result())

    # Convert the results to a dictionary
    property_links_dicts = convert_prop_search_to_dicts(
        station_property_links, stations_zone_df
    )

    # --- GET INFO FOR EACH PROPERTY ---
    property_infos = []
    with ThreadPoolExecutor(max_workers=concurrent_searches) as executor:
        futures = [
            executor.submit(get_property_info_retry, d) for d in property_links_dicts
        ]
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Getting tenancy types: "
        ):
            property_infos.append(future.result())

    # --- UPDATE DATABASE ---
    # Filter out None values
    update_database(property_infos)
