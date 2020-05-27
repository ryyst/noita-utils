# Misc utils for Noita modding

Contains random scripts to make my own [Noita](https://noitagame.com/) modding endeavours easier.

## Requirements

- Preferably a rather new Python 3
- The PIL/Pillow image library
- The Awesome [Coder's Crux Font](https://www.dafont.com/coders-crux.font), for the palette generation script

# Slice & Join spritesheets

Noita spritesheets can occasionally be rather big, and importing all the
animations separately into Aseprite is painful manual labor. These scripts
should help with that pain a bit.

### Basic usage and workflow:

```sh
↪ python3 slice_sheets.py <sheet.png> <sheet.xml> <output_directory_name>
```

This will create a new directory according to your given `output_directory_name`,
separating all the animations into separate images. The directory listing should
look something like this:

```
↪ ls <output_dir> -l

  1-12x19-stand.png
  21-12x19-walk-run-burn.png
  41-12x19-jump_up.png
  61-12x19-jump_fall.png
  81-12x19-land.png
  101-12x19-fly_idle.png
  121-13x20-fly_move.png
  141-13x20-knockback.png
  161-13x20-swim_idle.png
  181-13x20-swim_move.png
  201-13x20-attack-kick.png
  ...
```

Filenames are structured like so: `{y-position}-{width}x{height}-{all_animation_names}.png`

---

Then you've done all your animation work, and you want to join your sheets
back together, from the same output folder you used previously:

```sh
↪ python3 join_sheets.py <sheet.png> <output.png> [<sheet_part1.png>, <sheet_part2.png>...]
```

The command format favours shell globbing:

```sh
↪ python3 join_sheets.py player.png player.png player_parts/*.png
```

**Notice:** The output *can* be same as input master sheet. The master sheet is
used only for dimension data and doesn't care if it's being overwritten.

**Notice2:** All outputs are **always** mercilessly overwritten without any
warnings. This just happened to suit my own workflow nicely.

---

Bonus! If you want to automatically do the joining every time you save your
animation, you can use something like [entr](http://eradman.com/entrproject/):

```sh
↪ ls player_parts/*.png | entr python3 join_sheets.py player.png player.png player_parts/*.png
```


# Color palette for map making

Generates a nice palette for editing the `biome_map.png`, any wang tiles or pixel scenes.

```sh
↪ python3 generate_biome_cheatsheet.py data/_biomes_all.xml data/materials.xml
```

**TODO:**

* custom material definition files
* custom biome definition files
* wang_scripts.csv

**Example output:**
![Color palette of all Noita's materials & biomes](/colors.png)
