# SCRAPER Project

A comprehensive scraper suite for `turbo.az` vehicles, containing three modules:

- **app[Final]**: Interactive menu-driven scraper with endpoint discovery, CSV export, and DataFrame preview.
- **directDataScraper**: Simple batch CSV exporter (Option 2 functionality).
- **realClientsListCreator**: Endpoint discovery tool (Option 1 functionality).

---

## 📁 Folder Structure

```
SCRAPER/
├─ turboAz/
│  ├─ app[Final]/
│  │  ├─ data/
│  │  │  ├─ addresses.json       # Discovered valid URLs (sessions)
│  │  │  └─ turboaz_data.csv      # Exported vehicle data
│  │  └─ main.py                  # Interactive menu application
│  ├─ directDataScraper/
│  │  ├─ directScraper.py         # CSV exporter script
│  │  └─ turboaz_data.csv         # Sample/previous CSV output
│  └─ realClientsListCreator/
│     ├─ main.py                  # Endpoint discovery script
│     └─ addresses.json           # Sample/previous JSON of URLs
└─ README.md                      # This documentation
```

---

## 🚀 app[Final]

An interactive CLI menu in `app[Final/main.py]` with four options:

1. **Find real end points**
   - Prompts for `car_count` and `batch_size`.
   - Scans IDs from `8882000` to `8882000 + car_count` in batches.
   - Collects valid `https://turbo.az/autos/{id}` URLs.
   - Saves sessions of valid URLs to `data/addresses.json`.

2. **Get CSV data from real end points**
   - Prompts for `car_count` and `batch_size`.
   - Scrapes detailed fields (ID, link, brand, model, year, km, price, status, city, view count, last update) for each valid URL.
   - Auto-detects price from either `product-price__i--bold` or `product-price__i--main` elements.
   - Writes records to `data/turboaz_data.csv`.

3. **Get DataFrame from CSV**
   - Prompts for number of rows to display.
   - Reads `data/turboaz_data.csv` via `pandas` and prints a preview including all columns.

4. **Exit**
   - Terminates the application.

**Usage**:
```bash
cd turboAz/app[Final]
python main.py
```

---

## 📂 directDataScraper

Simple CSV exporter (`directScraper.py`) targeting the same `turbo.az` IDs:

- Hardcoded `start_id`, `car_count`, and `batch_size` prompts.
- Exports scraped fields (without JSON sessions) to `turboaz_data.csv` inside its own folder.
- Mirrors Option 2 behavior without the interactive menu.

**Usage**:
```bash
cd turboAz/directDataScraper
python directScraper.py
```

---

## 📂 realClientsListCreator

Standalone endpoint discovery (`main.py`):

- Prompts for `start_id`, `end_id`, and `batch_size` via code defaults.
- Iterates through IDs and collects valid URLs.
- Saves sessions of valid URLs to `addresses.json`.
- Mirrors Option 1 behavior (Find real end points).

**Usage**:
```bash
cd turboAz/realClientsListCreator
python main.py
```

---

## 💡 Notes

- All outputs live under the `data/` directory of each module.
- Adjust `start_id` or ID ranges within each script to target different listings.
- Ensure dependencies (`requests`, `beautifulsoup4`, `pandas`) are installed:
  ```bash
  pip install requests beautifulsoup4 pandas
  ```

Happy scraping! 🎉

