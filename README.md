# Rightmove scraper

This repository contains a Python web scraper based on Selenium for extracting property listings from Rightmove. 

The code is specifically tailored for buying properties in London, but can be easily adapted to search for other places or rental properties as well.

## Overview

### Benefits

- Save time by automating property searches across multiple locations in parallel.

- Gain access to more detailed data than Rightmove's standard filters.

- Build a customizable and exportable database of properties for further analysis.

### Search filters

- Search radius
- Max price
- Minimum number of bedrooms
- Maximum London zone from centre (e.g., Zone 3)
- Number of concurrent searches
- (Optional) List of stations to search (if empty all stations will be searched)

### Unique features extracted

What sets this web scraper apart is its ability to extract detailed and granular property information that is not typically provided in bulk by Rightmove's interface. Key features include:

- Tenancy Type: Extract whether the property is freehold or leasehold.

- Square Metres: Gather data on the property's size.

- Distance from closest Tube/Train Station: Determine proximity to public transportation.

- Latest Activity: Identify when the property was last updated, such as:

    - The posting date.

    - When the price was last reduced.

- Price

- Zone of Tube station

- Number of bedrooms

- Number of bathrooms


## Get started

### Prerequisites
- Python (we recommend >= 3.12)
- Chrome browser

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/cjboisvert/rightmove_scraper.git
    ```
2. Navigate to the project directory:
    ```sh
    cd rightmove_scraper
    ```
3. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Update the search parameters in [config.py](config.py). 

    - Search radius
    - Max price
    - Minimum number of bedrooms
    - Maximum London zone from centre (e.g., Zone 3)
    - Number of concurrent searches
    - (Optional) List of stations to search (if empty all stations will be searched)

2. Run the scraper:
    ```sh
    python main.py
    ```
3. The scraped properties will be saved to [database.csv](database.csv), which contains a row for each found property that meets the desired criteria.

4. To update the database, simply run the scraper again. This will update the [database.csv](database.csv) file.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

Rightmove does not allow the use of APIs or web scrapers, and using them would be a violation of their terms of service. So please don't use this repo! ;)

## Contact
Corey Boisvert, cjboisvert@hotmail.com

For any questions or suggestions, please contact moi using email above.
