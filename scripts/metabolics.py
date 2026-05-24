"""
Parses the Metabolics.java file to extract available metabolics and
their associated value. Used for timedAction script blocks for example.
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/characters/BodyDamage/Metabolics.java")
OUT = Path("out/metabolics.json")

PATTERN = r'(?P<enum>\w+)\((?P<value>\d+.\d+)F\)[,;]'

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    metabolics = []
    for match in matches:
        grp = match.groupdict()
        grp['value'] = float(grp['value'])
        metabolics.append(grp)


with open(OUT, "w") as out_file:
    json.dump(metabolics, out_file, indent=4)
