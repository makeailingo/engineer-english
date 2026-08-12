#!/usr/bin/env python3
"""Reassign vocabulary source URLs to pages where the term actually appears."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "source_index.json"
VOCAB_DIR = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"
REPORT_PATH = Path(__file__).resolve().parent / "source_fix_report.json"

# Scene preference order when scoring candidate pages.
SCENE_SOURCE_PRIORITY: dict[str, list[str]] = {
    "Career / Interview": [
        "www.amazon.jobs",
        "google.github.io",
        "developers.google.com",
        "sre.google",
        "developer.mozilla.org",
    ],
    "Implementation / Review": [
        "google.github.io",
        "developer.mozilla.org",
        "developers.google.com",
        "sre.google",
        "www.amazon.jobs",
    ],
    "Meetings / Events": [
        "google.github.io",
        "sre.google",
        "developer.mozilla.org",
        "developers.google.com",
        "www.amazon.jobs",
    ],
    "Design / Architecture": [
        "sre.google",
        "static.googleusercontent.com",
        "developer.mozilla.org",
        "google.github.io",
        "www.amazon.jobs",
    ],
    "Incident Response": [
        "sre.google",
        "google.github.io",
        "developer.mozilla.org",
        "developers.google.com",
    ],
    "Technical Writing": [
        "developers.google.com",
        "google.github.io",
        "developer.mozilla.org",
        "sre.google",
    ],
    "Management": [
        "sre.google",
        "google.github.io",
        "developers.google.com",
        "developer.mozilla.org",
    ],
}

SCENE_CONTEXT: dict[str, str] = {
    "Career / Interview": "技術面接の準備と評価の文脈。",
    "Implementation / Review": "コードの実装とレビューの文脈。",
    "Meetings / Events": "チーム内の打合せと調整の文脈。",
    "Design / Architecture": "システム設計と運用判断の文脈。",
    "Incident Response": "障害検知から復旧までの文脈。",
    "Technical Writing": "技術文書の作成と編集の文脈。",
    "Management": "チーム運営と意思決定の文脈。",
}


def stems(word: str) -> set[str]:
    out = {word.lower()}
    for suffix in ("ings", "ing", "ions", "ion", "edly", "ed", "es", "s", "e", "y", "al", "ly"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            out.add(word[: len(word) - len(suffix)])
    return out


def term_in_text(term: str, text: str) -> bool:
    for word in re.split(r"[\s\-/]+", term.lower()):
        if not word:
            continue
        if not any(st in text for st in stems(word)):
            return False
    return True


def domain(url: str) -> str:
    match = re.search(r"https?://([^/]+)", url)
    return match.group(1) if match else ""


def score_page(scene: str, page: dict) -> int:
    score = 0
    priorities = SCENE_SOURCE_PRIORITY.get(scene, [])
    dom = domain(page["url"])
    if dom in priorities:
        score += (len(priorities) - priorities.index(dom)) * 10
    hints = page.get("scene_hints") or []
    if scene in hints:
        score += 25
    # Prefer HTML over PDF for maintainability.
    if page["url"].endswith(".pdf"):
        score -= 3
    return score


def pick_source(term: str, scene: str, pages: list[dict]) -> dict | None:
    candidates = [p for p in pages if term_in_text(term, p["text"])]
    if not candidates:
        return None
    candidates.sort(key=lambda p: score_page(scene, p), reverse=True)
    return candidates[0]


def parse_entry(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.S)
    fm = match.group(1)

    def field(name: str) -> str:
        m = re.search(rf'^\s*{name}:\s*"?([^"\n]+)"?\s*$', fm, re.M)
        return m.group(1).strip() if m else ""

    return {
        "path": path,
        "content": content,
        "id": field("id"),
        "term": field("term"),
        "scene": field("scene"),
        "url": field("url"),
        "title": field("title"),
        "license": field("license"),
        "context": field("context"),
    }


def replace_source_block(content: str, page: dict, scene: str) -> str:
    context = SCENE_CONTEXT.get(scene, "ソフトウェア開発の文脈。")
    # Escape double quotes in title for YAML.
    title = page["title"].replace('"', '\\"')
    block = (
        f"source:\n"
        f'  title: "{title}"\n'
        f'  url: "{page["url"]}"\n'
        f'  license: "{page["license"]}"\n'
        f'  context: "{context}"'
    )
    return re.sub(
        r"source:\n(?:  .+\n)+",
        block + "\n",
        content,
        count=1,
    )


def fix_zero_width_and_meaning(content: str) -> str:
    content = content.replace("\u200b", "")
    content = re.sub(r"area of ​​influence", "area of influence", content)
    content = re.sub(
        r'meaning: "Tolerable failure amount frame, error budget"',
        'meaning: "Allowable failure margin, error budget"',
        content,
    )
    return content


def main() -> int:
    if not INDEX_PATH.exists():
        print("Run build_source_index.py first", file=sys.stderr)
        return 1

    pages = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    report: list[dict] = []
    fixed = 0
    unresolved: list[dict] = []

    for path in sorted(VOCAB_DIR.glob("*.md")):
        entry = parse_entry(path)
        term = entry["term"]
        scene = entry["scene"]
        current_url = entry["url"]
        current_page = next((p for p in pages if p["url"] == current_url), None)
        needs_fix = current_page is None or not term_in_text(term, current_page["text"])

        content = fix_zero_width_and_meaning(entry["content"])
        changed = content != entry["content"]

        if needs_fix:
            new_page = pick_source(term, scene, pages)
            if new_page:
                content = replace_source_block(content, new_page, scene)
                changed = True
                report.append(
                    {
                        "id": entry["id"],
                        "term": term,
                        "scene": scene,
                        "old_url": current_url,
                        "new_url": new_page["url"],
                    }
                )
                fixed += 1
            else:
                unresolved.append({"id": entry["id"], "term": term, "scene": scene, "url": current_url})

        if changed:
            path.write_text(content, encoding="utf-8")

    REPORT_PATH.write_text(json.dumps({"fixed": report, "unresolved": unresolved}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fixed sources for {fixed} entries")
    print(f"Unresolved: {len(unresolved)}")
    for item in unresolved[:30]:
        print(f"  {item['id']} {item['term']} ({item['scene']})")
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
