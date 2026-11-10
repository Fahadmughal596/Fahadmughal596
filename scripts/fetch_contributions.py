from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date
import requests
import json

USERNAME = "Fahadmughal596"
ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"

url = f"https://github.com/users/{USERNAME}/contributions"

print("Fetching real GitHub contributions...")

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
days = {}

for cell in soup.select("[data-date][data-level]"):
    day = cell.get("data-date")
    level = cell.get("data-level")

    if not day or not level:
        continue

    try:
        date.fromisoformat(day)
        level = int(level)
    except ValueError:
        continue

    if 0 <= level <= 4:
        days[day] = {
            "date": day,
            "level": level
        }

if not days:
    raise RuntimeError(
        "No contribution cells found. GitHub may have changed its HTML."
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

data = {
    "username": USERNAME,
    "days": sorted(days.values(), key=lambda x: x["date"])
}

OUTPUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(f"Success! Found {len(days)} calendar days.")
print(f"Saved: {OUTPUT}")
