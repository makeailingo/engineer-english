#!/usr/bin/env python3
"""Difficulty 回帰: 決定表の整合性 + Golden Cases を検証する。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).parent
EXPECTED = EVAL_DIR / "regression_expected.json"
VOCAB = EVAL_DIR.parents[1] / "docs" / "vocabulary"

GOLDEN_CASES: dict[str, str] = {
    "feedback": "Beginner",
    "deadline": "Beginner",
    "clarify": "Intermediate",
    "defer": "Intermediate",
    "courteous": "Advanced",
    "scrutiny": "Advanced",
    "discretion": "Advanced",
}


def decide_difficulty(general: str, engineer: str) -> str:
    if general == "high" and engineer != "low":
        return "Beginner"
    if general == "low" and engineer == "low":
        return "Advanced"
    return "Intermediate"


def load_vocab() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(VOCAB.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        term = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', text, re.M)
        diff = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if term and diff:
            out[term.group(1).strip()] = diff.group(1).strip()
    return out


def load_expected(path: Path) -> dict[str, dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def rule_violations(expected: dict[str, dict]) -> list[str]:
    bad: list[str] = []
    for term, entry in sorted(expected.items()):
        r = entry["reasoning"]
        gf, ef = r["generalFamiliarity"], r["engineerFamiliarity"]
        computed = decide_difficulty(gf, ef)
        if entry["difficulty"] != computed:
            bad.append(f"{term}: recorded={entry['difficulty']} rule={computed} ({gf}/{ef})")
    return bad


def transition_report(baseline: dict[str, str], current: dict[str, str]) -> list[str]:
    changes: dict[tuple[str, str], list[str]] = {}
    for term in sorted(current.keys()):
        old, new = baseline.get(term), current[term]
        if old and old != new:
            changes.setdefault((old, new), []).append(term)

    lines = ["\n## baseline からの変化"]
    if not changes:
        lines.append("  （変化なし）")
        return lines
    for (old, new), terms in sorted(changes.items()):
        lines.append(f"  {old} → {new}: {len(terms)}語")
        lines.append(f"    {', '.join(terms)}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, help="前回 expected との diff 用 JSON")
    parser.add_argument("--show-vocab-diff", action="store_true", help="Vocabulary 不一致を表示")
    args = parser.parse_args()

    if not EXPECTED.exists():
        print(f"Missing {EXPECTED}", file=sys.stderr)
        return 1

    expected = load_expected(EXPECTED)
    if len(expected) != 100:
        print(f"FAIL: expected {len(expected)} terms, need 100")
        return 1

    violations = rule_violations(expected)
    golden_ng = [
        (t, expected[t]["difficulty"], exp)
        for t, exp in GOLDEN_CASES.items()
        if expected[t]["difficulty"] != exp
    ]

    print("=== Difficulty 回帰 ===\n")
    for level in ("Beginner", "Intermediate", "Advanced"):
        n = sum(1 for e in expected.values() if e["difficulty"] == level)
        print(f"{level}: {n}語")

    print(f"\n決定表 整合: {100 - len(violations)}/100")
    if violations:
        for v in violations:
            print(f"  NG: {v}")

    print(f"Golden Cases: {len(GOLDEN_CASES) - len(golden_ng)}/{len(GOLDEN_CASES)}")
    if golden_ng:
        print(f"  NG: {golden_ng}")

    if args.baseline and args.baseline.exists():
        baseline = {
            t: (v if isinstance(v, str) else v["difficulty"])
            for t, v in json.loads(args.baseline.read_text()).items()
        }
        current = {t: e["difficulty"] for t, e in expected.items()}
        for line in transition_report(baseline, current):
            print(line)

    if args.show_vocab_diff:
        vocab = load_vocab()
        if len(vocab) != 100:
            print(f"\nWARN: vocabulary {len(vocab)} terms")
        else:
            mismatches = [
                (t, vocab[t], expected[t]["difficulty"])
                for t in sorted(expected.keys())
                if vocab.get(t) != expected[t]["difficulty"]
            ]
            print(f"\nVocabulary 不一致: {len(mismatches)}/100")
            for term, cur, exp in mismatches:
                print(f"  {term:20} current={cur:12} expected={exp}")

    ok = len(violations) == 0 and len(golden_ng) == 0
    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
