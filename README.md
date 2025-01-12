# Rightmove Scraper

This repository contains a web scraper for extracting property listings from Rightmove.

# Overview

This repository contains a Python script for automating property searches on Rightmove, specifically tailored for buying properties. For a quick start and setup instructions, please refer to the README.md file included in the repository.

The scraper allows users to search across multiple locations simultaneously and is fully customizable based on criteria like:

- Location

- Distance

- Price range

- Number of bedrooms

- Property type

# Unique Features

What sets this web scraper apart is its ability to extract detailed and granular property information that is not typically provided in bulk by Rightmove's interface. Key features include:

- Tenancy Type: Extract whether the property is freehold or leasehold.

- Square Metres: Gather data on the property's size.

- Distance from Tube/Train Station: Determine proximity to public transportation.

- Latest Activity: Identify when the property was last updated, such as:

    - The posting date.

    - When the price was last reduced.

# Output

The scraper outputs the results in the form of a data frame, which can be exported as a CSV file. This makes it easy to build a structured database of properties and filter them more effectively than the Rightmove interface allows. Users can sort and analyze the data based on their specific requirements, including filtering by tenancy type or proximity to transport hubs.

# Benefits

- Save time by automating property searches across multiple locations.

- Gain access to more detailed data than Rightmove's standard filters.

- Build a customizable and exportable database of properties for further analysis.

# Usage

- 1. Clone this repository to your local machine.

- 2. Customize the script with your search parameters:

    - Location(s)

    - Distance range

    - Price range

    - Number of bedrooms

    - Property type

- 3. Run the script to scrape data.

- 4. Export the results as a CSV for analysis.

## Requirements

- Python 3.7
- `requests` library
- `beautifulsoup4` library
- `pandas` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/rightmove_scraper.git
    ```
2. Navigate to the project directory:
    ```sh
    cd rightmove_scraper
    ```
3. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the search parameters in `config.py`.
2. Run the scraper:
    ```sh
    python scraper.py
    ```
3. The scraped data will be saved to `output.csv`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

Rightmove does not allow the use of APIs or web scrapers, and using them would be a violation of their terms of service. So please don't use this repo! ;)

## Contact
Corey Boisvert, cjboisvert@hotmail.com

For any questions or suggestions, please contact moi using email above.
