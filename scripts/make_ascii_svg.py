from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source-photo.jpg"
OUTPUT = ROOT / "avi-ascii.svg"

if not SOURCE.exists():
    raise SystemExit("ERROR: source-photo.jpg not found!")

image = Image.open(SOURCE).convert("RGB")
image = ImageOps.exif_transpose(image)
image = ImageOps.fit(image, (100, 60))
image = ImageOps.grayscale(image)
image = ImageEnhance.Contrast(image).enhance(1.8)

ramp = "@%#*+=-:. "
lines = []

for y in range(image.height):
    line = ""
    for x in range(image.width):
        brightness = image.getpixel((x, y))
        index = int(brightness / 255 * (len(ramp) - 1))
        line += ramp[index]
    lines.append(line)

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="600" height="660" viewBox="0 0 600 660">',
    '<rect width="600" height="660" rx="16" fill="#0d1117"/>',
    '<defs><clipPath id="typing">'
    '<rect x="15" y="0" width="0" height="660">'
    '<animate attributeName="width" from="0" to="580" '
    'dur="4s" fill="freeze"/>'
    '</rect></clipPath></defs>',
    '<g clip-path="url(#typing)" font-family="monospace" '
    'font-size="9" fill="#c9d1d9">',
]

for i, line in enumerate(lines):
    y = 25 + i * 10
    svg.append(
        f'<text x="15" y="{y}" xml:space="preserve">'
        f'{escape(line)}</text>'
    )

svg.extend([
    '</g>',
    '<text x="25" y="640" font-family="monospace" '
    'font-size="17" fill="#3fb950">'
    'fahad@github:~$ whoami</text>',
    '</svg>'
])

OUTPUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Created: {OUTPUT}")
