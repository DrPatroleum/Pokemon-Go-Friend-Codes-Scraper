import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

URL = "https://pokemongo.gishan.net/friends/codes/"
FILE_PATH = "pokemon_friend_codes.xlsx"

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_codes(html):
    soup = BeautifulSoup(html, 'html.parser')
    codes = set()
    for strong_tag in soup.find_all('strong'):
        code_match = re.match(r'\d{4} \d{4} \d{4}', strong_tag.text)
        if code_match:
            codes.add(code_match.group(0))
    return codes

def read_existing_codes(file_path):
    if not os.path.exists(file_path):
        return set()
    
    workbook = load_workbook(file_path)
    sheet = workbook.active
    return set(cell.value for cell in sheet['A'] if cell.value is not None)

def write_new_codes(file_path, new_codes):
    if os.path.exists(file_path):
        workbook = load_workbook(file_path)
    else:
        workbook = Workbook()
    
    sheet = workbook.active
    existing_codes = read_existing_codes(file_path)
    
    row = len(existing_codes) + 1
    for code in new_codes:
        sheet.cell(row=row, column=1, value=code)
        row += 1
    
    workbook.save(file_path)

def main():
    while True:
        requests.get(URL)
        time.sleep(2)

        html = fetch_page(URL)
        new_codes = extract_codes(html)
        existing_codes = read_existing_codes(FILE_PATH)

        unique_new_codes = new_codes - existing_codes
        if unique_new_codes:
            write_new_codes(FILE_PATH, unique_new_codes)

        total_codes = len(read_existing_codes(FILE_PATH))
        
        current_time = datetime.now().strftime("%H:%M:%S")
        
        print(f"{current_time} >> Pokemon Go Friends ({total_codes} in total)")

        time.sleep(100)

if __name__ == "__main__":
    main()