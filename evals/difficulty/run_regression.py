#!/usr/bin/env python3
"""100語回帰: Golden Cases 検証 + baseline 差分 + Vocabulary 比較。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).parent
EXPECTED = EVAL_DIR / "regression_expected.json"
BASELINE = EVAL_DIR / "regression_baseline.json"
VOCAB = EVAL_DIR.parents[1] / "docs" / "vocabulary"

LEVELS = ("Beginner", "Intermediate", "Advanced")

# 明らかな期待値（境界語は含めない）
GOLDEN_CASES: dict[str, str] = {
    "feedback": "Beginner",
    "deadline": "Beginner",
    "clarify": "Intermediate",
    "defer": "Intermediate",
    "courteous": "Advanced",
    "scrutiny": "Advanced",
    "discretion": "Advanced",
}


def load_vocab() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(VOCAB.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        term = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', text, re.M)
        diff = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if term and diff:
            out[term.group(1).strip()] = diff.group(1).strip()
    return out


def load_difficulties(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for term, entry in data.items():
        if isinstance(entry, str):
            out[term] = entry
        else:
            out[term] = entry["difficulty"]
    return out


def transition_report(baseline: dict[str, str], current: dict[str, str]) -> list[str]:
    lines: list[str] = []
    changes: dict[tuple[str, str], list[str]] = {}

    for term in sorted(current.keys()):
        old = baseline.get(term)
        new = current[term]
        if old and old != new:
            changes.setdefault((old, new), []).append(term)

    lines.append("## baseline からの変化")
    if not changes:
        lines.append("  （変化なし）")
    else:
        for (old, new), terms in sorted(changes.items()):
            lines.append(f"  {old} → {new}: {len(terms)}語")
            lines.append(f"    {', '.join(terms)}")
    return lines


def main() -> int:
    if not EXPECTED.exists():
        print(f"Missing {EXPECTED}", file=sys.stderr)
        return 1

    expected = load_difficulties(EXPECTED)
    vocab = load_vocab()

    if len(expected) != 100:
        print(f"FAIL: expected {len(expected)} terms, need 100")
        return 1
    if len(vocab) != 100:
        print(f"FAIL: vocabulary {len(vocab)} terms, need 100")
        return 1

    golden_ok = [t for t, exp in GOLDEN_CASES.items() if expected.get(t) == exp]
    golden_ng = [(t, expected.get(t), exp) for t, exp in GOLDEN_CASES.items() if expected.get(t) != exp]

    vocab_mismatches = [
        {"term": t, "current": vocab[t], "expected": expected[t]}
        for t in sorted(expected.keys())
        if vocab.get(t) != expected[t]
    ]

    print("=== Difficulty 回帰（100語）===\n")
    for level in LEVELS:
        n = sum(1 for d in expected.values() if d == level)
        print(f"{level}: {n}語")

    print(f"\nGolden Cases: {len(golden_ok)}/{len(GOLDEN_CASES)}")
    if golden_ng:
        print(f"  NG: {golden_ng}")

    print(f"現行 Vocabulary 不一致: {len(vocab_mismatches)}/100")

    if BASELINE.exists():
        baseline = load_difficulties(BASELINE)
        for line in transition_report(baseline, expected):
            print(line)
    else:
        print("\n## baseline からの変化")
        print("  （regression_baseline.json なし）")

    if vocab_mismatches:
        print("\n## Vocabulary 不一致")
        for m in vocab_mismatches:
            print(f"  {m['term']:20} current={m['current']:12} expected={m['expected']}")

    ok = len(expected) == 100 and len(golden_ng) == 0
    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
