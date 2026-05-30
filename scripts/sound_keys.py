import re, json
from pathlib import Path

JAVA = Path("ZomboidDecompiler/output/source/zombie/scripting/objects/SoundKey.java")
OUT = Path("out/sound_keys.json")

SOUND_KEYS_PATTERN = r'public static final SoundKey (?P<field>\w+) = registerBase\(\"(?P<id>\w+)\"\);'

# retrieve sound keys
sound_keys = []
with open(JAVA, "r") as f:
    java_content = f.read()

    matches = re.finditer(SOUND_KEYS_PATTERN, java_content)
    for match in matches:
        sound_keys.append(match.groupdict())

with open(OUT, "w") as out_file:
    json.dump(sound_keys, out_file, indent=4)
