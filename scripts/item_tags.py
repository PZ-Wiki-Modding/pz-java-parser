"""
Parses the ItemTag.java file to extract available item tags.
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/scripting/objects/ItemTag.java")
OUT = Path("out/item_tags.json")

PATTERN = r"ItemTag (?P<field>\S+) = registerBase\(\"(?P<name>\S+)\"\);"

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    item_tags = [match.groupdict() for match in matches]
    for tag in item_tags:
        tag['name'] = ("Base:" + tag['name']).lower()

with open(OUT, "w") as out_file:
    json.dump(item_tags, out_file, indent=4)
