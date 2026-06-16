#!/usr/bin/env python3
"""Capture Sam Altman's Startup Playbook as chapter Markdown files.

The script fetches the public single-page playbook, splits it at the page's
chapter anchors, and writes processed Markdown files into the yc-partner
resource tree. It intentionally does not persist raw HTML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import textwrap
import unicodedata
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://playbook.samaltman.com/"
DEFAULT_OUTPUT_DIR = (
    ROOT_DIR / "skills" / "yc-partner" / "resources" / "yc-partners" / "startup-playbook"
)

CHAPTERS: list[tuple[str, str]] = [
    ("introduction", "Introduction"),
    ("idea", "Part I: The Idea"),
    ("team", "Part II: A Great Team"),
    ("product", "Part III: A Great Product"),
    ("execution", "Part IV: Great Execution"),
    ("growth", "Part IV: Execution - Growth"),
    ("focus", "Part IV: Execution - Focus & Intensity"),
    ("ceo", "Part IV: Execution - Jobs of the CEO"),
    ("hiring", "Part IV: Execution - Hiring & Managing"),
    ("competition", "Part IV: Execution - Competitors"),
    ("money", "Part IV: Execution - Making Money"),
    ("fundraising", "Part IV: Execution - Fundraising"),
    ("closing", "Closing Thought"),
]

INTRO_KEY = CHAPTERS[0][0]
CHAPTER_TITLES = dict(CHAPTERS)
CHAPTER_ORDER = {key: index for index, (key, _title) in enumerate(CHAPTERS)}

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

SKIP_TAGS = {"script", "style", "svg", "noscript"}
SKIP_IDS = {"toc", "voxsnap-player"}
SKIP_CLASSES = {
    "apple",
    "apple-shadow",
    "apple-spin",
    "bg",
    "bg-ceo",
    "bg-closing",
    "bg-competition",
    "bg-execution",
    "bg-focus",
    "bg-fundraising",
    "bg-growth",
    "bg-hiring",
    "bg-idea",
    "bg-inside",
    "bg-money",
    "bg-product",
    "bg-team",
    "bottom-toc",
    "fa",
    "icon",
    "mobile-wrapper",
    "mouth",
    "social-fb",
    "social-link",
    "social-twitter",
    "top",
    "toc",
    "toc-arrow",
}

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "button",
    "dd",
    "details",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "footer",
    "form",
    "header",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}

INLINE_MARKERS = {
    "strong": "**",
    "b": "**",
    "em": "*",
    "i": "*",
    "code": "`",
}


@dataclass
class Section:
    key: str
    title: str
    lines: list[str] = field(default_factory=list)
    current: list[str] = field(default_factory=list)
    current_prefix: str = ""

    def append(self, value: str) -> None:
        self.current.append(value)

    def flush(self) -> None:
        text = normalize_inline("".join(self.current))
        self.current = []
        if not text:
            self.current_prefix = ""
            return

        line = self.current_prefix + text
        if self.lines and self.lines[-1] != "":
            self.lines.append("")
        self.lines.append(line)
        self.current_prefix = ""

    @property
    def markdown(self) -> str:
        self.flush()
        return "\n".join(dedupe_adjacent_blank_lines(self.lines)).strip()


class StartupPlaybookParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.in_body = False
        self.skip_depth = 0
        self.list_stack: list[str] = []
        self.link_stack: list[tuple[str, list[str]]] = []
        self.sections: dict[str, Section] = {
            key: Section(key=key, title=title) for key, title in CHAPTERS
        }
        self.current_key = INTRO_KEY

    @property
    def current(self) -> Section:
        return self.sections[self.current_key]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}

        if tag == "body":
            self.in_body = True
            return

        if not self.in_body:
            return

        anchor_id = attrs_by_name.get("id")
        if anchor_id in CHAPTER_TITLES and anchor_id != INTRO_KEY:
            self.current.flush()
            self.current_key = anchor_id
            return

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return

        if tag in SKIP_TAGS or self.should_skip(attrs_by_name):
            if tag not in VOID_TAGS:
                self.skip_depth = 1
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.current.flush()
            level = min(int(tag[1]) + 1, 6)
            self.current.current_prefix = "#" * level + " "
        elif tag == "li":
            self.current.flush()
            indent = "  " * max(len(self.list_stack) - 1, 0)
            self.current.current_prefix = f"{indent}- "
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
        elif tag == "br":
            self.append_text("\n")
        elif tag == "a":
            self.link_stack.append((attrs_by_name.get("href", ""), []))
        elif tag in INLINE_MARKERS:
            self.append_text(INLINE_MARKERS[tag])
        elif tag in BLOCK_TAGS:
            self.current.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag == "body":
            self.current.flush()
            self.in_body = False
            return

        if not self.in_body:
            return

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth = max(0, self.skip_depth - 1)
            return

        if tag == "a" and self.link_stack:
            href, parts = self.link_stack.pop()
            text = normalize_inline("".join(parts))
            if not text:
                return
            if href.startswith("#"):
                self.append_text(text)
            else:
                self.append_text(f"[{text}]({urljoin(self.base_url, href)})")
            return

        if tag in INLINE_MARKERS:
            self.append_text(INLINE_MARKERS[tag])
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6", "li", "p"}:
            self.current.flush()
        elif tag in {"ul", "ol"}:
            self.current.flush()
            if self.list_stack:
                self.list_stack.pop()
        elif tag in BLOCK_TAGS:
            self.current.flush()

    def handle_data(self, data: str) -> None:
        if not self.in_body or self.skip_depth:
            return
        text = normalize_text(unescape(data))
        if text:
            self.append_text(text)

    def append_text(self, text: str) -> None:
        target = self.link_stack[-1][1] if self.link_stack else self.current.current
        if target and not target[-1].endswith(("\n", " ", "`", "*")):
            previous = target[-1][-1]
            if previous not in "([/" and text[0] not in ".,:;!?)]`*":
                target.append(" ")
        target.append(text)

    @staticmethod
    def should_skip(attrs_by_name: dict[str, str]) -> bool:
        element_id = attrs_by_name.get("id")
        if element_id in SKIP_IDS:
            return True
        class_names = set(attrs_by_name.get("class", "").split())
        return bool(class_names & SKIP_CLASSES)


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return normalize_inline(" ".join(self.title_parts)) or "Startup Playbook"


def main() -> int:
    args = parse_args()
    captured_on = dt.datetime.now(dt.timezone.utc).date()
    html = fetch(args.url)
    source_title = parse_title(html)
    parser = StartupPlaybookParser(args.url)
    parser.feed(html)
    parser.current.flush()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for key, title in CHAPTERS:
        section = parser.sections[key]
        if args.skip_empty and not section.markdown:
            continue
        output_path = args.output_dir / output_name(key, title)
        output_path.write_text(
            render_markdown(
                section=section,
                source_title=source_title,
                base_url=args.url,
                captured_on=captured_on,
            ),
            encoding="utf-8",
        )
        print(output_path.relative_to(ROOT_DIR))

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_URL,
        help=f"Startup Playbook URL to capture. Defaults to {DEFAULT_URL}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated Markdown chapter files.",
    )
    parser.add_argument(
        "--skip-empty",
        action="store_true",
        help="Skip configured chapters if no body text is extracted.",
    )
    return parser.parse_args()


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "yc-trans-capture/1.0 (+local research)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def parse_title(html: str) -> str:
    parser = TitleParser()
    parser.feed(html)
    return parser.title


def render_markdown(
    section: Section, source_title: str, base_url: str, captured_on: dt.date
) -> str:
    canonical_base_url = base_url.rstrip("/") + "/"
    full_url = (
        canonical_base_url
        if section.key == INTRO_KEY
        else f"{canonical_base_url}#{section.key}"
    )
    body = section.markdown or "_No body text extracted._"
    return f"""# {section.title}

- Type: Startup Playbook chapter
- Status: YC-affiliated public essay
- URL: {full_url}
- Author: Sam Altman
- Published: Unknown
- Captured: {captured_on.isoformat()}
- Method: `scripts/capture_startup_playbook.py`
- Caveat: references/caveats/yc-founder-partner-source.md

## Summary

- Source page title: {source_title}.
- Split from the public single-page Startup Playbook by page anchors.
- Navigation, table of contents, illustrations, scripts, and site chrome were omitted.
- Body text was normalized into Markdown.

## Essay Text

{body}
"""


def output_name(key: str, title: str) -> str:
    index = CHAPTER_ORDER[key]
    return f"{index:02d}-{slugify(title)}.md"


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def normalize_text(value: str) -> str:
    replacements = {
        "\u00a0": " ",
        "\u00b7": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": " - ",
        "\u2026": "...",
    }
    for source, replacement in replacements.items():
        value = value.replace(source, replacement)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[ \t\r\n]+", " ", value)
    return value.strip()


def normalize_inline(value: str) -> str:
    value = normalize_text(value)
    value = value.replace("** **", " ").replace("* *", " ")
    value = re.sub(r"\s+([.,:;!?)])", r"\1", value)
    value = re.sub(r"([(])\s+", r"\1", value)
    return value.strip()


def dedupe_adjacent_blank_lines(lines: list[str]) -> list[str]:
    output: list[str] = []
    for line in lines:
        if not line and output and not output[-1]:
            continue
        output.append(wrap_line(line))
    while output and not output[-1]:
        output.pop()
    return output


def wrap_line(line: str) -> str:
    if not line or line.startswith("#") or line.startswith("- ") or line.startswith("  - "):
        return line
    return textwrap.fill(line, width=100)


if __name__ == "__main__":
    sys.exit(main())
