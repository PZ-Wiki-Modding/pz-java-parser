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
    property = []
    for match in matches:
        property.append(match.groupdict())

# parse the data file for tile properties
with open(DATA, "r") as f:
    data = yaml.safe_load(f)

    for name, obj in data["objects"].items():
        for prop in property:
            if prop["name"] == name:
                for key, value in obj.items():
                    prop[key] = value

with open(OUT, "w") as out_file:
    json.dump(property, out_file, indent=4)
