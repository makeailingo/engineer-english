#!/usr/bin/env python3
"""Apply curated MDN and Google Style Guide source resolutions."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

VOCAB_DIR = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"
REPORT_PATH = Path(__file__).resolve().parent / "source_fix_report.json"
MDN_RESOLVE = Path("/tmp/mdn_resolve.json")
STYLE_FOUND = Path("/tmp/style_found.json")

SCENE_CONTEXT = {
    "Career / Interview": "技術面接の準備と評価の文脈。",
    "Implementation / Review": "コードの実装とレビューの文脈。",
    "Meetings / Events": "チーム内の打合せと調整の文脈。",
    "Design / Architecture": "システム設計と運用判断の文脈。",
    "Incident Response": "障害検知から復旧までの文脈。",
    "Technical Writing": "技術文書の作成と編集の文脈。",
    "Management": "チーム運営と意思決定の文脈。",
}


def parse_entry(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.S)
    fm = match.group(1)

    def field(name: str) -> str:
        m = re.search(rf'^\s*{name}:\s*"?([^"\n]+)"?\s*$', fm, re.M)
        return m.group(1).strip() if m else ""

    return {"path": path, "content": content, "term": field("term"), "scene": field("scene"), "url": field("url")}


def replace_source(content: str, title: str, url: str, license_name: str, scene: str) -> str:
    context = SCENE_CONTEXT.get(scene, "ソフトウェア開発の文脈。")
    title = title.replace('"', '\\"')
    block = (
        f"source:\n"
        f'  title: "{title}"\n'
        f'  url: "{url}"\n'
        f'  license: "{license_name}"\n'
        f'  context: "{context}"'
    )
    return re.sub(r"source:\n(?:  .+\n)+", block + "\n", content, count=1)


def fetch_title(url: str) -> str:
    import html as html_lib

    body = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
    match = re.search(r"<title[^>]*>([^<]+)</title>", body, re.I)
    return html_lib.unescape(match.group(1).strip()) if match else url


def load_resolutions() -> dict[str, tuple[str, str]]:
    """term -> (url, license)"""
    out: dict[str, tuple[str, str]] = {}

    if MDN_RESOLVE.exists():
        for term, url in json.loads(MDN_RESOLVE.read_text(encoding="utf-8")).get("fixes", {}).items():
            out[term] = (url, "CC BY-SA 2.5")

    if STYLE_FOUND.exists():
        for term, url in json.loads(STYLE_FOUND.read_text(encoding="utf-8")).items():
            out[term] = (url, "CC BY 4.0")

    return out


def main() -> int:
    if not REPORT_PATH.exists():
        print("Run fix_vocabulary_sources.py first", file=sys.stderr)
        return 1

    unresolved = {item["term"] for item in json.loads(REPORT_PATH.read_text(encoding="utf-8"))["unresolved"]}
    resolutions = load_resolutions()
    applied = 0

    for path in sorted(VOCAB_DIR.glob("*.md")):
        entry = parse_entry(path)
        if entry["term"] not in unresolved:
            continue
        if entry["term"] not in resolutions:
            continue

        url, license_name = resolutions[entry["term"]]
        title = fetch_title(url)
        content = replace_source(entry["content"], title, url, license_name, entry["scene"])
        path.write_text(content, encoding="utf-8")
        applied += 1
        time.sleep(0.04)

    print(f"Applied {applied} curated resolutions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
