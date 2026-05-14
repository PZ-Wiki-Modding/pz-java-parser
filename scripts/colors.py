"""
Parses the Colors.java file to extract available colors, notably used in 
some Scripts like the fluid block or by the game at different places.

Colors can be of 3 types depending on the function used to create them:
- addGameColor
- addColorCB
- addColor

I don't know what the different is as I haven't checked tho but figured that 
info might be important anyway to store

It outputs its associated field in the Colors class, the name of the color refered to in the mapper,
and the RGB values
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/core/Colors.java")
OUT = Path("out/colors.json")

PATERN = r"Color (?P<field>\S+) = (?:(?P<fct>AddGameColor|addColorCB|addColor)\(\"(?P<name>\S+)\", new Color\((?P<r>\d+\.\d+)F, (?P<g>\d+\.\d+)F, (?P<b>\d+\.\d+)F\)\)|(?P<ref>\S+));"

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATERN, java_content)
    colors = []
    for match in matches:
        color = match.groupdict()
        color['r'] = float(color['r']) if color['r'] else None
        color['g'] = float(color['g']) if color['g'] else None
        color['b'] = float(color['b']) if color['b'] else None
        colors.append(color)

    for i, color in enumerate(colors):
        if isinstance(color['ref'], str):
            ref_color = next((c for c in colors if c['field'] == color['ref']), None)
            if ref_color is None:
                print(f"Could not find reference color for {color['field']} with ref {color['ref']}")
                continue
            ref_color['field'] = color['field']
            ref_color['ref'] = color['ref']
            colors[i] = ref_color

with open(OUT, "w") as out_file:
    json.dump(colors, out_file, indent=4)
