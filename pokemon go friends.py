import requests
from bs4 import BeautifulSoup
import re
import time
import qrcode
import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

URL = "https://pokemongo.gishan.net/friends/codes/"
FILE_PATH = "pokemon_friend_codes.xlsx"
QR_PATH = r"C:\Users\USER\Desktop"

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
    # W pierwszym wierszu są nagłówki
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
        # Nagłówki kolumn
        sheet.append(["Name", "Level", "Code", "Location"])
    
    existing_codes = read_existing_friend_codes(file_path)
    
    for friend in friends:
        if friend["code"] not in existing_codes:
            sheet.append([friend["name"], friend["level"], friend["code"], friend["location"]])
            print(f"Added friend \033[91m{friend['name']}\033[0m || lvl \033[35m{friend['level']}\033[0m || \033[32m{friend['location']}\033[0m")
            #generowanie QR kodu
            generate_qr(friend["code"])
            time.sleep(1)
    
    workbook.save(file_path)

def generate_unique_filename(base_filename, qr_path):
    unique_filename = base_filename
    counter = 1
    while os.path.exists(os.path.join(qr_path, unique_filename)):
        unique_filename = f"qr_{counter}.jpg"
        counter += 1
    return os.path.join(qr_path, unique_filename)

def generate_qr(data):
    qr_path = os.path.join(QR_PATH, "QR POGO CODES")
    if not os.path.exists(qr_path):
        os.makedirs(qr_path)
        
    qr_path = generate_unique_filename("qr_0.jpg", qr_path)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2)

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(qr_path)

def main():
    while True:
        requests.get(URL)
        time.sleep(2)

        html = fetch_page(URL)
        friends = extract_friend_info(html)
        write_new_friends(FILE_PATH, friends)
        total_friends = len(read_existing_friend_codes(FILE_PATH))
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\033[34m{current_time}\033[0m >>> \033[36m{total_friends}\033[0m Pokemon GO friends collected!")
        
        time.sleep(100)

if __name__ == "__main__":
    main()
