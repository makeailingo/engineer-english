#!/usr/bin/env python3
"""Remove vocabulary entries whose terms cannot be verified on any indexed primary source."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "source_index.json"
VOCAB_DIR = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"
REMOVED_PATH = Path(__file__).resolve().parent / "removed_vocabulary.json"


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


def parse_entry(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.S)
    fm = match.group(1)

    def field(name: str) -> str:
        m = re.search(rf'^\s*{name}:\s*"?([^"\n]+)"?\s*$', fm, re.M)
        return m.group(1).strip() if m else ""

    return {"path": path, "id": field("id"), "term": field("term"), "scene": field("scene"), "url": field("url")}


def fetch_text(url: str) -> str | None:
    import html as html_lib

    result = subprocess.run(
        ["curl", "-sL", "--max-time", "45", "-A", "Mozilla/5.0", url],
        capture_output=True,
        check=False,
    )
    if not result.stdout:
        return None
    if url.endswith(".pdf"):
        try:
            import io
            import pypdf

            reader = pypdf.PdfReader(io.BytesIO(result.stdout))
            return " ".join((p.extract_text() or "") for p in reader.pages).lower()
        except Exception:
            return None
    raw = result.stdout.decode("utf-8", "ignore")
    if "amazon.jobs" in url:
        chunks = re.findall(r'"(?:text|title|description)"\s*:\s*"([^"]{3,500})"', raw)
        return " ".join(chunks).lower()
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html_lib.unescape(text).lower()


def main() -> int:
    index: dict[str, str] = {}
    if INDEX_PATH.exists():
        for page in json.loads(INDEX_PATH.read_text(encoding="utf-8")):
            index[page["url"]] = page["text"]

    removed: list[dict] = []
    for path in sorted(VOCAB_DIR.glob("*.md")):
        entry = parse_entry(path)
        url = entry["url"]
        text = index.get(url) or fetch_text(url)
        if text:
            index[url] = text
        if text and term_in_text(entry["term"], text):
            continue
        removed.append({"id": entry["id"], "term": entry["term"], "scene": entry["scene"], "url": url, "file": path.name})
        path.unlink()

    REMOVED_PATH.write_text(json.dumps(removed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Removed {len(removed)} unverifiable entries")
    for item in removed:
        print(f"  {item['id']} {item['term']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
