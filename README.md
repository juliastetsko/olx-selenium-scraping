# OLX Apartment Data Scraper

## Overview
This project aims to scrape data about apartments listed on OLX.ua, specifically focusing on details like price, location, floor, total floors, and area. The scraped data is then structured and written to a Google Sheet for further analysis or usage.

## Methodology
- **Scraping:** Selenium is used to scrape apartment listings from OLX.ua, extracting details such as price, location, floor, total floors, and area.
- **Data Structuring:** The scraped data is structured into a dictionary format for each apartment listing.
- **Google Sheet Integration:** The structured data is written to a Google Sheet using the gspread library, allowing for easy storage and access to the data.

## Usage
1. Clone the GitHub repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the Python script to scrape apartment data and write it to the Google Sheet.

## GitHub Repository
[Link to GitHub Repository](https://github.com/juliastetsko/olx-selenium-scraping)

## Google Sheet
[Link to Google Sheet](https://docs.google.com/spreadsheets/d/1r86gtYULMXR527-XbjeyPVtN0v2gdAAEhu3w59K4lh8/edit?usp=sharing)
