# Pokemon Go Friend Codes Scraper

This Python script scrapes Pokémon Go friend codes from a specified website and stores them in an Excel file. The script continuously fetches new codes, checks for duplicates, and updates the Excel file with unique codes.

## Features

- **Web Scraping:** Uses `requests` to fetch HTML content and `BeautifulSoup` to parse it.
- **Regex Matching:** Extracts friend codes using regular expressions.
- **Excel File Handling:** Reads and writes friend codes to an Excel file using `openpyxl`.
- **Continuous Monitoring:** Periodically checks for new codes and updates the Excel file.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `openpyxl`

You can install the required libraries using pip:

```sh
pip install requests beautifulsoup4 openpyxl
