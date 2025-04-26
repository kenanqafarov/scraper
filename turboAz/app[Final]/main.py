import requests
import time
import json
import os
import csv
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

def print_welcome_message():
    print("\033[1;32m" + "="*40)
    print("\033[1;34mWelcome to Turbo.az Data Scrapper!")
    print("\033[1;32m" + "="*40)
    print("\033[1;36m")
    print("Choose an option:")
    print("1 - Find real end points")
    print("2 - Get CSV data from real end points")
    print("3 - Get DataFrame from CSV")
    print("4 - Exit")
    print("\033[1;36m")
    print("="*40 + "\033[0m")

def find_real_endpoints():
    car_count = int(input("How many cars do you want to find?: "))
    batch_size = int(input("What should be the batch size?: "))

    start_id = 8882000
    end_id = min(start_id + car_count, 9999999)

    folder_path = os.path.join("turboAz/app[Final]", "data")
    os.makedirs(folder_path, exist_ok=True)

    addresses_path = os.path.join(folder_path, "addresses.json")

    if os.path.exists(addresses_path):
        with open(addresses_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            if isinstance(loaded_data, dict):
                all_sessions = [loaded_data]
            else:
                all_sessions = loaded_data
    else:
        all_sessions = []

    session_id = len(all_sessions) + 1

    for batch_start in range(start_id, end_id, batch_size):
        batch_end = min(batch_start + batch_size, end_id)
        valid_urls = []

        for i in range(batch_start, batch_end):
            url = f"https://turbo.az/autos/{i}"
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200 and "turbo.az" in response.text:
                    print(f"✅ Found: {url}")
                    valid_urls.append(url)
                else:
                    print(f"❌ Not found: {url}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error on {url}: {e}")

        if valid_urls:
            session_data = {
                "session": session_id,
                "clients": valid_urls
            }
            all_sessions.append(session_data)
            session_id += 1

            with open(addresses_path, "w", encoding="utf-8") as f:
                json.dump(all_sessions, f, indent=2, ensure_ascii=False)

            print("⏳ Batch completed, waiting 10 seconds...")
            time.sleep(10)

    print(f"✅ Done. {session_id - 1} session addresses written to addresses.json.")

def get_csv_data():
    car_count = int(input("How many cars do you want to download?: "))
    batch_size = int(input("What should be the batch size?: "))

    start_id = 8882000
    end_id = min(start_id + car_count, 9999999)

    folder_path = os.path.join("turboAz/app[Final]", "data")
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, "turboaz_data.csv")

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Ad ID", "Link", "Brand", "Model", "Year", "KM", "Price", "Status", "City", "View Count", "Last Update"])

        for batch_start in range(start_id, end_id, batch_size):
            batch_end = min(batch_start + batch_size, end_id)

            for i in range(batch_start, batch_end):
                url = f"https://turbo.az/autos/{i}"
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200 and "turbo.az" in response.text:
                        soup = BeautifulSoup(response.text, "html.parser")

                        marka = model = il = km = qiymet = satis_statusu = seher = baxis_sayi = yenilenme_tarixi = ""

                        title_tag = soup.find("h1", class_="product-title")
                        if title_tag:
                            title_text = title_tag.text.strip()
                            parts = title_text.split(",")
                            if len(parts) >= 3:
                                marka_model = parts[0].strip()
                                marka, model = marka_model.split(" ", 1)
                                il = parts[2].replace("il", "").strip()
                            if len(parts) >= 4:
                                km = parts[3].replace("km", "").strip()

                        price_tag = soup.find("div", class_="product-price__i product-price__i--bold")
                        if not price_tag:
                            price_tag = soup.find("div", class_="product-price__i product-price__i--main")
                        if price_tag:
                            qiymet = price_tag.text.strip()

                        status_tag = soup.find("div", class_="product-not-available-text")
                        satis_statusu = status_tag.text.strip() if status_tag else "For Sale"

                        properties = soup.find_all("div", class_="product-properties__i")
                        for prop in properties:
                            label = prop.find("label")
                            value = prop.find("span", class_="product-properties__i-value")
                            if label and value:
                                label_text = label.text.strip()
                                value_text = value.text.strip()

                                if label_text == "Şəhər":
                                    seher = value_text
                                if label_text == "Yürüş":
                                    km = value_text

                        stats_section = soup.find_all("span", class_="product-statistics__i-text")
                        for stat in stats_section:
                            text = stat.text.strip()
                            if "Baxışların sayı" in text:
                                baxis_sayi = text.replace("Baxışların sayı:", "").strip()
                            if "Yeniləndi" in text:
                                yenilenme_tarixi = text.replace("Yeniləndi:", "").strip()

                        writer.writerow([i, url, marka, model, il, km, qiymet, satis_statusu, seher, baxis_sayi, yenilenme_tarixi])
                        print(f"✅ Written: {url}")

                    else:
                        print(f"❌ Not Found: {url}")

                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Error: {url} - {e}")

            print("⏳ Batch completed, waiting 5 seconds...")
            time.sleep(5)

    print("✅ All data written to CSV.")

def get_dataframe_from_csv():
    car_count = int(input("How many cars do you want to display?: "))

    folder_path = os.path.join("turboAz/app[Final]", "data")
    filename = os.path.join(folder_path, "turboaz_data.csv")

    df = pd.read_csv(filename)
    print(df.head(car_count))

def main():
    while True:
        print_welcome_message()

        choice = input("Please choose an option: ")

        if choice == "1":
            find_real_endpoints()
        elif choice == "2":
            get_csv_data()
        elif choice == "3":
            get_dataframe_from_csv()
        elif choice == "4":
            print("\033[1;32mThank you for using Turbo.az Data Scrapper! Goodbye!\033[0m")
            break
        else:
            print("\033[1;31mInvalid choice. Please try again.\033[0m")

if __name__ == "__main__":
    main()
