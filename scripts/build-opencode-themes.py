#!/usr/bin/env python3
"""Generate OpenCode terminal themes from the JetBrains Trash Panda theme."""

import json
import urllib.request
from pathlib import Path

# Theme variants from the upstream JetBrains theme repository.
THEMES = [
    "default",
    "default-2026",
    "starlight",
    "moonlight",
    "dawnlight",
    "daylight",
    "blacklight",
]

UPSTREAM_BASE_URL = (
    "https://raw.githubusercontent.com/jasonhulbert/jetbrains-trash-panda-theme"
    "/master/src/data"
)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / ".opencode" / "themes"

# Map JetBrains Trash Panda color roles to OpenCode theme roles.
ROLE_MAPPING = {
    "primary": "accent",
    "secondary": "blue",
    "accent": "accent",
    "error": "red",
    "warning": "orange",
    "success": "lime",
    "info": "cyan",
    "text": "base6",
    "textMuted": "base5",
    "background": "base2",
    "backgroundPanel": "base1",
    "backgroundElement": "base3",
    "border": "base3",
    "borderActive": "accent",
    "borderSubtle": "base4",
    "diffAdded": "lime",
    "diffRemoved": "red",
    "diffContext": "base5",
    "diffHunkHeader": "base4",
    "diffHighlightAdded": "lime",
    "diffHighlightRemoved": "red",
    "diffAddedBg": "lime_mod3",
    "diffRemovedBg": "red_mod3",
    "diffContextBg": "base2",
    "diffLineNumber": "base5",
    "diffAddedLineNumberBg": "lime_mod3",
    "diffRemovedLineNumberBg": "red_mod3",
    "markdownText": "base6",
    "markdownHeading": "purple",
    "markdownLink": "blue",
    "markdownLinkText": "cyan",
    "markdownCode": "lime",
    "markdownBlockQuote": "base5",
    "markdownEmph": "pink",
    "markdownStrong": "orange",
    "markdownHorizontalRule": "base4",
    "markdownListItem": "accent",
    "markdownListEnumeration": "cyan",
    "markdownImage": "blue",
    "markdownImageText": "cyan",
    "markdownCodeBlock": "base6",
    "syntaxComment": "base5",
    "syntaxKeyword": "purple",
    "syntaxFunction": "blue",
    "syntaxVariable": "pink",
    "syntaxString": "lime",
    "syntaxNumber": "orange",
    "syntaxType": "cyan",
    "syntaxOperator": "orange",
    "syntaxPunctuation": "base6",
}


def download_yaml(variant: str) -> str:
    url = f"{UPSTREAM_BASE_URL}/{variant}.yaml"
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def parse_yaml(content: str) -> dict:
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError as exc:
        raise RuntimeError(
            "PyYAML is required to build themes. "
            "Install it with: pip install pyyaml"
        ) from exc


def to_filename(variant: str) -> str:
    if variant == "default":
        return "trash-panda.json"
    return f"trash-panda-{variant}.json"


def build_theme(data: dict) -> dict:
    theme = data["theme"]

    defs = {}
    for key, value in theme.items():
        if key in ("transparent", "translucent"):
            continue
        defs[key] = f"#{value}"

    mapped_theme = {role: defs[source] for role, source in ROLE_MAPPING.items()}

    return {
        "$schema": "https://opencode.ai/theme.json",
        "defs": defs,
        "theme": mapped_theme,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for variant in THEMES:
        print(f"Building {variant}...")
        yaml_content = download_yaml(variant)
        data = parse_yaml(yaml_content)
        opencode_theme = build_theme(data)

        output_path = OUTPUT_DIR / to_filename(variant)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(opencode_theme, f, indent=2)
            f.write("\n")

    print(f"Done. Generated {len(THEMES)} themes in {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
