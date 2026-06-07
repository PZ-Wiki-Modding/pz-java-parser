"""
Parses 
"""

import json, re, yaml
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/core/properties/TilePropertyKey.java")
OUT = Path("out/tile_properties.json")
DATA = Path("data/tile_properties.yaml")

# parse the java file for tile properties
PATTERN = r'public static final TilePropertyKey (?P<field>\w+) = registerBase\("(?P<name>\w+)"\);'

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    property = {}
    for match in matches:
        property[match.group("name")] = {"field": match.group("field")}

# parse the data file for tile properties
with open(DATA, "r") as f:
    data = yaml.safe_load(f)

    for name, obj in data["objects"].items():
        if name in property:
            for key, value in obj.items():
                property[name][key] = value

# check provided data is not providing for a non-existing tile
for name in data["objects"].keys():
    if name not in property:
        print(f"Warning: provided data for non-existing tile property '{name}'")

# copy #desc to description
for prop in property.values():
    if "#desc" in prop:
        ref = prop["#desc"]
        if ref not in property:
            print(f"Warning: description reference '{ref}' not found for property '{prop['field']}'")
            continue
        prop["description"] = property[ref]["description"]

# output
with open(OUT, "w") as out_file:
    json.dump(property, out_file, indent=4)
