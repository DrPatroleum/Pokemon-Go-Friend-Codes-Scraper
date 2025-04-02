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

def extract_friend_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    friends = []
    # Znajdujemy wszystkie bloki komentarzy z kodami (klasa zawiera "comment-bubble")
    for bubble in soup.find_all("div", class_=re.compile(r"comment-bubble")):
        # Pobieramy nazwę trenera
        name_tag = bubble.find("span", class_="comment-bubble-header")
        name = name_tag.text.strip() if name_tag else "Unknown"
        
        # Szukamy poziomu - wyrażenie regularne wyszukujące "Level" i cyfrę
        level_match = re.search(r'Level\s*(\d+)', bubble.get_text())
        level = level_match.group(1) if level_match else "?"
        
        # Pobieramy kod znajomego
        code_tag = bubble.find("strong")
        code = code_tag.text.strip() if code_tag else "NoCode"
        
        # Pobieramy lokalizację: w divie "comment-content" szukamy linków, które nie prowadzą do profilu trenera
        comment_content = bubble.find("div", class_="comment-content")
        location_links = []
        if comment_content:
            for a in comment_content.find_all("a"):
                href = a.get("href", "")
                if not href.startswith("/trainer"):
                    location_links.append(a.text.strip())
        location = ", ".join(location_links) if location_links else "Unknown Location"
        
        friends.append({
            "name": name,
            "level": level,
            "code": code,
            "location": location
        })
    return friends

def read_existing_friend_codes(file_path):
    if not os.path.exists(file_path):
        return set()
    
    workbook = load_workbook(file_path)
    sheet = workbook.active
    friend_codes = set()
    # Zakładamy, że w pierwszym wierszu są nagłówki
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[2]:
            friend_codes.add(row[2])
    return friend_codes

def write_new_friends(file_path, friends):
    if os.path.exists(file_path):
        workbook = load_workbook(file_path)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        # Dodajemy nagłówki kolumn
        sheet.append(["Name", "Level", "Code", "Location"])
    
    existing_codes = read_existing_friend_codes(file_path)
    
    for friend in friends:
        if friend["code"] not in existing_codes:
            sheet.append([friend["name"], friend["level"], friend["code"], friend["location"]])
            print(f"Added friend {friend['name']} || lvl {friend['level']} || {friend['location']}")
    
    workbook.save(file_path)

def main():
    while True:
        # Odświeżamy stronę
        requests.get(URL)
        time.sleep(2)  # krótka pauza by strona się w pełni załadowała

        html = fetch_page(URL)
        friends = extract_friend_info(html)
        write_new_friends(FILE_PATH, friends)
        total_friends = len(read_existing_friend_codes(FILE_PATH))
        
        # Pobieramy aktualny czas
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{current_time} >> Pokemon GO friends ({total_friends} in total)")
        
        time.sleep(100)

if __name__ == "__main__":
    main()
