from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"

rows = [
    ("ROLE", "Software Developer"),
    ("FOCUS", "Backend Development + AI"),
    ("STACK", "Python / Django / JavaScript"),
    ("TOOLS", "Git / GitHub / SQL / REST APIs"),
    ("BUILDING", "FarmerChat / Web Applications"),
    ("LEARNING", "DevOps / AI Integration"),
    ("LOCATION", "Pakistan"),
]

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="440" viewBox="0 0 900 440">',
    '<rect width="900" height="440" rx="18" fill="#0d1117"/>',
    '<rect x="1" y="1" width="898" height="438" rx="17" fill="none" stroke="#30363d" stroke-width="2"/>',
    '<rect width="900" height="58" rx="18" fill="#161b22"/>',
    '<rect y="40" width="900" height="18" fill="#161b22"/>',
    '<circle cx="28" cy="29" r="8" fill="#ff5f57"/>',
    '<circle cx="54" cy="29" r="8" fill="#febc2e"/>',
    '<circle cx="80" cy="29" r="8" fill="#28c840"/>',
    '<text x="450" y="36" text-anchor="middle" font-family="monospace" font-size="19" fill="#8b949e">fahad@github:~</text>',
    '<text x="35" y="108" font-family="monospace" font-size="28" font-weight="bold" fill="#58a6ff">Fahad Mughal</text>',
    '<text x="35" y="145" font-family="monospace" font-size="17" fill="#3fb950">$ cat developer-info.txt</text>',
]

for index, (label, value) in enumerate(rows):
    y = 189 + index * 34
    delay = index * 0.16
    svg.append(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze"/>'
        f'<text x="35" y="{y}" font-family="monospace" font-size="17" fill="#79c0ff">{escape(label)}</text>'
        f'<text x="205" y="{y}" font-family="monospace" font-size="17" fill="#c9d1d9">{escape(value)}</text>'
        f'</g>'
    )

svg.append("</svg>")
OUTPUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Created: {OUTPUT}")
