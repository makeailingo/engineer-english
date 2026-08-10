#!/usr/bin/env python3
"""
POC: rubric + アンカー方式の回帰 Eval

外部データは使わない。ゴールドセット（anchor_gold.yaml）と
Skill に沿って人手で固定した expected 表（poc_anchor_expected.json）を比較する。

実行:
  python3 evals/difficulty/poc_anchor.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

POC_DIR = Path(__file__).parent
GOLD = POC_DIR / "anchor_gold.yaml"
EXPECTED = POC_DIR / "poc_anchor_expected.json"
VOCAB = POC_DIR.parents[1] / "docs" / "vocabulary"


def load_yaml_simple(path: Path) -> dict:
    """最小 YAML パーサ（anchor_gold 専用）。"""
    data: dict = {}
    section = None
    sub = None
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.endswith(":") and not s.startswith("-"):
            key = s[:-1]
            if key in ("anchors", "flagged_expected", "anchor_expected"):
                section = key
                data[section] = {} if section != "anchors" else {}
                sub = None
            continue
        if section == "anchors" and s.endswith(":"):
            sub = s[:-1]
            data["anchors"][sub] = []
            continue
        if section == "anchors" and s.startswith("- "):
            data["anchors"][sub].append(s[2:].strip())
            continue
        if section in ("flagged_expected", "anchor_expected") and ":" in s:
            k, v = s.split(":", 1)
            data[section][k.strip()] = v.strip()
    return data


def load_vocab() -> dict[str, str]:
    out = {}
    for p in sorted(VOCAB.glob("*.md")):
        t = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', p.read_text(), re.M)
        d = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', p.read_text(), re.M)
        if t and d:
            out[t.group(1).strip()] = d.group(1).strip()
    return out


def main() -> int:
    gold = load_yaml_simple(GOLD)
    expected = json.loads(EXPECTED.read_text())
    vocab = load_vocab()

    flagged = gold["flagged_expected"]
    anchors = gold["anchor_expected"]

    # flagged: rubric expected vs current
    flagged_detected = []
    for term, exp in flagged.items():
        cur = vocab.get(term)
        if cur and cur != exp:
            flagged_detected.append(term)

    # anchors: rubric expected vs current (should match expected = anchor)
    # 核心アンカー（納得感が高い5語）— 現行と一致必須
    core_anchors = {
        "feedback": "Beginner",
        "clarify": "Intermediate",
        "courteous": "Advanced",
        "scrutiny": "Advanced",
        "trade-off": "Intermediate",
    }
    core_ok = [t for t, exp in core_anchors.items() if vocab.get(t) == exp]
    core_ng = [(t, vocab.get(t), exp) for t, exp in core_anchors.items() if vocab.get(t) != exp]

    # 拡張アンカー（Skill 例示。現行不一致は vocab 側の修正候補として報告）
    ext_ng = [(t, vocab.get(t), exp) for t, exp in anchors.items() if t not in core_anchors and vocab.get(t) != exp]

    # rubric judgments in expected file vs gold
    rubric_match = sum(
        1 for term, exp in {**flagged, **anchors}.items()
        if expected.get(term, {}).get("difficulty") == exp
    )
    rubric_total = len(flagged) + len(anchors)

    print("=== Anchor Rubric POC ===\n")
    print(f"Rubric expected 一致: {rubric_match}/{rubric_total}")
    print(f"\nflagged 検出（現行≠rubric期待）: {len(flagged_detected)}/{len(flagged)}")
    print(f"  → {flagged_detected}")
    print(f"\ncore anchor 維持: {len(core_ok)}/{len(core_anchors)}")
    if core_ng:
        print(f"  NG: {core_ng}")
    if ext_ng:
        print(f"拡張 anchor 不一致（vocab修正候補）: {ext_ng}")

    # 不整合の詳細
    print("\n## flagged 詳細")
    for term in flagged:
        exp = flagged[term]
        cur = vocab.get(term, "?")
        r = expected.get(term, {})
        mark = "≠" if cur != exp else "="
        print(f"  {term:15} current={cur:12} rubric={exp:12} {mark}")
        if r.get("reasoning"):
            print(f"    reasoning: {r['reasoning']}")

    ok = (
        len(flagged_detected) >= 8
        and len(core_ng) == 0
        and rubric_match == rubric_total
    )
    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
