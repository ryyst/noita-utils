#!/usr/bin/env python3
"""Noita spritesheet joiner

This script is used for managing spritesheets used by the Noita videogame
(by Nolla Games).

The script simply joins together all individual animation sheet files sliced
earlier by the other script.

Separate animations are pasted into the correct Y-position (depicted from their
filename) of the original spritesheet, then saved into the given output filename.
Original sheet is used to get correct dimensions of the output sheet.

NOTICE:

The supplied output sheet file will ALWAYS be overwritten without any further
warnings.

Usage:

    join_sheets.py <original_sheet.png> <output_sheet.png> [<sheet_part1.png>, <sheet_part2.png>...]
"""
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


def create_new_sheet(master_path, output_path, parts_data):
    try:
        master_sheet = Image.open(master_path)
    except (OSError, FileNotFoundError):
        print("[ERROR] Please supply a copy of the original sheet as the first parameter")
        sys.exit(1)

    # Create new sheet to remove possible artifacts from editing process.
    new_sheet = Image.new("RGBA", master_sheet.size, (255, 0, 0, 0))

    for part in parts_data:
        new_sheet.paste(part["image"], part["position"])

    new_sheet.save(output_path)



def main(args):
    if len(args) < 3:
        print(__doc__)
        sys.exit(1)

    master_path, output_path, parts_paths = args[0], args[1], args[2:]

    parts_data = get_parts_data(parts_paths)
    create_new_sheet(master_path, output_path, parts_data)


if __name__ == "__main__":
    main(sys.argv[1:])
