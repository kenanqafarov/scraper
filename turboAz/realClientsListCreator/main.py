import requests
import time
import json
import os

folder_path = "turboAz/realClientsListCreator"
os.makedirs(folder_path, exist_ok=True)  

addresses_file_path = os.path.join(folder_path, "addresses.json")

headers = {
    "User-Agent": "Mozilla/5.0"
}

start_id = 8882000
end_id = 9999999

batch_size = 10

if os.path.exists(addresses_file_path):
    with open(addresses_file_path, "r", encoding="utf-8") as f:
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

    session_data = {
        "session": session_id,
        "clients": valid_urls
    }
    all_sessions.append(session_data)
    session_id += 1

    with open(addresses_file_path, "w", encoding="utf-8") as f:
        json.dump(all_sessions, f, indent=2, ensure_ascii=False)

    print("⏳ Batch tamamlandı, 10 saniyə gözləyirəm.")
    time.sleep(10)

print(f"✅ Bitdi. Toplam {session_id - 1} session addresses.json faylına yazıldı.")
