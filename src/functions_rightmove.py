from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import time
from typing import List

from src.utils import retry_function


def reject_cookies(driver: WebDriver) -> None:
    """Wait for the reject cookies button to be clickable using its ID"""
    logger.info("Rejecting cookies")
    reject_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
    )
    time.sleep(1)  # Additional 1 second sleep to ensure the button is clickable
    reject_cookies_button.click()
    logger.info("Rejected cookies")


def search_station_for_sale(driver: WebDriver, station: str) -> None:
    """Search for properties near station"""
    logger.info(f"Searching for properties near station: {station}")

    # Get search box
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#ta_searchInput"))
    )
    time.sleep(1)  # Adding sleep to ensure search box is loaded

    # Enter station into search box
    search_box.send_keys(station)
    time.sleep(1)  # Adding sleep to ensure station is entered
    search_box.send_keys(Keys.RETURN)
    logger.info(f"Entered station: {station} into search box")
    time.sleep(1)  # Adding sleep to ensure page is loaded

    # Get and click for sale button
    for_sale_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[data-testid='forSaleCta']")
        )
    )
    for_sale_button.click()
    logger.info("Clicked 'For Sale' button")


def set_filters(
    driver: WebDriver,
    radius: str = "Within ¼ mile",
    max_price: str = "1,000,000",
    min_num_bedrooms: int = 3,
) -> None:
    """Set the filters to search for properties"""
    logger.info("Setting search filters")
    # Filter 1: Search Radius - dropdown
    logger.info(f"Setting search radius to: {radius}")
    assert radius in [
        "Within ¼ mile",
        "Within ½ mile",
        "Within 1 mile",
        "Within 3 miles",
        "Within 5 miles",
    ], "Radius not valid for Rightmove"
    radius_dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "radius"))
    )
    select = Select(radius_dropdown)
    select.select_by_visible_text(radius)

    # Filter 2: Max price
    logger.info(f"Setting max price to: {max_price}")
    assert max_price in [
        "800,000",
        "900,000",
        "1,000,000",
        "1,250,000",
        "1,500,000",
        "2,000,000",
        "5,000,000",
    ], "Max price not valid for Rightmove"
    max_price_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "maxPrice"))
    )
    select = Select(max_price_dropdown)
    select.select_by_visible_text(max_price)

    # Filter 3: Min number of bedrooms
    logger.info(f"Setting minimum number of bedrooms to: {min_num_bedrooms}")
    min_bedrooms_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "minBedrooms"))
    )
    select = Select(min_bedrooms_dropdown)
    select.select_by_visible_text(str(min_num_bedrooms))

    time.sleep(1)

    # Click the 'Submit' button
    see_properties_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "submit"))
    )
    see_properties_button.click()
    logger.info("Searching for properties...")


def get_property_links(driver: WebDriver) -> List[str]:
    """Get property links from the search results"""
    # Find the parent element
    parent_element = driver.find_element(
        "id", "l-searchResults"
    )  # Replace with your parent element's ID

    # Get the outer HTML of the parent element
    parent_html = parent_element.get_attribute("outerHTML")

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(parent_html, "html.parser")

    # Find all direct child elements (level 1)
    child_elements = soup.find_all(
        recursive=True
    )  # `recursive=False` ensures only direct children are included

    # Extract IDs of the child elements
    ids_all = [child.get("id") for child in child_elements if child.get("id")]
    ids_properties = [
        id.replace("property-", "") for id in ids_all if "property-" in id
    ]

    # Create links from the IDs
    property_links = [
        f"https://www.rightmove.co.uk/properties/{id}#/?channel=RES_BUY"
        for id in ids_properties
    ]

    # Remove duplicates from the list of property links
    property_links_unique = list(set(property_links))

    return property_links_unique


def get_property_info_retry(property_link_dict: dict) -> str:
    try:
        return retry_function(get_property_info, n_retries=3, raise_error=True)(
            property_link_dict
        )
    except Exception as e:
        logger.warning(
            f"Failed to get property info for link: {property_link_dict['link']}. Error: {e}"
        )
        return None


def get_property_info(property_link_dict: dict) -> str:
    """Get the tenancy type of a property"""
    # Initialize the Chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Open the property link
    property_link = property_link_dict["link"]
    driver.get(property_link)
    logger.info(f"Opening property using link: {property_link}")

    time.sleep(1)
    retry_function(reject_cookies, n_retries=3, raise_error=False)(driver)
    time.sleep(1)

    price_str = driver.find_elements(
        By.CSS_SELECTOR, "div._1gfnqJ3Vtd1z40MlC0MzXu > span:first-child"
    )[0].text

    updated_date = driver.find_elements(By.CSS_SELECTOR, "div._2nk2x6QhNB1UrxdI5KpvaF")[
        0
    ].text

    if "on" in updated_date:
        date = updated_date.split("on ")[1]
    else:
        day = updated_date.split(" ")[1]
        if day == "yesterday":
            date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        elif day == "today":
            date = datetime.now().strftime("%d/%m/%Y")
        else:
            date = None

    # Click the stations button
    stations_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Stations-button"))
    )
    stations_button.click()
    time.sleep(1)

    distance_closest = driver.find_element(
        By.CSS_SELECTOR, "div.mlEuHXZpfrrzJtwlRmwBe > span._1ZY603T1ryTT3dMgGkM7Lg"
    )

    distance_number = distance_closest.text.replace(" miles", "")

    # Get property type, number of bedrooms, number of bathrooms, size, and tenancy type
    elements = driver.find_elements(By.CSS_SELECTOR, "p._1hV1kqpVceE9m-QrX_hWDN")
    if len(elements) == 5:
        elm_indx = {
            "property_type": 0,
            "bedrooms": 1,
            "bathrooms": 2,
            "size": 3,
            "tenancy_type": 4,
        }
    else:
        elm_indx = {
            "property_type": 0,
            "bedrooms": 1,
            "size": 2,
            "tenancy_type": 3,
        }

    if "sq ft" in elements[elm_indx["size"]].text:
        size = (
            int(elements[elm_indx["size"]].text.replace(" sq ft", "").replace(",", "")),
        )
    else:
        size = None

    try:
        bedrooms = int(elements[elm_indx["bedrooms"]].text)
    except:
        bedrooms = None
    try:
        bathrooms = int(elements[elm_indx["bathrooms"]].text)
    except:
        bathrooms = None

    property_link_dict_new = {
        "station": property_link_dict["station"],
        "zone": property_link_dict["zone"],
        "link": property_link_dict["link"],
        "price": int(price_str.replace("£", "").replace(",", "")),
        "like": None,
        "comment": None,
        "property_type": elements[elm_indx["property_type"]].text,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "size": size,
        "distance_to_closest_station": distance_number,
        "tenancy_type": elements[elm_indx["tenancy_type"]].text,
        "date": date,
        "post_type": updated_date.split(" ")[0],
    }

    driver.quit()

    return property_link_dict_new
