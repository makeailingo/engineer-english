#!/usr/bin/env python3
"""
POC: TOEIC 3ソース照合（100語）

ソース:
  1. toeic-words.com     … 600 / 730-800 / 800+  （Web公開リスト）
  2. かんたんTOEIC       … 600 / 730 / 860       （品詞別ページ）
  3. TSL 1.2 stats       … 公式 CC BY-SA CSV（えいたんご相当・再現可能）

※ えいたんごクイズはページが CSR のため静的取得不可（10語のみ）。
   同一系統の NGSL/TSL 公式データをソース3として使用。
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

POC_DIR = Path(__file__).parent
FIXTURE = POC_DIR / "poc_toeic_fixture.json"
UA = "EngineerEnglish-TOEIC-POC/1.0"

# Engineer English Difficulty マスタとの対応（vocabulary-markdown 準拠）
TOEIC_TO_DIFFICULTY = {
    "600": "Beginner",
    "730": "Intermediate",
    "730-800": "Intermediate",
    "800+": "Advanced",
    "860": "Advanced",
    "990": "Advanced",
}

DIFF_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

FLAGGED = [
    "critique", "replace", "reproduce", "isolate", "assertion",
    "coverage", "availability", "reliability", "capacity", "ownership",
]
ANCHORS = {
    "feedback": "Beginner", "clarify": "Intermediate", "courteous": "Advanced",
    "scrutiny": "Advanced", "trade-off": "Intermediate",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def load_vocab_terms() -> dict[str, str]:
    terms: dict[str, str] = {}
    for path in sorted((POC_DIR.parents[1] / "docs" / "vocabulary").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        term = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', text, re.M)
        diff = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if term and diff:
            terms[term.group(1).strip()] = diff.group(1).strip()
    return terms


def parse_toeic_words() -> dict[str, str]:
    html = fetch("https://www.toeic-words.com/words")
    rank_order = [
        ("section-important", "600"),
        ("section-medium", "730-800"),
        ("section-high", "800+"),
    ]
    out: dict[str, str] = {}
    for sec_id, rank in rank_order:
        m = re.search(rf'id="{sec_id}"[^>]*>(.*?)(?=id="section-|$)', html, re.S)
        if not m:
            continue
        for word in re.findall(r"/words/([a-z0-9-]+)", m.group(1)):
            out.setdefault(word, rank)
    return out


def parse_tsl() -> dict[str, str]:
    """TSL 1.2 頻度 rank → TOEIC band（公式 CSV、凍結可能）"""
    csv_text = fetch("https://www.newgeneralservicelist.com/s/TSL_12_stats.csv")
    out: dict[str, str] = {}
    for line in csv_text.splitlines()[1:]:
        parts = line.split(",")
        if len(parts) < 2:
            continue
        word = parts[0].strip().lower()
        try:
            rank = int(parts[1])
        except ValueError:
            continue
        if rank <= 400:
            band = "600"
        elif rank <= 800:
            band = "730"
        else:
            band = "860"
        out[word] = band
    return out


def parse_kantantoeic() -> dict[str, str]:
    pages = []
    for band in ["600", "730", "860"]:
        for pos in ["verb", "noun", "adjective"]:
            pages.append((band, f"https://kantantoeic.u-ff.com/toeic-vocabulary-{pos}-{band}/"))
    out: dict[str, str] = {}
    for band, url in pages:
        try:
            html = fetch(url)
        except Exception:
            continue
        for row in re.findall(r"<tr>\s*<td>([a-z][a-z-]*)</td>", html, re.I):
            out.setdefault(row.lower(), band)
        time.sleep(0.2)
    return out


def toeic_band_to_difficulty(band: str | None) -> str | None:
    if not band:
        return None
    return TOEIC_TO_DIFFICULTY.get(band)


@dataclass
class TermResult:
    term: str
    current: str
    toeic_words: str | None
    kantantoeic: str | None
    tsl: str | None
    sources_hit: int
    difficulty_votes: dict[str, int]
    adopted_toeic: str | None
    adopted_difficulty: str | None
    consensus: bool


def build_results(terms: dict[str, str], sources: dict[str, dict[str, str]]) -> list[TermResult]:
    results = []
    for term, current in sorted(terms.items()):
        key = term.lower().replace(" ", "-")
        tw = sources["toeic_words"].get(key)
        tsl = sources["tsl"].get(key)
        ka = sources["kantantoeic"].get(key)
        diffs = [d for d in (toeic_band_to_difficulty(tw),
                             toeic_band_to_difficulty(tsl),
                             toeic_band_to_difficulty(ka)) if d]
        votes = Counter(diffs)
        adopted_diff = votes.most_common(1)[0][0] if votes else None
        bands = [x for x in (tw, tsl, ka) if x]
        adopted_toeic = Counter(bands).most_common(1)[0][0] if bands else None
        consensus = len(votes) == 1 and len(bands) >= 2
        results.append(TermResult(
            term=term, current=current,
            toeic_words=tw, tsl=tsl, kantantoeic=ka,
            sources_hit=len(bands),
            difficulty_votes=dict(votes),
            adopted_toeic=adopted_toeic,
            adopted_difficulty=adopted_diff,
            consensus=consensus,
        ))
    return results


def main() -> int:
    print("=== TOEIC 3ソース POC ===\n")
    terms = load_vocab_terms()

    if FIXTURE.exists() and "--refresh" not in sys.argv:
        data = json.loads(FIXTURE.read_text())
        sources = data["sources"]
        print(f"Loaded fixture: {FIXTURE}\n")
    else:
        print("Fetching 3 sources...")
        sources = {
            "toeic_words": parse_toeic_words(),
            "kantantoeic": parse_kantantoeic(),
            "tsl": parse_tsl(),
        }
        FIXTURE.write_text(json.dumps({
            "sources_meta": {
                "toeic_words": "https://www.toeic-words.com/words",
                "kantantoeic": "https://kantantoeic.u-ff.com/toeic-vocabulary-{pos}-{600,730,860}/",
                "tsl": "https://www.newgeneralservicelist.com/s/TSL_12_stats.csv",
                "note": "eitanquiz.com は CSR のため静的取得不可。TSL 公式 CSV を代替。",
            },
            "sources": sources,
        }, ensure_ascii=False, indent=2) + "\n")
        print(f"Wrote {FIXTURE}\n")

    results = build_results(terms, sources)

    # --- 統計 ---
    n = len(results)
    cov = {1: 0, 2: 0, 3: 0, 0: 0}
    for r in results:
        cov[r.sources_hit] += 1

    print("## カバー率")
    print(f"  0ソース: {cov[0]}/{n}")
    print(f"  1ソース: {cov[1]}/{n}")
    print(f"  2ソース: {cov[2]}/{n}")
    print(f"  3ソース: {cov[3]}/{n}")
    print(f"  1ソース以上: {n - cov[0]}/{n} ({100*(n-cov[0])//n}%)")

    with_adopted = [r for r in results if r.adopted_difficulty]
    agree_current = [r for r in with_adopted if r.current == r.adopted_difficulty]
    print(f"\n## 採用 Difficulty あり: {len(with_adopted)}/{n}")
    print(f"  現行と一致: {len(agree_current)}/{len(with_adopted)}")

    consensus_n = sum(1 for r in results if r.consensus)
    print(f"  2ソース以上 & Difficulty一致（consensus）: {consensus_n}/{n}")

    # flagged / anchors
    print("\n## flagged 語（10語）")
    for t in FLAGGED:
        r = next(x for x in results if x.term == t)
        mark = "≠" if r.adopted_difficulty and r.current != r.adopted_difficulty else "="
        print(f"  {t:15} current={r.current:12} toeic→{r.adopted_difficulty or 'NONE':12} "
              f"[tw={r.toeic_words or '-':8} tsl={r.tsl or '-':4} ka={r.kantantoeic or '-':4}] {mark}")

    flagged_detected = [t for t in FLAGGED
                        if (r := next(x for x in results if x.term == t))
                        and r.adopted_difficulty and r.current != r.adopted_difficulty]
    print(f"\n  検出（現行≠TOEIC採用）: {len(flagged_detected)}/10 → {flagged_detected}")

    print("\n## anchor 語（5語）")
    anchor_fp = []
    for t, expected in ANCHORS.items():
        r = next(x for x in results if x.term == t)
        ok = r.adopted_difficulty == expected if r.adopted_difficulty else None
        if r.adopted_difficulty and r.adopted_difficulty != expected:
            anchor_fp.append(t)
        status = "OK" if ok else ("?" if ok is None else "NG")
        print(f"  {t:15} anchor={expected:12} toeic→{r.adopted_difficulty or 'NONE':12} [{status}]")

    # ソース間一致
    print("\n## ソース間 TOEIC band 一致（2ソース以上ヒット時）")
    band_agree = band_disagree = 0
    for r in results:
        bands = [b for b in (r.toeic_words, r.tsl, r.kantantoeic) if b]
        if len(bands) < 2:
            continue
        mapped = [toeic_band_to_difficulty(b) for b in bands]
        if len(set(mapped)) == 1:
            band_agree += 1
        else:
            band_disagree += 1
    print(f"  Difficulty 一致: {band_agree}")
    print(f"  Difficulty 不一致: {band_disagree}")

    # 決定性
    r2 = build_results(terms, sources)
    assert [asdict(r) for r in results] == [asdict(r) for r in r2]

    print("\n## POC 成功条件")
    checks = {
        "凍結 fixture から決定的": True,
        f"1ソース以上カバー ≥80%": (n - cov[0]) >= n * 0.8,
        f"flagged 検出 ≥7/10": len(flagged_detected) >= 7,
        f"anchor 誤判定 ≤1/5": len(anchor_fp) <= 1,
    }
    ok = True
    for label, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
        ok = ok and passed

    print(f"\n=== {'PASS' if ok else 'FAIL'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
