#!/usr/bin/env python3
"""Generate additional Meetings / Events vocabulary markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from meetings_vocabulary_additions_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Meetings / Events"
START_ID = 777

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    "sorry for cutting in": {
        "type": "phrase",
        "partOfSpeech": "phrase",
        "pronunciation": "/ˈsɒri fə ˈkʌtɪŋ ɪn/",
        "meaning": "sorry for interrupting",
        "description": "Apologize before interrupting someone to ask a question or add a point.",
        "difficulty": "Intermediate",
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    "sorry for cutting in": "割り込んですみませんが、タイムラインを明確にしてもらえますか？",
}


def slug(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def word_count(text: str) -> int:
    return len(text.split())


def load_existing_terms() -> set[str]:
    terms: set[str] = set()
    if not VOCAB_DIR.exists():
        return terms
    term_re = re.compile(r'^term:\s*"(.*)"\s*$')
    for path in VOCAB_DIR.glob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = term_re.match(line)
            if match:
                terms.add(match.group(1))
                break
    return terms


def merge_entries() -> tuple[list[dict], list[str]]:
    existing = load_existing_terms()
    skipped: list[str] = []
    merged: list[dict] = []
    for user_index, user in enumerate(USER_ENTRIES):
        term = user["term"]
        if term in existing:
            skipped.append(term)
            continue
        if term not in METADATA:
            raise KeyError(f"Missing METADATA for term: {term}")
        if term not in USAGE_EXAMPLE_JA:
            raise KeyError(f"Missing USAGE_EXAMPLE_JA for term: {term}")
        entry = {**METADATA[term], **user}
        entry["usageExampleJa"] = USAGE_EXAMPLE_JA[term]
        entry["scene"] = SCENE
        entry["_user_index"] = user_index
        merged.append(entry)
    merged.sort(
        key=lambda e: (
            DIFFICULTY_ORDER[e["difficulty"]],
            e["_user_index"],
        )
    )
    for entry in merged:
        del entry["_user_index"]
    return merged, skipped


def validate(entry: dict, entry_id: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    term = entry["term"]
    if len(entry["description"]) > 120:
        errors.append(f"{entry_id} {term}: description > 120 chars ({len(entry['description'])})")
    if len(entry["descriptionJa"]) > 80:
        warnings.append(f"{entry_id} {term}: descriptionJa > 80 chars ({len(entry['descriptionJa'])})")
    if word_count(entry["usageExample"]) > 25:
        errors.append(
            f"{entry_id} {term}: usageExample > 25 words ({word_count(entry['usageExample'])})"
        )
    if len(entry["usageExampleJa"]) > 80:
        errors.append(
            f"{entry_id} {term}: usageExampleJa > 80 chars ({len(entry['usageExampleJa'])})"
        )
    return errors, warnings


def render(entry: dict, entry_id: str) -> str:
    return (
        "---\n"
        f'id: "{entry_id}"\n'
        f'term: "{entry["term"]}"\n'
        f'type: "{entry["type"]}"\n'
        f'partOfSpeech: "{entry["partOfSpeech"]}"\n'
        f'pronunciation: "{entry["pronunciation"]}"\n'
        f'description: "{entry["description"]}"\n'
        f'descriptionJa: "{entry["descriptionJa"]}"\n'
        f'meaning: "{entry["meaning"]}"\n'
        f'meaningJa: "{entry["meaningJa"]}"\n'
        f'usageExample: "{entry["usageExample"]}"\n'
        f'usageExampleJa: "{entry["usageExampleJa"]}"\n'
        f'difficulty: "{entry["difficulty"]}"\n'
        f'scene: "{SCENE}"\n'
        "---\n"
    )


def main() -> int:
    entries, skipped = merge_entries()
    VOCAB_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    all_errors: list[str] = []
    all_warnings: list[str] = []
    counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

    if skipped:
        print(f"Skipped duplicates ({len(skipped)}):")
        for term in skipped:
            print(f"  - {term}")

    for idx, entry in enumerate(entries, start=START_ID):
        term = entry["term"]
        if term in seen:
            all_errors.append(f"Duplicate term: {term}")
            continue
        seen.add(term)
        counts[entry["difficulty"]] += 1
        entry_id = f"{idx:04d}"
        errs, warns = validate(entry, entry_id)
        all_errors.extend(errs)
        all_warnings.extend(warns)
        path = VOCAB_DIR / f"{entry_id}_{slug(term)}.md"
        path.write_text(render(entry, entry_id), encoding="utf-8")

    print(f"Wrote {len(entries)} vocabulary files to {VOCAB_DIR}")
    print(
        "Difficulty counts: "
        f"Beginner={counts['Beginner']}, "
        f"Intermediate={counts['Intermediate']}, "
        f"Advanced={counts['Advanced']}"
    )
    if all_warnings:
        print(f"Warnings ({len(all_warnings)}):")
        for warn in all_warnings:
            print(f"  - {warn}")
    if all_errors:
        print(f"Validation failures ({len(all_errors)}):")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print("All validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
