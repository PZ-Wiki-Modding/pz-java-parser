import json, yaml, re, argparse
from pathlib import Path
from typing import TypedDict

from pylogs import echo

class ConfigEntry(TypedDict):
    pattern: str
    file: str
    out: str

def lowered(val: str) -> str:
    return val.lower()

Types = {
    "str": str,
    "int": int,
    "float": float,
    "lowered": lowered,
}

def convert_types(match: dict, typing: dict):
    for key, value in match.items():
        # it's optional to have a typing for each key
        # the value will stay a string
        if key not in typing:
            continue

        type_func = Types.get(typing[key])
        if type_func:
            try:
                match[key] = type_func(value)
            except TypeError as e:
                match[key] = value

        # only valid types are allowed
        else:
            raise ValueError(f"Unsupported type '{typing[key]}' for key '{key}'")
    return match

def parse_entry(entry: ConfigEntry):
    pattern = entry['pattern']
    java_file = Path(entry['file'])
    out_file = Path(entry['out'])
    typing = entry.get('typing', {})

    echo.path(java_file)

    if not java_file.exists():
        raise FileNotFoundError(f"Java file not found: {java_file}")
    if not java_file.is_file():
        raise FileNotFoundError(f"Java file is not a file: {java_file}")

    with open(java_file, "r") as f:
        java_content = f.read()

        matches = re.finditer(pattern, java_content)
        results = []
        for match in matches:
            results.append(convert_types(match.groupdict(), typing))

    with open(out_file, "w") as out_f:
        json.dump(results, out_f, indent=4, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description="Parse Java files to extract data based on regex patterns defined in a YAML config file.")
    parser.add_argument("config", type=str, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file is not a file: {config_path}")

    with open(config_path, "r") as f:
        config: list[ConfigEntry] = yaml.safe_load(f)

    for entry in config:
        parse_entry(entry)

if __name__ == "__main__":
    main()