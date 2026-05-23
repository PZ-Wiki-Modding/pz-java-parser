"""
Parses the ActionSoundTime.java file to extract available action sound events,
which are used in the timedAction block for example.

The regex is a bit weak sadly
"""

import json, re
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/scripting/objects/ActionSoundTime.java")
OUT = Path("out/action_sound_time.json")

PATTERN = r'(?P<enum>[A-Z_]+)\(\"(?P<name>\w+)\"\)[,;]'

with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(PATTERN, java_content)
    action_sound_time = []
    for match in matches:
        action_sound_time.append(match.groupdict())

with open(OUT, "w") as out_file:
    json.dump(action_sound_time, out_file, indent=4)
