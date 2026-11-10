from pathlib import Path
import copy
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

def tag(name):
    return f"{{{NS}}}{name}"

hero = ET.Element(tag("svg"), {
    "width": "1100",
    "height": "540",
    "viewBox": "0 0 1100 540",
    "xmlns": NS,
})

ET.SubElement(hero, tag("rect"), {
    "width": "1100",
    "height": "540",
    "rx": "22",
    "fill": "#0d1117",
})

ET.SubElement(hero, tag("rect"), {
    "x": "1", "y": "1",
    "width": "1098", "height": "538",
    "rx": "21",
    "fill": "none",
    "stroke": "#30363d",
})

def text(x, y, content, size, color, weight="normal"):
    element = ET.SubElement(hero, tag("text"), {
        "x": str(x),
        "y": str(y),
        "font-family": "monospace",
        "font-size": str(size),
        "font-weight": weight,
        "fill": color,
        "text-anchor": "middle",
    })
    element.text = content

text(550, 46, "FAHAD MUGHAL", 32, "#f0f6fc", "bold")
text(550, 77, "SOFTWARE DEVELOPER  /  BACKEND  /  AI", 16, "#3fb950")

def embed(filename, x, y, width, height):
    source = ET.parse(ROOT / filename).getroot()
    embedded = copy.deepcopy(source)
    embedded.set("x", str(x))
    embedded.set("y", str(y))
    embedded.set("width", str(width))
    embedded.set("height", str(height))
    embedded.set("preserveAspectRatio", "xMidYMid meet")
    hero.append(embedded)

embed("avi-ascii.svg", 45, 95, 345, 365)
embed("info-card.svg", 420, 117, 640, 325)

text(550, 494, "BUILD  /  LEARN  /  SHIP", 17, "#58a6ff")
text(550, 519, "Python  |  Django  |  JavaScript  |  Git", 14, "#8b949e")

output = ROOT / "profile-hero.svg"
ET.ElementTree(hero).write(
    output, encoding="utf-8", xml_declaration=True
)

print("Created:", output)
