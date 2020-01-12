#!/usr/bin/env python3
import sys
from pathlib import Path

from PIL import Image


def get_parts_data(parts_paths):
    parts_data = []

    for path in parts_paths:
        filename = Path(path).name
        y_position = int(filename.split("-")[0])
        img = Image.open(path)

        parts_data.append({
            "image": img,
            "position": (0, y_position)
        })

    return parts_data


def paste_parts_to_master_sheet(img_path, parts_data):
    master_sheet = Image.open(img_path)

    # Create new sheet to remove possible artifacts from editing process.
    new_sheet = Image.new("RGBA", master_sheet.size, (255, 0, 0, 0))

    for part in parts_data:
        new_sheet.paste(part["image"], part["position"])

    new_sheet.save(img_path)



def main(args):
    if len(args) < 2:
        print(f"Usage: join_sheets.py <sheet.png> [<sheet_part>, ...]")
        sys.exit(1)

    img_path, parts_paths = args[0], args[1:]

    parts_data = get_parts_data(parts_paths)
    paste_parts_to_master_sheet(img_path, parts_data)


if __name__ == "__main__":
    main(sys.argv[1:])
