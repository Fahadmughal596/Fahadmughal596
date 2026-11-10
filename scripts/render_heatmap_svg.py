import json
from pathlib import Path
from datetime import date, timedelta
from html import escape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

data = json.loads(DATA.read_text(encoding="utf-8-sig"))
days = {
    item["date"]: int(item["level"])
    for item in data["days"]
}

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

CELL = 11
GAP = 4
STEP = CELL + GAP
LEFT = 42
TOP = 86
WEEKS = 53

today = date.today()
start = today - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="900" height="255" viewBox="0 0 900 255">',
    '<rect width="900" height="255" rx="18" fill="#0d1117"/>',
    '<rect x="1" y="1" width="898" height="253" rx="17" '
    'fill="none" stroke="#30363d"/>',
    '<text x="35" y="38" fill="#58a6ff" '
    'font-family="monospace" font-size="21" font-weight="bold">'
    'fahad@github:~$ ./contributions.sh</text>',
    '<text x="35" y="59" fill="#8b949e" '
    'font-family="monospace" font-size="12">'
    'Real GitHub activity - last 12 months</text>',
]

for week in range(WEEKS):
    for weekday in range(7):
        current = start + timedelta(days=week * 7 + weekday)

        if current > today:
            continue

        level = max(0, min(4, days.get(current.isoformat(), 0)))

        x = LEFT + week * STEP
        y = TOP + weekday * STEP

        # Diagonal reveal animation
        delay = (week * 0.025) + (weekday * 0.05)

        svg.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{COLORS[level]}" opacity="0">'
            f'<animate attributeName="opacity" '
            f'from="0" to="1" dur="0.4s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f'<title>{escape(current.isoformat())}</title>'
            '</rect>'
        )

svg.extend([
    '<text x="35" y="222" fill="#8b949e" '
    'font-family="monospace" font-size="13">'
    'Less</text>',
])

for i, color in enumerate(COLORS):
    svg.append(
        f'<rect x="{78+i*17}" y="211" '
        f'width="11" height="11" rx="2" fill="{color}"/>'
    )

svg.extend([
    '<text x="173" y="222" fill="#8b949e" '
    'font-family="monospace" font-size="13">More</text>',
    '</svg>'
])

OUTPUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Created: {OUTPUT}")
