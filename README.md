# Pokemon Go Friend Codes Scraper

This Python script scrapes Pokémon Go friend codes along with additional friend details from a specified website and stores them in an Excel file. The script continuously monitors the page for new entries, extracts friend codes together with trainer names, levels, and locations, and updates the Excel file with only unique entries.

## Features

- **Web Scraping:** Uses `requests` to fetch HTML content and `BeautifulSoup` to parse it.
- **Data Extraction:** Leverages regular expressions and HTML parsing to extract friend codes, trainer names, levels, and locations.
- **Excel File Handling:** Reads from and writes to an Excel file using `openpyxl`, ensuring no duplicate entries are stored.
- **Continuous Monitoring:** Periodically checks for new friend entries on the website, updates the Excel file in real time, and logs added entries with details such as:
  - Trainer name
  - Level
  - Location (e.g., Suffolk, United Kingdom)
- **User Feedback:** Displays notifications in the console whenever a new friend entry is added, along with the current total count.
- **NEW! Generating QR Codes:** Generating QR codes for each friend code

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `openpyxl`

## Plans

- creating a large Pokémon Go player database categorized by country
- a simple GUI (e.g., Tkinter, PyQt, Gradio) with buttons like “Start,” “Stop,” “Export,” “Filter” — or a web-based frontend
