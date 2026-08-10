#!/usr/bin/env python3
"""
POC: Difficulty Eval の再現性検証

検証項目:
  1. 同一語を2回取得して CEFR が一致するか
  2. 凍結フィクスチャから Eval 結果が決定的か
  3. 既知の不整合ペアを ordering inversion で検出できるか
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
CEFR_RANK = {lv: i for i, lv in enumerate(CEFR_LEVELS, 1)}
DIFF_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
USER_AGENT = "EngineerEnglishDifficultyEval-POC/1.0"

# ユーザーが指摘した代表語 + アンカー語
POC_TERMS = [
    "critique", "replace", "reproduce", "isolate", "assertion",
    "coverage", "availability", "reliability", "capacity", "ownership",
    "feedback", "clarify", "courteous", "scrutiny", "invoke",
]

# 現行 Vocabulary の difficulty（手動確認済み）
CURRENT = {
    "critique": "Beginner", "replace": "Advanced", "reproduce": "Advanced",
    "isolate": "Beginner", "assertion": "Beginner", "coverage": "Beginner",
    "availability": "Beginner", "reliability": "Beginner", "capacity": "Beginner",
    "ownership": "Beginner", "feedback": "Beginner", "clarify": "Intermediate",
    "courteous": "Advanced", "scrutiny": "Advanced", "invoke": "Intermediate",
}

# 期待される検出（POC 成功条件）
EXPECTED_INVERSIONS = [
    ("replace", "invoke"),   # B1=Advanced vs C1=Intermediate
]
EXPECTED_SAME_CEFR_SPLITS = [
    "C1",  # critique=Beginner vs clarify=Intermediate 等
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def highest(levels: list[str]) -> str | None:
    if not levels:
        return None
    return max(levels, key=lambda x: CEFR_RANK[x])


def parse_cambridge(html: str) -> str | None:
    return highest(re.findall(r">\s*(A1|A2|B1|B2|C1|C2)\s*<", html))


def parse_oxford(html: str) -> str | None:
    a = re.findall(r'cefr="(A1|A2|B1|B2|C1|C2)"', html, re.I)
    b = re.findall(r"Topics[^<]*?(A1|A2|B1|B2|C1|C2)", html, re.I)
    return highest([x.upper() for x in a + b])


def lookup(term: str) -> dict:
    slug = term.lower().replace(" ", "-")
    cam_url = f"https://dictionary.cambridge.org/dictionary/english/{slug}"
    ox_url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{slug}"
    cam = ox = None
    errors = []
    try:
        cam = parse_cambridge(fetch(cam_url))
    except Exception as e:
        errors.append(f"cambridge: {e}")
    time.sleep(0.5)
    try:
        ox = parse_oxford(fetch(ox_url))
    except Exception as e:
        errors.append(f"oxford: {e}")

    if cam and ox:
        adopted = cam if cam == ox else highest([cam, ox])
        method = "both" if cam == ox else "both_max"
    elif cam:
        adopted, method = cam, "cambridge"
    elif ox:
        adopted, method = ox, "oxford"
    else:
        adopted, method = None, "none"

    return {
        "term": term, "cambridge": cam, "oxford": ox,
        "adopted": adopted, "method": method, "errors": errors,
    }


def check_reproducibility(records_a: list[dict], records_b: list[dict]) -> dict:
    mismatches = []
    for a, b in zip(records_a, records_b):
        if a["adopted"] != b["adopted"]:
            mismatches.append({
                "term": a["term"],
                "run1": a["adopted"], "run2": b["adopted"],
                "run1_detail": {"cambridge": a["cambridge"], "oxford": a["oxford"]},
                "run2_detail": {"cambridge": b["cambridge"], "oxford": b["oxford"]},
            })
    return {"passed": len(mismatches) == 0, "mismatches": mismatches}


def detect_inversions(ref: dict[str, str], current: dict[str, str]) -> list[dict]:
    findings = []
    terms = sorted(ref.keys())
    for i, ta in enumerate(terms):
        for tb in terms[i + 1:]:
            ca, cb = ref[ta], ref[tb]
            if CEFR_RANK[ca] == CEFR_RANK[cb]:
                continue
            if CEFR_RANK[ca] > CEFR_RANK[cb]:
                hard, easy, c_hard, c_easy = ta, tb, ca, cb
            else:
                hard, easy, c_hard, c_easy = tb, ta, cb, ca
            if DIFF_RANK[current[hard]] < DIFF_RANK[current[easy]]:
                findings.append({
                    "harder": hard, "harder_cefr": c_hard,
                    "harder_current": current[hard],
                    "easier": easy, "easier_cefr": c_easy,
                    "easier_current": current[easy],
                })
    return findings


def detect_same_cefr_splits(ref: dict[str, str], current: dict[str, str]) -> dict[str, list[str]]:
    by_cefr: dict[str, set[str]] = {}
    for term, cefr in ref.items():
        by_cefr.setdefault(cefr, set()).add(current[term])
    return {c: sorted(labels) for c, labels in by_cefr.items() if len(labels) > 1}


def main() -> int:
    print("=" * 60)
    print("POC 1: ライブ取得の再現性（同一語を2回取得）")
    print("=" * 60)

    run1, run2 = [], []
    for term in POC_TERMS:
        print(f"  fetch x2: {term}", flush=True)
        run1.append(lookup(term))
        time.sleep(0.5)
        run2.append(lookup(term))
        time.sleep(0.5)

    repro = check_reproducibility(run1, run2)
    print(f"\n再現性: {'PASS' if repro['passed'] else 'FAIL'}")
    if repro["mismatches"]:
        for m in repro["mismatches"]:
            print(f"  MISMATCH {m['term']}: run1={m['run1']} run2={m['run2']}")
            print(f"    detail1={m['run1_detail']} detail2={m['run2_detail']}")

    print("\n取得結果 (run1):")
    for r in run1:
        print(f"  {r['term']:15} cam={r['cambridge'] or '-':3} ox={r['oxford'] or '-':3} "
              f"adopted={r['adopted'] or 'NONE':4} method={r['method']}"
              + (f" ERR={r['errors']}" if r['errors'] else ""))

    ref = {r["term"]: r["adopted"] for r in run1 if r["adopted"]}
    missing = [t for t in POC_TERMS if t not in ref]
    print(f"\nCEFR 取得率: {len(ref)}/{len(POC_TERMS)}")
    if missing:
        print(f"  未取得: {missing}")

    print("\n" + "=" * 60)
    print("POC 2: 凍結フィクスチャからの決定的 Eval")
    print("=" * 60)

    fixture = {"terms": run1}
    frozen = json.dumps(fixture, sort_keys=True)
    ref_from_frozen = {
        item["term"]: item["adopted"]
        for item in json.loads(frozen)["terms"]
        if item["adopted"]
    }
    inv1 = detect_inversions(ref_from_frozen, CURRENT)
    inv2 = detect_inversions(ref_from_frozen, CURRENT)
    deterministic = inv1 == inv2
    print(f"決定性: {'PASS' if deterministic else 'FAIL'} (2回同一結果)")

    print("\n" + "=" * 60)
    print("POC 3: 既知不整合の検出")
    print("=" * 60)

    inversions = detect_inversions(ref, CURRENT)
    splits = detect_same_cefr_splits(ref, CURRENT)

    print(f"\nOrdering inversions ({len(inversions)}):")
    for f in inversions:
        print(f"  {f['harder']} ({f['harder_cefr']},{f['harder_current']}) "
              f"< {f['easier']} ({f['easier_cefr']},{f['easier_current']})")

    print(f"\nSame-CEFR splits:")
    for cefr, labels in sorted(splits.items()):
        terms = [t for t, c in ref.items() if c == cefr]
        detail = {l: [t for t in terms if CURRENT[t] == l] for l in labels}
        print(f"  {cefr}: {labels} -> {detail}")

    # 期待検出の確認
    detected_pairs = {(f["harder"], f["easier"]) for f in inversions}
    inv_ok = all(p in detected_pairs or (p[1], p[0]) not in detected_pairs
                 for p in EXPECTED_INVERSIONS)
    # replace/invoke: replace is easier CEFR but harder current -> inversion
    replace_invoke_ok = ("replace", "invoke") not in detected_pairs and \
        any(f["harder"] == "invoke" and f["easier"] == "replace" for f in inversions)

    print("\n期待検出:")
    print(f"  replace vs invoke inversion: {'PASS' if replace_invoke_ok else 'FAIL'}")
    print(f"  C1 same-CEFR split exists: {'PASS' if 'C1' in splits else 'FAIL'}")

    # 総合判定
    all_pass = (
        repro["passed"]
        and len(missing) == 0
        and deterministic
        and replace_invoke_ok
        and "C1" in splits
    )

    print("\n" + "=" * 60)
    print(f"POC 総合: {'PASS - 100%再現可能と言える' if all_pass else 'FAIL - 再現性に問題あり'}")
    print("=" * 60)

    if not repro["passed"]:
        print("\n⚠ ライブ取得が run 間で不一致 → 凍結フィクスチャ必須、ライブ取得は更新用途のみ")
    if missing:
        print(f"\n⚠ CEFR 未取得語あり → スクレイピング精度不足")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
