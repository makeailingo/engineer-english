#!/usr/bin/env python3
"""Mechanical QA checks for vocabulary markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"

FIELD_RE = re.compile(r'^(\w+):\s*"(.*)"\s*$')
REQUIRED_FIELDS = [
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
VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}
VALID_SCENES = {
    "Career / Interview",
    "Implementation / Review",
    "Meetings / Events",
    "Design / Architecture",
    "Incident Response",
    "Technical Writing",
    "Management",
}

ENGLISH_PATTERNS = [
    (re.compile(r"\ba A\b"), "duplicate article before placeholder A"),
    (re.compile(r"\bwas disagreed\b"), "invalid grammar: was disagreed"),
    (re.compile(r"\bstate or incomplete\b"), "likely typo: state or incomplete"),
    (re.compile(r"\b神調\b"), "Japanese typo: 神調"),
    (re.compile(r"（最後"), "broken Japanese meaningJa parentheses"),
]

JAPANESE_PATTERNS = [
    (re.compile(r"神調"), "Japanese typo: 神調"),
    (re.compile(r"（最後"), "broken Japanese parentheses in meaningJa"),
]


def parse_file(path: Path) -> dict[str, str]:
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
    return fields


def word_count(text: str) -> int:
    return len(text.split())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    terms: dict[str, str] = {}

    for path in sorted(VOCAB_DIR.glob("*.md")):
        fields = parse_file(path)
        entry_id = fields.get("id", path.stem)

        for field in REQUIRED_FIELDS:
            if field not in fields or not fields[field].strip():
                errors.append(f"{entry_id} {path.name}: missing {field}")

        term = fields.get("term", "")
        if term in terms:
            errors.append(f"{entry_id} {path.name}: duplicate term '{term}' (also in {terms[term]})")
        elif term:
            terms[term] = path.name

        if fields.get("difficulty") not in VALID_DIFFICULTIES:
            errors.append(f"{entry_id} {path.name}: invalid difficulty")

        if fields.get("scene") not in VALID_SCENES:
            errors.append(f"{entry_id} {path.name}: invalid scene")

        if len(fields.get("description", "")) > 120:
            errors.append(f"{entry_id} {path.name}: description > 120 chars")

        if len(fields.get("descriptionJa", "")) > 80:
            warnings.append(f"{entry_id} {path.name}: descriptionJa > 80 chars")

        if word_count(fields.get("usageExample", "")) > 25:
            errors.append(f"{entry_id} {path.name}: usageExample > 25 words")

        if len(fields.get("usageExampleJa", "")) > 80:
            errors.append(f"{entry_id} {path.name}: usageExampleJa > 80 chars")

        combined_en = " ".join(
            fields.get(key, "")
            for key in ("term", "meaning", "description", "usageExample")
        )
        for pattern, message in ENGLISH_PATTERNS:
            if pattern.search(combined_en):
                errors.append(f"{entry_id} {path.name}: {message}")

        combined_ja = " ".join(
            fields.get(key, "")
            for key in ("meaningJa", "descriptionJa", "usageExampleJa")
        )
        for pattern, message in JAPANESE_PATTERNS:
            if pattern.search(combined_ja):
                errors.append(f"{entry_id} {path.name}: {message}")

        expected_slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        if not path.name.endswith(f"_{expected_slug}.md") and term:
            warnings.append(f"{entry_id} {path.name}: filename slug mismatch for term '{term}'")

    print(f"Checked {len(list(VOCAB_DIR.glob('*.md')))} vocabulary files.")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for warn in warnings[:20]:
            print(f"  - {warn}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("All validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
