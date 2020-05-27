#!/usr/bin/env python3
import sys
from datetime import date
from pathlib import Path
from xml.dom import minidom

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


FONT = ImageFont.truetype("Coder's Crux.ttf", 16)
BLACK = "#999"


LINE_PADDING = 3
PAGE_MARGINS = 16
LINE_HEIGHT = 16
COLUMN_WIDTH = 280

BOX_SIZE = 12


def _normalize_name(name):
    """Return the filename in a "human readable" format."""
    return Path(name).stem.replace("_", " ").capitalize()


def _normalize_color(color):
    """Noita uses ARGB instead of RGBA, so we gotta swap around a bit."""
    return "#%s" % (color[2:].lower())


def parse_materials_xml(xml_path):
    xml_file = minidom.parse(xml_path)
    cell_data = xml_file.getElementsByTagName("CellData")
    cell_data_children = xml_file.getElementsByTagName("CellDataChild")

    elements = cell_data + cell_data_children

    line_data = []
    for elem in elements:
        attrs = elem.attributes

        name = _normalize_name(attrs["name"].value)
        color = _normalize_color(attrs["wang_color"].value)
        line_data.append((name, color))

    return line_data


def parse_biomes_xml(xml_path):
    xml_file = minidom.parse(xml_path)
    elements = xml_file.getElementsByTagName("Biome")

    line_data = []
    for elem in elements:
        attrs = elem.attributes

        name = _normalize_name(attrs["biome_filename"].value)
        color = _normalize_color(attrs["color"].value)
        line_data.append((name, color))

    return line_data


def render_biomes(draw, biomes, start_y):
    # Sort alphabetically
    biomes = sorted(biomes, key=lambda k: k[0].lower())

    # TODO: This will still break with odd sizes, the +1 is just an
    #       emergency fix for this specific length.
    column_size = int(len(biomes) / 3) + 1
    biomes_by_columns = [biomes[i:i + column_size] for i in range(0, len(biomes), column_size)]

    for col, column in enumerate(biomes_by_columns):
        for row, data in enumerate(column):
            y = start_y + LINE_HEIGHT*row
            x = PAGE_MARGINS + COLUMN_WIDTH*col
            name, color = data

            render_line(draw, (x, y), color, name)

    # Lowest y-position
    new_y = column_size * LINE_HEIGHT
    return new_y


def render_line(draw, start_point, color, name):
    """Draw the colored box and its associated line of text.

    Roughly like so:
    [_] #color - Biome Name
    """
    x, y = start_point

    box_coords = ((x, y), (x + BOX_SIZE, y + BOX_SIZE))
    text_coords = (x + BOX_SIZE + LINE_PADDING, y+LINE_PADDING)

    biome_info = f"{color} - {name}"

    draw.rectangle(box_coords, fill=color, outline=BLACK)
    draw.text(text_coords, biome_info, BLACK, font=FONT)


def render_sheet(biomes, materials):
    """Render the entire sheet, going in order from top to bottom"""

    # Pre-calculate the dimensions that the sheet will approximately take.
    # NOTE: The height might be a bit off but works for the current specific cases.
    width = PAGE_MARGINS*2 + COLUMN_WIDTH*3

    height = len(biomes)/3 * LINE_HEIGHT + PAGE_MARGINS * 2
    height += (len(materials)/3 * LINE_HEIGHT) + (PAGE_MARGINS * 8)
    height = int(height)

    img = Image.new("RGBA", (width, height), "#2c2c2c")
    draw = ImageDraw.Draw(img)

    # Basically we keep track of the Y-coordinate after every draw, and just keep adding stuff
    y = PAGE_MARGINS

    draw.text((PAGE_MARGINS, y), "BIOME COLORS (for biome_map.png)", BLACK, font=FONT)
    y += (PAGE_MARGINS * 2)
    y = render_biomes(draw, biomes, y)

    y += (PAGE_MARGINS * 5)
    draw.text((PAGE_MARGINS, y), "MATERIALS (for Wang tiles & pixel scenes)", BLACK, font=FONT)
    y += (PAGE_MARGINS * 2)
    y = render_biomes(draw, materials, y)

    disclaimer = "Generated on: %s" % date.today().isoformat()
    disclaimer += " | Contact: @ryyst/roisto/rippentrop/mortti"
    disclaimer += " | Font: Coder's Crux by Chequered Ink"
    draw.text((PAGE_MARGINS, height-12), disclaimer, BLACK, font=FONT)

    return img


def main(args):
    if len(args) != 2:
        print(f"Usage: generate_biome_cheatsheet.py _biomes_all.xml materials.xml")
        sys.exit(1)

    biomes_path, materials_path = args

    biomes = parse_biomes_xml(biomes_path)
    materials = parse_materials_xml(materials_path)

    img = render_sheet(biomes, materials)

    output_path = "colors.png"
    img.save(output_path)

    print("Material palette generated to: %s" % output_path)

if __name__ == "__main__":
    main(sys.argv[1:])
