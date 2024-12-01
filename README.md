# Rightmove Scraper

This repository contains a web scraper for extracting property listings from Rightmove.

## Features

- Scrapes property details such as price, address, and description.
- Saves data to a CSV file for easy analysis.
- Configurable search parameters.

## Requirements

- Python 3.x
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

## Contact

For any questions or suggestions, please contact [your email].
