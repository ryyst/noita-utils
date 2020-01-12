#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from xml.dom import minidom

from PIL import Image


def parse_rows_from_xml(xml_path):
    xml_file = minidom.parse(xml_path)
    elements = xml_file.getElementsByTagName("RectAnimation")

    rows_by_pos = {}

    for elem in elements:
        attrs = elem.attributes

        y_position = attrs["pos_y"].value
        height = attrs["frame_height"].value
        frame_width = attrs["frame_width"].value
        frame_count = attrs["frame_count"].value
        name = attrs["name"].value

        if y_position in rows_by_pos:
            # Append to existing data if found, do not write multiple files
            # for same animation. Separate by dash, because names themselves
            # might have underscores, eg. "grab_item".
            rows_by_pos[y_position]["name"] += f"-{name}"
            continue

        rows_by_pos[y_position] = {
            "name": f"{y_position}-{frame_width}x{height}-{name}",
            "y_position": int(y_position),
            "height": int(height),
            "total_width": int(frame_width) * int(frame_count),
        }

    return rows_by_pos


def create_dir_for_splits(dir_name):
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        # Already exists, all good.
        pass


def create_new_files_from_rows(img_path, rows, dir_name):
    img = Image.open(img_path)

    # Sprites always start from the edge.
    left = 0

    for row in rows.values():
        new_path = Path(dir_name, row["name"]).with_suffix(".png")

        top = row["y_position"]
        bottom = top + row["height"]
        right = row["total_width"]

        print(f"Writing {new_path}...")
        section = img.crop((left, top, right, bottom))
        section.save(new_path)


def main(args):
    if len(args) != 2:
        print(f"Usage: slice_sheets.py <sheet.png> <sheet.xml>")
        sys.exit(1)

    img_path, xml_path = args
    dir_name, _ = img_path.split(".")

    rows_by_pos = parse_rows_from_xml(xml_path)
    create_dir_for_splits(dir_name)
    create_new_files_from_rows(img_path, rows_by_pos, dir_name)


if __name__ == "__main__":
    main(sys.argv[1:])
