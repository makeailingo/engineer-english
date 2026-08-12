#!/usr/bin/env python3
"""Build a searchable index of open-license primary sources for vocabulary verification."""

from __future__ import annotations

import html as html_lib
import io
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import pypdf
except ImportError:
    pypdf = None

INDEX_PATH = Path(__file__).resolve().parent / "source_index.json"

# Seed URLs grouped by license and typical scene affinity.
SEED_URLS: list[tuple[str, str, list[str]]] = [
    # (url, license, scene_hints)
    # Google Engineering Practices — CC BY 3.0
    ("https://google.github.io/eng-practices/", "CC BY 3.0", ["Implementation / Review", "Meetings / Events", "Management"]),
    ("https://google.github.io/eng-practices/review/developer/cl-descriptions.html", "CC BY 3.0", ["Implementation / Review", "Technical Writing"]),
    ("https://google.github.io/eng-practices/review/developer/handling-comments.html", "CC BY 3.0", ["Implementation / Review", "Meetings / Events"]),
    ("https://google.github.io/eng-practices/review/developer/small-cls.html", "CC BY 3.0", ["Implementation / Review", "Meetings / Events"]),
    ("https://google.github.io/eng-practices/review/emergencies.html", "CC BY 3.0", ["Incident Response", "Implementation / Review"]),
    ("https://google.github.io/eng-practices/review/reviewer/comments.html", "CC BY 3.0", ["Implementation / Review"]),
    ("https://google.github.io/eng-practices/review/reviewer/looking-for.html", "CC BY 3.0", ["Implementation / Review"]),
    ("https://google.github.io/eng-practices/review/reviewer/navigate.html", "CC BY 3.0", ["Implementation / Review"]),
    ("https://google.github.io/eng-practices/review/reviewer/pushback.html", "CC BY 3.0", ["Implementation / Review", "Meetings / Events"]),
    ("https://google.github.io/eng-practices/review/reviewer/speed.html", "CC BY 3.0", ["Implementation / Review"]),
    ("https://google.github.io/eng-practices/review/reviewer/standard.html", "CC BY 3.0", ["Implementation / Review", "Management"]),
    # Google SRE CC BY 4.0 materials
    ("https://sre.google/resources/practices-and-processes/art-of-slos/", "CC BY 4.0", ["Design / Architecture", "Incident Response"]),
    ("https://sre.google/classroom/distributed-pubsub/", "CC BY 4.0", ["Design / Architecture"]),
    ("https://sre.google/workbook/team-lifecycles/", "CC BY 4.0", ["Management", "Meetings / Events"]),
    ("https://sre.google/workbook/implementing-slos/", "CC BY 4.0", ["Design / Architecture", "Incident Response"]),
    ("https://sre.google/static/pdf/art-of-slos-howto-a4.pdf", "CC BY 4.0", ["Design / Architecture", "Incident Response"]),
    ("https://static.googleusercontent.com/media/sre.google/en//static/pdf/nalsd-workbook-a4.pdf", "CC BY 4.0", ["Design / Architecture"]),
    # Google Developer Documentation Style Guide — CC BY 4.0
    ("https://developers.google.com/style/tone", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/word-list", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/grammar", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/accessibility", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/code-samples", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/documenting-code", "CC BY 4.0", ["Technical Writing", "Implementation / Review"]),
    ("https://developers.google.com/style/headings", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/organizing-content", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/principles", "CC BY 4.0", ["Technical Writing"]),
    ("https://developers.google.com/style/structure", "CC BY 4.0", ["Technical Writing"]),
    # Amazon Jobs Interview Prep — usage reference (no open license)
    (
        "https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics",
        "No open license identified",
        ["Career / Interview"],
    ),
    (
        "https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep",
        "No open license identified",
        ["Career / Interview"],
    ),
    (
        "https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep",
        "No open license identified",
        ["Career / Interview", "Design / Architecture"],
    ),
    # MDN — CC BY-SA (usage verification only); include pages already cited in vocabulary
    ("https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing", "CC BY-SA 2.5", ["Implementation / Review"]),
    ("https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/deployment", "CC BY-SA 2.5", ["Design / Architecture"]),
    ("https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Soft_skills/Workflows_and_processes", "CC BY-SA 2.5", ["Meetings / Events", "Management"]),
    ("https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Design_and_accessibility/Thinking_before_coding", "CC BY-SA 2.5", ["Design / Architecture"]),
    ("https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Fundamentals", "CC BY-SA 2.5", ["Design / Architecture", "Implementation / Review"]),
    ("https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Rum-vs-Synthetic", "CC BY-SA 2.5", ["Design / Architecture"]),
    ("https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Network_resilience", "CC BY-SA 2.5", ["Design / Architecture", "Incident Response"]),
    ("https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Understanding_latency", "CC BY-SA 2.5", ["Design / Architecture"]),
    ("https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Input_validation", "CC BY-SA 2.5", ["Implementation / Review", "Design / Architecture"]),
    ("https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Debugging_JavaScript", "CC BY-SA 2.5", ["Implementation / Review"]),
]

STYLE_GUIDE_PAGES = [
    "tone", "word-list", "grammar", "accessibility", "code-samples", "documenting-code",
    "headings", "organizing-content", "principles", "structure", "writing-for-a-global-audience",
    "write-for-the-user", "presenting-information", "cross-references", "lists-and-tables",
    "ui-elements", "release-notes", "changelog", "glossary", "abbreviations",
]


@dataclass
class SourcePage:
    url: str
    title: str
    license: str
    scene_hints: list[str]
    text: str


def fetch_bytes(url: str) -> bytes:
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "45", "-A", "Mozilla/5.0", url],
        capture_output=True,
        check=False,
    )
    return result.stdout


def extract_title(html: str) -> str:
    match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    if match:
        return html_lib.unescape(match.group(1).strip())
    return ""


def html_to_text(raw: bytes) -> str:
    text = raw.decode("utf-8", "ignore")
    chunks: list[str] = []
    # Keep human-readable strings embedded in JS/JSON payloads (e.g. Amazon Jobs SPA).
    for match in re.finditer(r'"(?:text|title|description|content)"\s*:\s*"((?:\\.|[^"\\])*)"', text):
        chunks.append(match.group(1).encode("utf-8").decode("unicode_escape"))
    for match in re.finditer(r'"(?:text|title|description|content)"\s*:\s*"([^"]{3,200})"', text):
        chunks.append(match.group(1))
    visible = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    visible = re.sub(r"(?is)<style.*?>.*?</style>", " ", visible)
    visible = re.sub(r"<[^>]+>", " ", visible)
    chunks.append(html_lib.unescape(visible))
    return " ".join(chunks)


def pdf_to_text(raw: bytes) -> str:
    if pypdf is None:
        return ""
    try:
        reader = pypdf.PdfReader(io.BytesIO(raw))
        return " ".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return ""


def load_page(url: str, license_name: str, scene_hints: list[str]) -> SourcePage | None:
    raw = fetch_bytes(url)
    if not raw or len(raw) < 200:
        print(f"SKIP (empty): {url}", file=sys.stderr)
        return None

    if url.endswith(".pdf"):
        text = pdf_to_text(raw)
        title = Path(urlparse(url).path).name
    else:
        html = raw.decode("utf-8", "ignore")
        title = extract_title(html) or url
        text = html_to_text(raw)

    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 300:
        print(f"SKIP (short text {len(text)}): {url}", file=sys.stderr)
        return None

    return SourcePage(url=url, title=title, license=license_name, scene_hints=scene_hints, text=text.lower())


def discover_mdn_urls(vocab_dir: Path) -> list[str]:
    urls: set[str] = set()
    for path in vocab_dir.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r'url:\s*"(https://developer\.mozilla\.org[^"]+)"', content):
            urls.add(match.group(1))
    return sorted(urls)


def main() -> None:
    vocab_dir = Path(__file__).resolve().parents[1] / "docs" / "vocabulary"
    seen: set[str] = set()
    pages: list[SourcePage] = []

    seeds = list(SEED_URLS)
    for slug in STYLE_GUIDE_PAGES:
        url = f"https://developers.google.com/style/{slug}"
        if url not in {s[0] for s in seeds}:
            seeds.append((url, "CC BY 4.0", ["Technical Writing"]))

    for url in discover_mdn_urls(vocab_dir):
        if url not in {s[0] for s in seeds}:
            seeds.append((url, "CC BY-SA 2.5", ["Implementation / Review", "Design / Architecture"]))

    for url, license_name, hints in seeds:
        if url in seen:
            continue
        seen.add(url)
        print(f"Fetching {url}...", file=sys.stderr)
        page = load_page(url, license_name, hints)
        if page:
            pages.append(page)

    payload = [asdict(p) for p in pages]
    INDEX_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(pages)} pages to {INDEX_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
