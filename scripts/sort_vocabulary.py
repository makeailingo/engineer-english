#!/usr/bin/env python3
"""Sort Engineer English vocabulary by chapter and learning order.

Workflow (see sorting-vocabulary SKILL):
1. Classify all entries into 5 chapters
2. Sort within each chapter
3. Concatenate chapters
4. Renumber IDs and rename files
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"

DIFFICULTY_RANK = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

# Architecture terms that belong in chapter 3 (planning / general design language).
ARCH_CH3_TERMS = frozenset(
    {
        "alternative",
        "approach",
        "balanced",
        "broad",
        "cautious",
        "communication",
        "compatibility",
        "contrast",
        "conventional",
        "credible",
        "decide",
        "delegate",
        "defend",
        "durable",
        "endorse",
        "eventually",
        "fallback",
        "feasible",
        "formal",
        "identical",
        "illustrate",
        "inconsistent",
        "independent",
        "interaction",
        "justify",
        "legacy",
        "lightweight",
        "logical",
        "mature",
        "naive",
        "operation",
        "ordering",
        "phase out",
        "preserve",
        "relay",
        "segment",
        "think through",
        "thereby",
        "ultimately",
        "viable",
    }
)

# High learning-value terms for engineers (idiomatic / non-compositional).
HIGH_LEARNING_VALUE = frozenset(
    {
        "follow up",
        "wrap up",
        "clarify",
        "reach out",
        "heads-up",
        "point out",
        "hold off",
        "sort out",
        "touch base",
        "loop in",
        "circle back",
        "chime in",
        "iron out",
        "weigh in",
        "get around to",
        "push back",
        "check in",
        "bring up",
        "sync up",
        "get up to speed",
        "on the same page",
        "in the loop",
        "deep dive",
        "sanity check",
        "catch up",
        "come up",
        "end up",
        "follow through",
        "figure out",
        "call out",
        "dig into",
        "look into",
        "rule out",
        "track down",
        "narrow down",
        "kick in",
        "turn out",
        "run into",
        "try out",
        "set up",
        "act on",
        "make a note of",
        "good to go",
        "gotcha",
        "heads up",
        "pushback",
        "trade-off",
        "edge case",
        "happy path",
        "smoke test",
        "hotfix",
        "workaround",
        "off-by-one",
        "race condition",
        "memory leak",
        "stack trace",
        "feature flag",
        "release candidate",
        "code health",
        "nitpick",
        "bikeshedding",
        "scope creep",
        "design decision",
        "under the hood",
        "think through",
        "mission-critical",
        "time complexity",
        "walk through",
        "brute force",
    }
)

# Obvious words with low learning value — deprioritize within a chapter.
LOW_LEARNING_VALUE = frozenset(
    {
        "update",
        "explain",
        "share",
        "confirm",
        "request",
        "respond",
        "mention",
        "inform",
        "notify",
        "note",
        "question",
        "status",
        "decide",
        "consider",
        "propose",
        "apply",
        "perform",
        "select",
        "swap",
        "currently",
        "previously",
        "shortly",
        "occasionally",
        "rarely",
        "frequently",
        "gradually",
        "slightly",
        "roughly",
        "automatically",
        "locally",
        "remotely",
        "alternative",
        "approach",
        "broad",
        "formal",
        "identical",
        "independent",
        "interaction",
        "operation",
        "communication",
        "logical",
    }
)

SCENE_CHAPTER = {
    "Daily Communication": 1,
    "Implementation": 2,
    "Code Review": 2,
    "Debugging": 2,
    "Testing": 2,
    "Sprint Planning": 3,
    "Requirements": 3,
    "Leadership / Management": 3,
    "Incident Response": 4,
    "Infrastructure / Cloud": 4,
    "Performance": 4,
    "Security": 4,
    "Database": 4,
    "Technical Interview": 5,
}

# Idiomatic communication phrases belong in chapter 1 even when scene is Code Review
# or Sprint Planning.
COMMUNICATION_CH1 = frozenset(
    {
        "bring up",
        "catch up",
        "check in",
        "chime in",
        "circle back",
        "clarify",
        "come up",
        "deep dive",
        "end up",
        "follow through",
        "follow up",
        "get around to",
        "get up to speed",
        "good to go",
        "gotcha",
        "heads-up",
        "hold off",
        "in the loop",
        "iron out",
        "loop in",
        "make a note of",
        "on the same page",
        "point out",
        "push back",
        "pushback",
        "reach out",
        "sanity check",
        "sort out",
        "sync up",
        "touch base",
        "weigh in",
        "wrap up",
    }
)

# Preferred opening order within chapter 1 (lower index = earlier).
CH1_OPENING_ORDER = {
    term: index
    for index, term in enumerate(
        [
            "follow up",
            "wrap up",
            "clarify",
            "reach out",
            "heads-up",
            "point out",
            "hold off",
            "sort out",
            "get around to",
            "push back",
            "check in",
            "bring up",
            "sync up",
            "touch base",
            "loop in",
            "get up to speed",
            "on the same page",
            "in the loop",
            "circle back",
            "chime in",
            "iron out",
            "weigh in",
            "deep dive",
            "sanity check",
            "catch up",
            "come up",
            "end up",
            "follow through",
        ]
    )
}


def classify_chapter(entry: dict) -> int:
    scene = entry["scene"]
    term = entry["term"]
    difficulty = entry["difficulty"]

    if term in COMMUNICATION_CH1:
        return 1

    if scene == "Architecture":
        if difficulty == "Beginner" or term in ARCH_CH3_TERMS:
            return 3
        return 5

    if scene == "Technical Interview":
        return 5

    chapter = SCENE_CHAPTER.get(scene)
    if chapter is None:
        raise ValueError(f"Unknown scene {scene!r} for term {term!r}")

    return chapter


def learning_value_score(entry: dict) -> int:
    term = entry["term"]
    score = 0

    if entry["type"] == "phrase":
        score += 80
    if " " in term or "-" in term:
        score += 40
    if term in HIGH_LEARNING_VALUE:
        score += 150
    if term in LOW_LEARNING_VALUE:
        score -= 120

    return score


def practicality_score(entry: dict) -> int:
    scene = entry["scene"]
    score = 0

    if scene == "Daily Communication":
        score += 50
    elif scene in {"Code Review", "Debugging", "Implementation", "Testing"}:
        score += 35
    elif scene in {"Sprint Planning", "Requirements", "Incident Response"}:
        score += 25
    elif scene in {"Architecture", "Technical Interview"}:
        score += 15

    if entry["type"] == "phrase":
        score += 10

    return score


def chapter_sort_key(entry: dict) -> tuple:
    if entry["_chapter"] == 1 and entry["term"] in CH1_OPENING_ORDER:
        return (
            0,
            CH1_OPENING_ORDER[entry["term"]],
            entry["term"],
        )
    return (
        1,
        -learning_value_score(entry),
        -practicality_score(entry),
        DIFFICULTY_RANK[entry["difficulty"]],
        entry["term"],
    )


def parse_entry(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid front matter: {path}")
    data = yaml.safe_load(match.group(1))
    body = match.group(2)
    data["_path"] = path
    data["_body"] = body
    return data, text


def term_slug(term: str) -> str:
    return term.lower().replace(" ", "-")


def write_entry(path: Path, entry: dict, new_id: str) -> None:
    original = path.read_text(encoding="utf-8")
    updated = re.sub(
        r'^id: "[0-9]{4}"',
        f'id: "{new_id}"',
        original,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(updated, encoding="utf-8")


def load_entries() -> list[dict]:
    entries = []
    for path in sorted(VOCAB_DIR.glob("*.md")):
        entry, _ = parse_entry(path)
        entries.append(entry)
    return entries


def sort_entries(entries: list[dict]) -> list[dict]:
    by_chapter: dict[int, list[dict]] = {i: [] for i in range(1, 6)}
    for entry in entries:
        chapter = classify_chapter(entry)
        entry["_chapter"] = chapter
        by_chapter[chapter].append(entry)

    ordered: list[dict] = []
    for chapter in range(1, 6):
        chapter_entries = sorted(by_chapter[chapter], key=chapter_sort_key)
        ordered.extend(chapter_entries)

    return ordered


def apply_renumber(ordered: list[dict], dry_run: bool = False) -> None:
    # Phase 1: rename to temporary names to avoid collisions.
    temp_paths: list[tuple[Path, Path]] = []
    for index, entry in enumerate(ordered, start=1):
        old_path: Path = entry["_path"]
        temp_path = old_path.with_name(f"__tmp_{index:04d}_{old_path.name}")
        temp_paths.append((old_path, temp_path))

    if not dry_run:
        for old_path, temp_path in temp_paths:
            old_path.rename(temp_path)

    # Phase 2: write final names and IDs.
    for index, entry in enumerate(ordered, start=1):
        new_id = f"{index:04d}"
        slug = term_slug(entry["term"])
        final_path = VOCAB_DIR / f"{new_id}_{slug}.md"
        _, temp_path = temp_paths[index - 1]
        entry["_new_id"] = new_id
        entry["_new_path"] = final_path
        if dry_run:
            continue
        write_entry(temp_path, entry, new_id)
        temp_path.rename(final_path)


def report(ordered: list[dict]) -> None:
    chapter_names = {
        1: "Ch1 基本コミュニケーション",
        2: "Ch2 開発とレビュー",
        3: "Ch3 計画と意思決定",
        4: "Ch4 運用と障害対応",
        5: "Ch5 高度な技術英語",
    }
    boundaries: dict[int, tuple[str, str, int]] = {}
    current = None
    for index, entry in enumerate(ordered, start=1):
        ch = entry["_chapter"]
        if ch != current:
            boundaries[ch] = (entry["term"], entry["term"], 1)
            current = ch
        start_term, _, _ = boundaries[ch]
        boundaries[ch] = (start_term, entry["term"], boundaries[ch][2] + (0 if boundaries[ch][1] == start_term else 0))

    # Recompute counts properly
    from collections import Counter

    counts = Counter(entry["_chapter"] for entry in ordered)
    print(f"Total entries: {len(ordered)}")
    for ch in range(1, 6):
        ch_entries = [e for e in ordered if e["_chapter"] == ch]
        if not ch_entries:
            print(f"  {chapter_names[ch]}: 0")
            continue
        start_id = ordered.index(ch_entries[0]) + 1
        end_id = ordered.index(ch_entries[-1]) + 1
        print(
            f"  {chapter_names[ch]}: {counts[ch]} entries "
            f"(IDs {start_id:04d}-{end_id:04d}, "
            f"{ch_entries[0]['term']} … {ch_entries[-1]['term']})"
        )

    ch5 = [e for e in ordered if e["_chapter"] == 5]
    ch5_beginner = [e["term"] for e in ch5 if e["difficulty"] == "Beginner"]
    print(f"\nCh5 Beginner count: {len(ch5_beginner)}")
    if ch5_beginner:
        print("  " + ", ".join(ch5_beginner))

    print("\nCh1 first 25 terms:")
    ch1 = [e["term"] for e in ordered if e["_chapter"] == 1][:25]
    print("  " + ", ".join(ch1))


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    entries = load_entries()
    if len(entries) != 995:
        print(f"Warning: expected 995 entries, found {len(entries)}", file=sys.stderr)

    ordered = sort_entries(entries)
    report(ordered)

    if dry_run:
        print("\n(dry run — no files changed)")
        return 0

    apply_renumber(ordered)
    print("\nRenumbering complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
