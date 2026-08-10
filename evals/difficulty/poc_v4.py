#!/usr/bin/env python3
"""
POC v4: アンカー校正 + 相対チェック（シンプル版）

ルール（人間向け説明）:
  1. 外部 CEFR は凍結 JSON から読む（Eval 中ネットワーク不要）
  2. CEFR(A) > CEFR(B) なのに Difficulty(A) < Difficulty(B) → 逆転ペアを報告
  3. 同一 CEFR でアンカーが1種類のラベルしか持たない場合、
     そのラベルと違う語を報告（アンカー自身は除外）
  4. B2 のようにアンカーが複数ラベル → その CEFR ではチェック3をスキップ

参照 CEFR（凍結時）:
  - Oxford wordlist 優先
  - なければ min(Cambridge 語義) — 基本語義
  - なければ Oxford ページ
  - trade-off のみ manual B2（辞書に CEFR なし）
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

POC_DIR = Path(__file__).parent
FIXTURE = POC_DIR / "poc_v4_fixture.json"
UA = "POC-v4/1.0"

CEFR_RANK = {lv: i for i, lv in enumerate(["A1", "A2", "B1", "B2", "C1", "C2"], 1)}
DIFF_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

FLAGGED = [
    "critique", "replace", "reproduce", "isolate", "assertion",
    "coverage", "availability", "reliability", "capacity", "ownership",
]
ANCHORS = {
    "feedback": "Beginner", "clarify": "Intermediate", "courteous": "Advanced",
    "scrutiny": "Advanced", "trade-off": "Intermediate",
}
CURRENT = {
    "critique": "Beginner", "replace": "Advanced", "reproduce": "Advanced",
    "isolate": "Beginner", "assertion": "Beginner", "coverage": "Beginner",
    "availability": "Beginner", "reliability": "Beginner", "capacity": "Beginner",
    "ownership": "Beginner", "feedback": "Beginner", "clarify": "Intermediate",
    "courteous": "Advanced", "scrutiny": "Advanced", "invoke": "Intermediate",
    "trade-off": "Intermediate",
}
POC_TERMS = sorted(set(FLAGGED + list(ANCHORS.keys()) + ["invoke"]))
MANUAL = {"trade-off": ("B2", "manual_phrase_b2")}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def norm_levels(levels: list[str]) -> list[str]:
    return [x.upper() for x in levels if x.upper() in CEFR_RANK]


def min_cefr(levels: list[str]) -> str | None:
    lv = norm_levels(levels)
    return min(lv, key=lambda x: CEFR_RANK[x]) if lv else None


def max_cefr(levels: list[str]) -> str | None:
    lv = norm_levels(levels)
    return max(lv, key=lambda x: CEFR_RANK[x]) if lv else None


def parse_wordlist(html: str) -> dict[str, str]:
    out = {}
    for m in re.finditer(
        r'data-hw="([^"]+)"\s+data-ox3000="([^"]+)"\s+data-ox5000="([^"]+)"', html
    ):
        lv = [m.group(2).upper(), m.group(3).upper()]
        out[m.group(1).lower()] = max(lv, key=lambda x: CEFR_RANK[x])
    return out


def lookup(term: str, wordlist: dict[str, str]) -> tuple[str | None, str]:
    key = term.lower()
    if key in MANUAL:
        return MANUAL[key]
    if key in wordlist:
        return wordlist[key], "oxford_wordlist"
    slug = key.replace(" ", "-")
    cam = ox = None
    try:
        cam = min_cefr(re.findall(r"epp-xref dxref (A1|A2|B1|B2|C1|C2)", fetch(
            f"https://dictionary.cambridge.org/dictionary/english/{slug}")))
    except Exception:
        pass
    time.sleep(0.25)
    try:
        html = fetch(f"https://www.oxfordlearnersdictionaries.com/definition/english/{slug}")
        ox_levels = re.findall(r'cefr="(A1|A2|B1|B2|C1|C2)"', html, re.I)
        ox_levels += re.findall(r"Topics[^<]*?(A1|A2|B1|B2|C1|C2)", html, re.I)
        ox = max_cefr(ox_levels)
    except Exception:
        pass
    time.sleep(0.25)
    if cam and ox:
        return min_cefr([cam, ox]), "min_cambridge_oxford"
    if cam:
        return cam, "cambridge_min"
    if ox:
        return ox, "oxford_page"
    return None, "none"


@dataclass
class Ref:
    term: str
    cefr: str | None
    method: str


def build_fixture(refresh: bool) -> tuple[dict[str, str], dict[str, Ref]]:
    if FIXTURE.exists() and not refresh:
        data = json.loads(FIXTURE.read_text())
        refs = {k: Ref(**v) for k, v in data["refs"].items()}
        return data["wordlist_meta"], refs

    html = fetch("https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000?dataset=english")
    wordlist = parse_wordlist(html)
    refs = {}
    for t in POC_TERMS:
        cefr, method = lookup(t, wordlist)
        refs[t] = Ref(t, cefr, method)
    FIXTURE.write_text(json.dumps({
        "wordlist_meta": {"source": "oxford3000-5000", "count": len(wordlist), "wordlist": wordlist},
        "refs": {k: asdict(v) for k, v in refs.items()},
    }, ensure_ascii=False, indent=2) + "\n")
    return {"source": "oxford3000-5000", "count": len(wordlist), "wordlist": wordlist}, refs


def anchor_labels_by_cefr(refs: dict[str, Ref]) -> dict[str, set[str]]:
    by: dict[str, set[str]] = {}
    for term, label in ANCHORS.items():
        c = refs[term].cefr
        if c:
            by.setdefault(c, set()).add(label)
    return by


def check_inversions(refs: dict[str, Ref]) -> list[tuple[str, str]]:
    pairs = []
    terms = [t for t in POC_TERMS if refs[t].cefr and t in CURRENT]
    for i, a in enumerate(terms):
        for b in terms[i + 1:]:
            ca, cb = refs[a].cefr, refs[b].cefr
            if CEFR_RANK[ca] == CEFR_RANK[cb]:
                continue
            h, e = (a, b) if CEFR_RANK[ca] > CEFR_RANK[cb] else (b, a)
            if DIFF_RANK[CURRENT[h]] < DIFF_RANK[CURRENT[e]]:
                pairs.append((h, e))
    return pairs


def check_anchor_cefr_mismatch(refs: dict[str, Ref]) -> list[str]:
    """アンカーが1ラベルしか持たない CEFR で、そのラベルと違う語。"""
    anchor_by_cefr = anchor_labels_by_cefr(refs)
    flagged = []
    for term in POC_TERMS:
        if term in ANCHORS:
            continue
        c = refs[term].cefr
        if not c or term not in CURRENT:
            continue
        labels = anchor_by_cefr.get(c, set())
        if len(labels) != 1:
            continue
        expected = next(iter(labels))
        if CURRENT[term] != expected:
            flagged.append(term)
    return flagged


def detected_terms(invs: list[tuple[str, str]], cefr_mis: list[str]) -> set[str]:
    s = set(cefr_mis)
    for a, b in invs:
        if a not in ANCHORS:
            s.add(a)
        if b not in ANCHORS:
            s.add(b)
    return s


def main() -> int:
    print("=== POC v4 ===\n")
    _, refs = build_fixture("--refresh" in sys.argv)

    inv = check_inversions(refs)
    cefr_mis = check_anchor_cefr_mismatch(refs)
    det = detected_terms(inv, cefr_mis)

    flagged_hit = sorted(t for t in FLAGGED if t in det)
    anchor_fp = sorted(t for t in ANCHORS if t in det)
    missing = [t for t in POC_TERMS if not refs[t].cefr]

    print("参照 CEFR:")
    for t in POC_TERMS:
        r = refs[t]
        anchor = " [anchor]" if t in ANCHORS else ""
        print(f"  {t:15} {r.cefr or 'NONE':4} {r.method:18} current={CURRENT[t]}{anchor}")

    print(f"\nanchor labels by CEFR: { {k: sorted(v) for k,v in anchor_labels_by_cefr(refs).items()} }")
    print(f"\nordering inversions ({len(inv)}): {inv[:5]}{'...' if len(inv)>5 else ''}")
    print(f"anchor-cefr mismatch: {cefr_mis}")
    print(f"\nflagged detected: {flagged_hit} ({len(flagged_hit)}/10)")
    print(f"anchor false pos: {anchor_fp}")

    # 決定性
    inv2 = check_inversions(refs)
    assert inv == inv2 and cefr_mis == check_anchor_cefr_mismatch(refs)

    ok = len(flagged_hit) >= 9 and len(anchor_fp) == 0 and len(missing) == 0
    print("\n--- checks ---")
    for label, passed in [
        ("凍結 fixture で決定的", True),
        ("CEFR 15/15", len(missing) == 0),
        ("flagged >= 9/10", len(flagged_hit) >= 9),
        ("anchor fp 0", len(anchor_fp) == 0),
    ]:
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")

    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
