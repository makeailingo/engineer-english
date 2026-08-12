#!/usr/bin/env python3
"""Renumber vocabulary IDs and filenames after Scene/difficulty order."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

VOCAB_DIR = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"

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


def parse_entry(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.S)
    fm = match.group(1)

    def field(name: str) -> str:
        m = re.search(rf'^\s*{name}:\s*"?([^"\n]+)"?\s*$', fm, re.M)
        return m.group(1).strip() if m else ""

    return {
        "path": path,
        "content": content,
        "id": field("id"),
        "term": field("term"),
        "scene": field("scene"),
        "difficulty": field("difficulty"),
    }


def slugify(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def main() -> None:
    entries = [parse_entry(p) for p in VOCAB_DIR.glob("*.md")]
    entries.sort(
        key=lambda e: (
            SCENE_ORDER.index(e["scene"]) if e["scene"] in SCENE_ORDER else 99,
            DIFFICULTY_ORDER.get(e["difficulty"], 9),
            e["term"].lower(),
        )
    )

    temp_dir = VOCAB_DIR / ".renumber_tmp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    for idx, entry in enumerate(entries, start=1):
        new_id = f"{idx:04d}"
        slug = slugify(entry["term"])
        new_name = f"{new_id}_{slug}.md"
        content = re.sub(r'^id: "[0-9]{4}"', f'id: "{new_id}"', entry["content"], count=1, flags=re.M)
        (temp_dir / new_name).write_text(content, encoding="utf-8")

    for old in VOCAB_DIR.glob("*.md"):
        old.unlink()
    for new_file in sorted(temp_dir.glob("*.md")):
        shutil.move(str(new_file), str(VOCAB_DIR / new_file.name))
    temp_dir.rmdir()
    print(f"Renumbered {len(entries)} vocabulary entries")


if __name__ == "__main__":
    main()
