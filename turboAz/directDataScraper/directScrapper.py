import requests
from bs4 import BeautifulSoup
import csv
import time
import os

headers = {
    "User-Agent": "Mozilla/5.0"
}

car_count = int(input("Neçə maşın məlumatı yüklənsin?: "))
batch_size = int(input("Batch size neçə olsun?: "))

start_id = 8882000  
end_id = min(start_id + car_count, 9999999) 
folder_path = "turboAz/directDataScraper"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = os.path.join(folder_path, "turboaz_data.csv")

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Elan ID", "Link", "Marka", "Model", "İl", "KM", "Qiymət", "Satış Statusu", "Şəhər", "Baxış sayı", "Yeniləmə tarixi"])

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

                    price_tag = soup.find("div", class_="product-price__i product-price__i--main")
                    if price_tag:
                        qiymet = price_tag.text.strip()

                    status_tag = soup.find("div", class_="product-not-available-text")
                    satis_statusu = status_tag.text.strip() if status_tag else "Satışda"

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
                    print(f"✅ Yazıldı: {url}")

                else:
                    print(f"❌ Tapılmadı: {url}")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Xəta: {url} - {e}")

        print("⏳ Batch bitdi, 5 saniyə gözləyirəm...")
        time.sleep(1)

print("✅ Bütün datalar CSV-ə yazıldı.")
