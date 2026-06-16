#!/usr/bin/env python3
"""Convert locally captured Paul Graham essay HTML into processed Markdown."""

from __future__ import annotations

import argparse
from datetime import date
import html
import re
import textwrap
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

SOURCE_META = {
    "paul-graham-ace.html": ("Billionaires Build", "https://www.paulgraham.com/ace.html"),
    "paul-graham-default-alive-or-dead.html": (
        "Default Alive or Default Dead?",
        "https://www.paulgraham.com/aord.html",
    ),
    "paul-graham-do-things-that-dont-scale.html": (
        "Do Things that Don't Scale",
        "https://www.paulgraham.com/ds.html",
    ),
    "paul-graham-growth.html": ("Startup = Growth", "https://www.paulgraham.com/growth.html"),
    "paul-graham-startup-ideas.html": (
        "How to Get Startup Ideas",
        "https://www.paulgraham.com/startupideas.html",
    ),
}

PUBLISHED_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$"
)


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for source in args.sources:
        title, url = SOURCE_META.get(source.name, extract_title_and_url(source))
        text, published = extract_essay_text(source)
        output = args.output_dir / f"{slugify(title)}.md"
        output.write_text(build_markdown(title, url, published, text, source), encoding="utf-8")
        print(f"Wrote {output.relative_to(ROOT_DIR)}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT_DIR / "skills" / "yc-partner" / "resources" / "pg-essays",
    )
    return parser.parse_args()


def extract_title_and_url(path: Path) -> tuple[str, str]:
    raw = path.read_bytes().decode("windows-1252", errors="replace")
    title_match = re.search(r"<title>(.*?)</title>", raw, flags=re.IGNORECASE | re.DOTALL)
    title = normalize_text(title_match.group(1)) if title_match else path.stem
    url = f"https://www.paulgraham.com/{path.stem.removeprefix('paul-graham-')}.html"
    return title, url


def extract_essay_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes().decode("windows-1252", errors="replace")
    raw = re.sub(r"<script\b.*?</script>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    raw = re.sub(r"<style\b.*?</style>", "", raw, flags=re.IGNORECASE | re.DOTALL)

    body_start_match = re.search(r'<font size="2" face="verdana">', raw, flags=re.IGNORECASE)
    if not body_start_match:
        raise RuntimeError(f"Could not find essay body in {path}")

    body = raw[body_start_match.end() :]
    body = re.split(r"</font></td></tr></table><br\s*/?><table|</font></td></tr></table></td></tr></table>|</body>|<script", body, maxsplit=1, flags=re.IGNORECASE | re.DOTALL)[0]
    body = re.sub(r"<table width=100%.*?</table>\s*<p>\s*", "", body, count=1, flags=re.IGNORECASE | re.DOTALL)
    body = re.sub(
        r"<b>(.*?)</b>\s*<br\s*/?>\s*<br\s*/?>",
        lambda match: f"\n\n## {strip_tags(match.group(1))}\n\n",
        body,
        flags=re.IGNORECASE | re.DOTALL,
    )
    body = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n\n", body, flags=re.IGNORECASE)
    body = re.sub(r"<p\s*/?>", "\n\n", body, flags=re.IGNORECASE)
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.IGNORECASE)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    body = normalize_text(body)

    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", body) if paragraph.strip()]
    published = "Unknown"
    if paragraphs and PUBLISHED_RE.match(paragraphs[0]):
        published = paragraphs.pop(0)

    wrapped = []
    for paragraph in paragraphs:
        if paragraph.startswith("## "):
            wrapped.append(paragraph)
        else:
            wrapped.append(textwrap.fill(paragraph, width=100))
    return "\n\n".join(wrapped), published


def strip_tags(value: str) -> str:
    return normalize_text(re.sub(r"<[^>]+>", "", html.unescape(value)))


def normalize_text(value: str) -> str:
    replacements = {
        "\u00a0": " ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\ufffd": "-",
    }
    for source, replacement in replacements.items():
        value = value.replace(source, replacement)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def build_markdown(title: str, url: str, published: str, text: str, source: Path) -> str:
    source_name = source.name
    captured = date.today().isoformat()
    return f"""# {title}

- Type: Paul Graham essay
- Status: YC-affiliated public essay
- URL: {url}
- Author: Paul Graham
- Published: {published}
- Captured: {captured}
- Method: `scripts/convert_pg_html_to_markdown.py`
- Caveat: references/caveats/yc-founder-partner-source.md

## Summary

- Converted from local HTML capture `{source_name}`.
- Navigation, scripts, images, translation links, and site chrome were omitted.
- Body text was normalized into Markdown.

## Essay Text

{text}
"""


def slugify(value: str) -> str:
    value = value.lower().replace("=", "equals")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


if __name__ == "__main__":
    raise SystemExit(main())
