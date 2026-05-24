"""
Parses the MagazineSubject.java file to extract available magazine subjects,
which are used in the magazine_subject item property for example.
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/scripting/objects/MagazineSubject.java")
OUT = Path("out/magazine_subject.json")

PATTERN = r'public static final MagazineSubject (?P<field>\w+) = registerBase\(\"(?P<name>\w+)\"\);'

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    magazine_subject = []
    for match in matches:
        magazine_subject.append(match.groupdict())

with open(OUT, "w") as out_file:
    json.dump(magazine_subject, out_file, indent=4)
