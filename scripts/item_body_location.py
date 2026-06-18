"""
Parses the ItemBodyLocation.java file to extract available body locations
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/scripting/objects/ItemBodyLocation.java")
OUT = Path("out/item_body_locations.json")

PATTERN = r"public static final ItemBodyLocation (?P<field>\w+) = registerBase\(\"(?P<name>\w+)\"\);"

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    body_locations = []
    for match in matches:
        body_location = match.groupdict()
        body_locations.append(body_location)

with open(OUT, "w") as out_file:
    json.dump(body_locations, out_file, indent=4)
