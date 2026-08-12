#!/usr/bin/env python3
"""Verify that each vocabulary entry's term appears on its cited primary source page."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "source_index.json"
VOCAB_DIR = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"


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
    if not match:
        raise ValueError(f"No front matter: {path}")
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
    }


def fetch_text(url: str) -> str | None:
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "45", "-A", "Mozilla/5.0", url],
        capture_output=True,
        check=False,
    )
    if not result.stdout:
        return None
    import html as html_lib

    raw = result.stdout.decode("utf-8", "ignore")
    if url.endswith(".pdf"):
        try:
            import io
            import pypdf

            reader = pypdf.PdfReader(io.BytesIO(result.stdout))
            return " ".join((p.extract_text() or "") for p in reader.pages).lower()
        except Exception:
            return None
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html_lib.unescape(text).lower()


def main() -> int:
    index: dict[str, str] = {}
    if INDEX_PATH.exists():
        for page in json.loads(INDEX_PATH.read_text(encoding="utf-8")):
            index[page["url"]] = page["text"]

    failures: list[tuple[str, str, str, str]] = []
    checked = 0

    for path in sorted(VOCAB_DIR.glob("*.md")):
        entry = parse_entry(path)
        url = entry["url"]
        term = entry["term"]
        text = index.get(url)
        if text is None:
            text = fetch_text(url)
            if text:
                index[url] = text

        checked += 1
        if not text or not term_in_text(term, text):
            failures.append((entry["id"], term, entry["scene"], url))

    print(f"Checked {checked} entries; {len(failures)} failures")
    for row in failures:
        print("\t".join(row))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
