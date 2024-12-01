from loguru import logger
from selenium import webdriver
import time
from typing import List

from functions_rightmove import (
    reject_cookies,
    search_station_for_sale,
    set_filters,
    get_property_links,
)
from utils import retry_function


def search_retry(
    station: str, radius: str, max_price: str, min_num_bedrooms: int
) -> List[str]:
    "Wrapper function to retry the search function"
    try:
        return retry_function(search, n_retries=3)(
            station, radius, max_price, min_num_bedrooms
        )
    except Exception as e:
        logger.error(f"Failed to search for station: {station}. Error: {e}")
        return [station, []]


def search(station: str, radius: str, max_price: str, min_num_bedrooms: int) -> List:
    """Open new driver to search for properties near station and apply filters"""
    logger.info(
        f"Opening new chrome driver to search for properties near station: {station}"
    )
    # STEP 1 - Open new browser and navigate to rightmove.co.uk
    # Set up new selenium driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Open Rightmove and navigate to the search page
    logger.info("Navigating to Rightmove website")
    driver.get("https://www.rightmove.co.uk/")

    # Reject cookies
    time.sleep(2)
    retry_function(reject_cookies, n_retries=3)(driver)
    time.sleep(2)

    # STEP 2 - Search "For sale" for properties near station that meet filter criteria
    # Search for the station and "For Sale" properties
    retry_function(search_station_for_sale, n_retries=3)(driver, station)
    time.sleep(2)

    # Set the filters and search for properties
    retry_function(set_filters, n_retries=3)(
        driver, radius, max_price, min_num_bedrooms
    )

    # Step 3: Iterate through found properties and extract information
    time.sleep(5)  # Adding sleep to ensure page is loaded

    # Loop over found property cards and save the links that meet the criteria
    property_links = retry_function(get_property_links, n_retries=3, raise_error=False)(
        driver
    )

    driver.quit()

    return [station, property_links]
