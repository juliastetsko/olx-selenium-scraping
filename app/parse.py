import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import gspread

BASE_URL = (
    "https://www.olx.ua/uk/list/q-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B8/"
)
GOOGLE_SHEET_LINK = "https://docs.google.com/spreadsheets/d/1r86gtYULMXR527-XbjeyPVtN0v2gdAAEhu3w59K4lh8/edit?usp=sharing"


def parse_apartments(driver: webdriver.Chrome, url: str):
    driver.get(url)
    accept_cookies_if_asked(driver)

    data = []
    apartments = driver.find_elements(By.CSS_SELECTOR, "div > div.css-1ut25fa > a")
    apartment_urls = [apartment.get_attribute("href") for apartment in apartments]
    for apartment_url in apartment_urls:
        driver.get(apartment_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "css-12vqlj3")))

        price = get_price(driver)
        location = get_location(driver)

        elements = driver.find_elements(By.CSS_SELECTOR, ".css-1r0si1e > p.css-b5m1rv")
        apartment_infos = [el.text for el in elements]

        floor = get_floor(apartment_infos)
        total_floors = get_total_floor(apartment_infos)
        area = get_area(apartment_infos)
        data.append(
            {
                "price": price,
                "floor": floor,
                "total_floors": total_floors,
                "location": location,
                "area": area,
            }
        )

    return data


def accept_cookies_if_asked(driver: webdriver.Chrome) -> None:
    try:
        accept_cookies_button = driver.find_element(By.CLASS_NAME, "css-1l30vq6")
        if accept_cookies_button.is_displayed():
            accept_cookies_button.click()
    except NoSuchElementException:
        pass


def get_price(driver: webdriver.Chrome) -> float | None:
    try:
        text = driver.find_element(By.CLASS_NAME, "css-12vqlj3").text
        price_text = text.replace("грн", "").replace("$", "").replace(" ", "")
        return float(price_text)
    except NoSuchElementException:
        return 0.0


def extract_info_value(apartment_infos: list[str], key: str) -> str:
    for apartment_info in apartment_infos:
        if apartment_info.startswith(key + ":"):
            return apartment_info.split(":")[1].strip()
    return ""


def get_floor(apartment_infos: list[str]) -> int:
    floor_str = extract_info_value(apartment_infos, "Поверх")
    return int(floor_str) if floor_str else 0


def get_total_floor(apartment_infos: list[str]) -> int:
    total_floor_str = extract_info_value(apartment_infos, "Поверховість")
    return int(total_floor_str) if total_floor_str else 0


def get_location(driver: webdriver.Chrome) -> str:
    return driver.find_element(By.CSS_SELECTOR, "div > p.css-1cju8pu.er34gjf0").text


def get_area(apartment_infos: list[str]) -> float:
    area_str = extract_info_value(apartment_infos, "Загальна площа")
    return float(area_str.replace("м²", "").replace(" ", "")) if area_str else 0.0


def write_to_google_sheet(data, sheet_link: str):
    if not data:
        return
    gc = gspread.service_account()
    sheet = gc.open_by_url(sheet_link).sheet1
    sheet.clear()

    headers = list(data[0].keys())
    sheet.append_row(headers)
    for row_data in data:
        row = [row_data[field] for field in headers]
        sheet.append_row(row)


if __name__ == "__main__":
    web_driver = webdriver.Chrome()
    try:
        parsed_data = parse_apartments(web_driver, BASE_URL)
        write_to_google_sheet(parsed_data, GOOGLE_SHEET_LINK)
    finally:
        web_driver.quit()
