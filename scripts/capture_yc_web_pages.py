#!/usr/bin/env python3
"""Capture official YC web pages as Markdown assets.

The generated files are source captures for local review work. The script keeps
the capture metadata with each Markdown file and writes outputs outside scripts/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "skills" / "yc-partner" / "resources" / "yc-website"

DEFAULT_PAGES = [
    "https://www.ycombinator.com/apply",
    "https://www.ycombinator.com/faq",
    "https://www.ycombinator.com/video",
    "https://www.ycombinator.com/whynot",
]

TITLE_OVERRIDES = {
    "/apply": "Apply to YC",
    "/faq": "YC Frequently Asked Questions",
    "/video": "The Application Video",
    "/whynot": "Why Didn't My Group Get an Interview?",
}

TYPE_OVERRIDES = {
    "/apply": "Official YC application page",
    "/faq": "Official YC FAQ",
    "/video": "Official YC application video guide",
    "/whynot": "Official YC application feedback note",
}

SLUG_OVERRIDES = {
    "/apply": "apply-to-y-combinator.md",
    "/faq": "frequently-asked-questions.md",
    "/video": "application-video.md",
    "/whynot": "why-didnt-my-group-get-an-interview.md",
}

CONTENT_OVERRIDES = {
    "/video": """## The Application Video

### Instructions

- In the video please introduce yourselves, explain what you are doing and why, and tell us anything else you want to about the founders or the project.
- The video should be 1 minute long and should contain nothing except the founders talking.
- This is not the place to submit a demo or promotional video. If you have a demo for your product, there is a separate place in the application for that. For this video, YC wants to hear how the founders communicate.
- If there is more than one founder, all founders should appear in the video. If they cannot be in the same room at the same time, screen record a video call instead.
- Do not recite a written script. Use bullet points instead and talk spontaneously as you would to a friend. Reading a written script does not help the application or convey communication skills.

### Successful YC Application Video Examples

- Campus Job (YC W15)
- Flip (YC W15)
- Zenefits (YC W13)
- Teespring (YC W13)

### YC Summary

- 1 minute video
- Only founders talking
- With all founders
- No script: just bullet points""",
    "/whynot": """## Why Didn't My Group Get an Interview?

A lot of groups that do not get invited to interviews want to know why, because they want to know whether something was wrong with the project.

YC's explanation is that often there is no single reason. The median application is usually pretty good. A rejection often does not mean the application is particularly bad; it may mean enough other applications seemed particularly good.

Applying to YC is not like taking a test with a grade. YC has physical limits on how many teams each YC Partner can work with during a batch. YC interviews enough great teams to find that number of companies and then generally stops, even though many good teams applied.

For many rejected teams near the cutoff, the reason is not found inside their application. They were pushed below the cutoff by stronger applications above them.

YC does not respond with application feedback because, much of the time, there is no specific answer to give without making one up.""",
}

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


@dataclass(frozen=True)
class Page:
    url: str
    source_title: str
    title: str
    source_type: str
    output_name: str
    content: str


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []
        self.canonical_url: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value for name, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "link" and attrs_by_name.get("rel") == "canonical":
            self.canonical_url = attrs_by_name.get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return normalize_space(" ".join(self.title_parts))


class MainMarkdownParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.in_main = False
        self.main_depth = 0
        self.skip_depth = 0
        self.lines: list[str] = []
        self.current: list[str] = []
        self.current_prefix = ""
        self.list_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return

        if tag == "main" and not self.in_main:
            self.in_main = True
            self.main_depth = 1
            return

        if not self.in_main:
            return

        if tag not in VOID_TAGS:
            self.main_depth += 1

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()
            level = min(int(tag[1]) + 1, 6)
            self.current_prefix = "#" * level + " "
        elif tag == "button":
            self.flush()
            self.current_prefix = "### "
        elif tag == "li":
            self.flush()
            indent = "  " * max(len(self.list_stack) - 1, 0)
            self.current_prefix = f"{indent}- "
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
        elif tag == "br":
            self.current.append("\n")
        elif tag in BLOCK_TAGS:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        if not self.in_main:
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "button", "li", "p"}:
            self.flush()
        elif tag in {"ul", "ol"}:
            self.flush()
            if self.list_stack:
                self.list_stack.pop()
        elif tag in BLOCK_TAGS:
            self.flush()

        if tag != "main" and tag not in VOID_TAGS:
            self.main_depth = max(0, self.main_depth - 1)
        elif tag == "main":
            self.flush()
            self.in_main = False
            self.main_depth = 0

    def handle_data(self, data: str) -> None:
        if not self.in_main or self.skip_depth:
            return
        text = normalize_space(unescape(data))
        if not text:
            return

        if self.current and not self.current[-1].endswith(("\n", " ")):
            previous = self.current[-1][-1]
            if previous not in "([/" and text[0] not in ".,:;!?)]":
                self.current.append(" ")
        self.current.append(text)

    def flush(self) -> None:
        text = normalize_space("".join(self.current))
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
        return "\n".join(dedupe_adjacent(self.lines)).strip()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def dedupe_adjacent(lines: Iterable[str]) -> list[str]:
    output: list[str] = []
    previous_text = None
    for line in lines:
        key = line.strip()
        if key and key == previous_text:
            continue
        output.append(line)
        if key:
            previous_text = key
    return output


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return f"{slug or 'yc-page'}.md"


def ensure_official_yc_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "www.ycombinator.com":
        raise ValueError(f"Refusing non-official YC page: {url}")


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


def parse_page(url: str, html: str) -> Page:
    metadata = TitleParser()
    metadata.feed(html)

    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    source_title = metadata.title or TITLE_OVERRIDES.get(path, path)
    title = TITLE_OVERRIDES.get(path) or source_title.replace("| Y Combinator", "").strip()
    source_type = TYPE_OVERRIDES.get(path, "Official YC page")
    output_name = SLUG_OVERRIDES.get(path) or slugify(title)
    canonical_url = urljoin(url, metadata.canonical_url) if metadata.canonical_url else url

    content_parser = MainMarkdownParser(canonical_url)
    content_parser.feed(html)
    content = content_parser.markdown
    if not content and path in CONTENT_OVERRIDES:
        content = CONTENT_OVERRIDES[path]

    return Page(
        url=canonical_url,
        source_title=source_title,
        title=title,
        source_type=source_type,
        output_name=output_name,
        content=content,
    )


def render_markdown(page: Page, captured_on: dt.date) -> str:
    return "\n".join(
        [
            f"# {page.title}",
            "",
            f"- Type: {page.source_type}",
            "- Status: Official YC source",
            f"- URL: {page.url}",
            "- Author: Y Combinator",
            "- Published: Unknown",
            f"- Captured: {captured_on.isoformat()}",
            "- Method: `scripts/capture_yc_web_pages.py`",
            "- Caveat: references/caveats/official-yc-source.md",
            "",
            "## Summary",
            "",
            f"- Official YC page capture. Source page title: {page.source_title}.",
            "",
            "## Page Text",
            "",
            page.content or "_No main page content extracted._",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="*", default=DEFAULT_PAGES)
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        type=Path,
        help="Directory for generated Markdown files.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    captured_on = dt.datetime.now(dt.timezone.utc).date()

    for url in args.urls:
        ensure_official_yc_url(url)
        page = parse_page(url, fetch(url))
        output_path = output_dir / page.output_name
        output_path.write_text(render_markdown(page, captured_on), encoding="utf-8")
        print(output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
