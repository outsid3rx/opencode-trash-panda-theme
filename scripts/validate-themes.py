#!/usr/bin/env python3
"""Validate generated OpenCode theme files against the official JSON schema."""

import json
from pathlib import Path

import jsonschema

SCHEMA_FILE = Path(__file__).resolve().parent / "theme-schema.json"
THEMES_DIR = Path(__file__).resolve().parent.parent / ".opencode" / "themes"


def main() -> None:
    print(f"Loading schema from {SCHEMA_FILE}...")
    with SCHEMA_FILE.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = jsonschema.Draft7Validator(schema)
    errors = 0

    for theme_file in sorted(THEMES_DIR.glob("*.json")):
        print(f"Validating {theme_file.name}...")
        with theme_file.open("r", encoding="utf-8") as f:
            theme = json.load(f)

        file_errors = list(validator.iter_errors(theme))
        if file_errors:
            errors += len(file_errors)
            print(f"  {len(file_errors)} error(s) in {theme_file.name}:")
            for err in file_errors:
                print(f"    - {err.message} at {list(err.path)}")
        else:
            print(f"  {theme_file.name} is valid.")

    if errors:
        raise SystemExit(f"Validation failed with {errors} error(s).")

    print("All themes are valid.")


if __name__ == "__main__":
    main()
