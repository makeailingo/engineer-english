#!/usr/bin/env python3
"""Renumber vocabulary files by scene order, difficulty, and current ID."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"

SCENE_ORDER = [
    "Career / Interview",
    "Implementation / Review",
    "Meetings / Events",
    "Design / Architecture",
    "Incident Response",
    "Technical Writing",
    "Management",
]
DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

FIELD_RE = re.compile(r'^(\w+):\s*"(.*)"\s*$')


def slug(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def parse_file(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    fields: dict[str, str] = {}
    for line in lines:
        if line.strip() == "---":
            if fields:
                break
            continue
        match = FIELD_RE.match(line)
        if match:
            fields[match.group(1)] = match.group(2)
    fields["_path"] = path
    return fields


def render(fields: dict, entry_id: str) -> str:
    order = [
        "id",
        "term",
        "type",
        "partOfSpeech",
        "pronunciation",
        "description",
        "descriptionJa",
        "meaning",
        "meaningJa",
        "usageExample",
        "usageExampleJa",
        "difficulty",
        "scene",
    ]
    lines = ["---"]
    for key in order:
        lines.append(f'{key}: "{fields[key]}"')
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    files = sorted(VOCAB_DIR.glob("*.md"))
    entries = [parse_file(path) for path in files]

    for entry in entries:
        if entry["scene"] not in SCENE_ORDER:
            print(f"Unknown scene: {entry['scene']} in {entry['_path']}", file=sys.stderr)
            return 1

    entries.sort(
        key=lambda e: (
            SCENE_ORDER.index(e["scene"]),
            DIFFICULTY_ORDER[e["difficulty"]],
            int(e["id"]),
        )
    )

    temp_dir = VOCAB_DIR / ".renumber_tmp"
    temp_dir.mkdir(exist_ok=True)

    for idx, entry in enumerate(entries, start=1):
        entry_id = f"{idx:04d}"
        entry["id"] = entry_id
        term = entry["term"]
        temp_path = temp_dir / f"{entry_id}_{slug(term)}.md"
        temp_path.write_text(render(entry, entry_id), encoding="utf-8")

    for path in files:
        path.unlink()

    for temp_path in sorted(temp_dir.glob("*.md")):
        temp_path.rename(VOCAB_DIR / temp_path.name)

    temp_dir.rmdir()
    print(f"Renumbered {len(entries)} vocabulary files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
