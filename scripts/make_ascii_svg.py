from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source-photo.jpg"
OUTPUT = ROOT / "avi-ascii.svg"

if not SOURCE.exists():
    raise SystemExit("ERROR: source-photo.jpg not found")

image = Image.open(SOURCE)
image = ImageOps.exif_transpose(image).convert("RGB")

# Crop portrait to a balanced frame
image = ImageOps.fit(
    image,
    (80, 65),
    method=Image.Resampling.LANCZOS,
    centering=(0.5, 0.42)
)

image = ImageOps.grayscale(image)
image = ImageEnhance.Contrast(image).enhance(1.5)
image = image.filter(ImageFilter.GaussianBlur(0.3))

ramp = "@%#*+=-:. "
lines = []

for y in range(image.height):
    chars = []
    for x in range(image.width):
        brightness = image.getpixel((x, y))

        # Remove brightest background pixels
        if brightness > 225:
            chars.append(" ")
        else:
            index = min(
                len(ramp) - 1,
                int(brightness / 256 * len(ramp))
            )
            chars.append(ramp[index])

    lines.append("".join(chars).rstrip())

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="460" height="480" viewBox="0 0 460 480">',
    '<rect width="460" height="480" rx="16" fill="#0d1117"/>',
    '<rect x="1" y="1" width="458" height="478" rx="15" '
    'fill="none" stroke="#30363d"/>',
    '<text x="18" y="28" font-family="monospace" '
    'font-size="13" fill="#3fb950">'
    '$ ./portrait.sh</text>',
]

for i, line in enumerate(lines):
    y = 50 + i * 6.1
    delay = i * 0.035

    svg.append(
        f'<text x="18" y="{y:.1f}" '
        f'font-family="monospace" font-size="6.4" '
        f'xml:space="preserve" fill="#c9d1d9" opacity="0">'
        f'{escape(line)}'
        f'<animate attributeName="opacity" '
        f'from="0" to="1" dur="0.2s" '
        f'begin="{delay:.2f}s" fill="freeze"/>'
        '</text>'
    )

svg.extend([
    '<text x="18" y="458" font-family="monospace" '
    'font-size="13" fill="#58a6ff">'
    'fahad@github:~$ whoami</text>',
    '</svg>'
])

OUTPUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Created: {OUTPUT}")
