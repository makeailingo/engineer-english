#!/usr/bin/env python3
"""100語回帰: Skill 判断基準に沿った expected と現行 Vocabulary を比較する。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).parent
EXPECTED = EVAL_DIR / "regression_expected.json"
VOCAB = EVAL_DIR.parents[1] / "docs" / "vocabulary"

# 納得感が高いとされる代表例（現行維持を確認）
REFERENCE_TERMS = {
    "feedback": "Beginner",
    "clarify": "Intermediate",
    "courteous": "Advanced",
    "scrutiny": "Advanced",
    "trade-off": "Intermediate",
}

# 既知の不整合候補
MISJUDGMENT_CANDIDATES = [
    "critique", "replace", "reproduce", "isolate", "assertion",
    "coverage", "availability", "reliability", "capacity", "ownership",
]


def load_vocab() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(VOCAB.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        term = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', text, re.M)
        diff = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if term and diff:
            out[term.group(1).strip()] = diff.group(1).strip()
    return out


def main() -> int:
    if not EXPECTED.exists():
        print(f"Missing {EXPECTED}", file=sys.stderr)
        return 1

    expected: dict[str, dict] = json.loads(EXPECTED.read_text(encoding="utf-8"))
    vocab = load_vocab()

    if len(expected) != 100:
        print(f"FAIL: expected {len(expected)} terms, need 100")
        return 1
    if len(vocab) != 100:
        print(f"FAIL: vocabulary {len(vocab)} terms, need 100")
        return 1

    mismatches = []
    for term, entry in sorted(expected.items()):
        exp = entry["difficulty"]
        cur = vocab.get(term)
        if cur != exp:
            mismatches.append({"term": term, "current": cur, "expected": exp})

    ref_ok = [t for t, exp in REFERENCE_TERMS.items() if vocab.get(t) == exp]
    ref_ng = [(t, vocab.get(t), exp) for t, exp in REFERENCE_TERMS.items() if vocab.get(t) != exp]

    flagged_hit = [m["term"] for m in mismatches if m["term"] in MISJUDGMENT_CANDIDATES]

    print("=== Difficulty 回帰（100語）===\n")
    print(f"expected 語数: {len(expected)}")
    print(f"現行と不一致: {len(mismatches)}/100")
    print(f"代表例 維持: {len(ref_ok)}/{len(REFERENCE_TERMS)}")
    if ref_ng:
        print(f"  代表例 NG: {ref_ng}")
    print(f"不整合候補 検出: {len(flagged_hit)}/{len(MISJUDGMENT_CANDIDATES)}")
    print(f"  → {flagged_hit}")

    print("\n## 不一致一覧")
    for m in mismatches:
        print(f"  {m['term']:20} current={m['current']:12} expected={m['expected']}")

    ok = (
        len(expected) == 100
        and len(ref_ng) == 0
        and len(flagged_hit) >= 8
    )
    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
