"""
Parses 
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/core/properties/TilePropertyKey.java")
OUT = Path("out/tile_properties.json")

PATTERN = r'public static final TilePropertyKey (?P<field>\w+) = registerBase\("(?P<name>\w+)"\);'

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    property = []
    for match in matches:
        property.append(match.groupdict())

with open(OUT, "w") as out_file:
    json.dump(property, out_file, indent=4)
