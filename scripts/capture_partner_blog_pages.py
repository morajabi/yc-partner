#!/usr/bin/env python3
"""Capture YC-affiliated partner blog posts as processed Markdown.

The script fetches public article pages, extracts the article body, and writes
compact Markdown resources. It does not persist raw HTML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "skills" / "yc-partner" / "resources" / "yc-partners"

DEFAULT_URLS = [
    "https://blog.samaltman.com/what-ive-learned-from-female-founders-so-far",
    "https://blog.samaltman.com/startup-advice",
    "https://blog.samaltman.com/the-worst-part-of-yc",
    "https://blog.samaltman.com/applying-to-yc",
    "https://www.michaelseibel.com/blog/yc-s-essential-startup-advice",
    "https://www.michaelseibel.com/blog/how-to-pitch-your-company",
    "https://www.michaelseibel.com/blog/how-to-email-early-stage-investors",
]

PAGE_OVERRIDES = {
    "https://blog.samaltman.com/what-ive-learned-from-female-founders-so-far": {
        "author": "Sam Altman",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use narrowly for female-founder context, application review sensitivity around gendered assumptions, and reminders to avoid stereotyping female founders.",
    },
    "https://blog.samaltman.com/startup-advice": {
        "author": "Sam Altman",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use for broad startup operating advice: make something people want, write code, talk to users, move fast, stay focused, and keep burn low.",
    },
    "https://blog.samaltman.com/the-worst-part-of-yc": {
        "author": "Sam Altman",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use when founders worry about rejection, post-YC slumps, investor signaling, or confusing YC acceptance with company success.",
    },
    "https://blog.samaltman.com/applying-to-yc": {
        "author": "Sam Altman",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use for applying-too-early/too-late doubts, simple application writing, why YC acceptance is not a judgment of founder worth, and how founders should frame their company.",
    },
    "https://www.michaelseibel.com/blog/yc-s-essential-startup-advice": {
        "author": "Geoff Ralston and Michael Seibel",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use for launch-now, talk-to-users, do-things-that-do-not-scale, 90/10 solutions, customer choice, focus, growth, and cofounder relationship advice.",
    },
    "https://www.michaelseibel.com/blog/how-to-pitch-your-company": {
        "author": "Michael Seibel",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use for company-description and pitch clarity: what you do, problem, customer, how it works, market, traction, team, and fundraising ask.",
    },
    "https://www.michaelseibel.com/blog/how-to-email-early-stage-investors": {
        "author": "Michael Seibel",
        "source_type": "YC-affiliated partner blog post",
        "status": "YC-affiliated public essay",
        "summary": "Use for concise investor-email structure, fundraising communication hygiene, and writing that makes the company easy to understand.",
    },
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

SKIP_TAGS = {"script", "style", "svg", "noscript", "iframe"}
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


@dataclass(frozen=True)
class CapturedPage:
    url: str
    title: str
    author: str
    source_type: str
    status: str
    published: str
    summary: str
    content: str


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []
        self.meta: dict[tuple[str, str], str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = attrs_by_name.get("property") or attrs_by_name.get("name") or attrs_by_name.get("itemprop")
            content = attrs_by_name.get("content")
            if key and content:
                self.meta[(key.lower(), tag)] = html.unescape(content)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        title = normalize_inline(" ".join(self.title_parts))
        return title

    def meta_content(self, key: str) -> str:
        return self.meta.get((key.lower(), "meta"), "")


class ArticleMarkdownParser(HTMLParser):
    def __init__(self, base_url: str, target_class: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.target_class = target_class
        self.capture_depth = 0
        self.done = False
        self.skip_depth = 0
        self.lines: list[str] = []
        self.current: list[str] = []
        self.current_prefix = ""
        self.list_stack: list[str] = []
        self.link_stack: list[tuple[str, list[str]]] = []
        self.blockquote_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}

        if self.done:
            return

        if not self.capture_depth:
            classes = set(attrs_by_name.get("class", "").split())
            if tag == "div" and self.target_class in classes:
                self.capture_depth = 1
            return

        if tag not in VOID_TAGS:
            self.capture_depth += 1

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return

        if tag in SKIP_TAGS:
            if tag not in VOID_TAGS:
                self.skip_depth = 1
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()
            level = min(int(tag[1]) + 1, 6)
            self.current_prefix = "#" * level + " "
        elif tag == "li":
            self.flush()
            indent = "  " * max(len(self.list_stack) - 1, 0)
            self.current_prefix = f"{indent}- "
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
        elif tag == "br":
            self.append_text("\n")
        elif tag == "a":
            self.link_stack.append((attrs_by_name.get("href", ""), []))
        elif tag == "blockquote":
            self.flush()
            self.blockquote_depth += 1
        elif tag in INLINE_MARKERS:
            self.append_text(INLINE_MARKERS[tag])
        elif tag in BLOCK_TAGS:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if self.done or not self.capture_depth:
            return

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth = max(0, self.skip_depth - 1)
            self.decrement_depth(tag)
            return

        if tag == "a" and self.link_stack:
            href, parts = self.link_stack.pop()
            text = normalize_inline("".join(parts))
            if text:
                if href and not href.startswith("#"):
                    self.append_text(f"[{text}]({urljoin(self.base_url, href)})")
                else:
                    self.append_text(text)
        elif tag in INLINE_MARKERS:
            self.append_text(INLINE_MARKERS[tag])
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6", "li", "p"}:
            self.flush()
        elif tag in {"ul", "ol"}:
            self.flush()
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "blockquote":
            self.flush()
            self.blockquote_depth = max(0, self.blockquote_depth - 1)
        elif tag in BLOCK_TAGS:
            self.flush()

        self.decrement_depth(tag)

    def handle_data(self, data: str) -> None:
        if self.done or not self.capture_depth or self.skip_depth:
            return
        self.append_text(data)

    def append_text(self, value: str) -> None:
        if self.link_stack:
            self.link_stack[-1][1].append(value)
            return

        if value == "\n":
            text = value
        else:
            value = value.replace("\n", " ")
            text = normalize_text_fragment(value)
        if not text:
            return
        if self.current and not self.current[-1].endswith(("\n", " ")):
            previous = self.current[-1][-1]
            if previous not in "([/" and text[0] not in ".,:;!?)]":
                self.current.append(" ")
        self.current.append(text)

    def flush(self) -> None:
        text = normalize_inline("".join(self.current))
        self.current = []
        if not text:
            self.current_prefix = ""
            return

        prefix = self.current_prefix
        if self.blockquote_depth and not prefix:
            prefix = "> "
        line = prefix + text
        if self.lines and self.lines[-1] != "":
            self.lines.append("")
        self.lines.append(line)
        self.current_prefix = ""

    def decrement_depth(self, tag: str) -> None:
        if tag not in VOID_TAGS:
            self.capture_depth = max(0, self.capture_depth - 1)
            if self.capture_depth == 0:
                self.flush()
                self.done = True

    @property
    def markdown(self) -> str:
        self.flush()
        return "\n".join(dedupe_adjacent_blank_lines(self.lines)).strip()


def normalize_text_fragment(value: str) -> str:
    value = unicodedata.normalize("NFKC", html.unescape(value))
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    return value


def normalize_inline(value: str) -> str:
    value = normalize_text_fragment(value)
    value = re.sub(r"\s*\n\s*", "\n", value)
    value = re.sub(r" {2,}", " ", value)
    return value.strip()


def dedupe_adjacent_blank_lines(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    for line in lines:
        if line == "" and cleaned and cleaned[-1] == "":
            continue
        cleaned.append(line)
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    return cleaned


def tidy_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    cleaned: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        number_match = re.fullmatch(r"(\d+)\.", line.strip())
        if number_match:
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            if next_index < len(lines):
                cleaned.append(f"{number_match.group(1)}. {lines[next_index].strip()}")
                index = next_index + 1
                continue

        line = re.sub(r"^\* \*\* (.*?) \*\* \*$", r"**\1**", line)
        line = re.sub(r"^\*\* (.*?) \*\*$", r"**\1**", line)
        cleaned.append(line)
        index += 1
    return "\n".join(dedupe_adjacent_blank_lines(cleaned)).strip()


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", "replace")


def target_class_for_url(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    if hostname == "blog.samaltman.com":
        return "posthaven-post-body"
    if hostname == "www.michaelseibel.com":
        return "s-blog-body"
    raise ValueError(f"Unsupported partner blog host: {hostname}")


def clean_title(title: str, url: str, metadata: MetadataParser) -> str:
    title = metadata.meta_content("og:title") or title
    title = re.sub(r"\s+-\s+Sam Altman$", "", title).strip()
    if not title:
        title = urlparse(url).path.strip("/").replace("-", " ").title()
    return title


def published_date(html_text: str, url: str) -> str:
    if "blog.samaltman.com" in url:
        match = re.search(r'data-unix-time="(\d+)"', html_text)
        if match:
            timestamp = int(match.group(1))
            return dt.datetime.fromtimestamp(timestamp, tz=dt.UTC).date().isoformat()

    json_ld_match = re.search(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if json_ld_match:
        try:
            data = json.loads(html.unescape(json_ld_match.group(1)))
        except json.JSONDecodeError:
            data = {}
        published = data.get("datePublished")
        if isinstance(published, str) and published.strip():
            return published.strip()

    return "Unknown"


def slug_for(page: CapturedPage) -> str:
    hostname = urlparse(page.url).hostname or ""
    prefix = ""
    if hostname == "blog.samaltman.com":
        prefix = "sam-altman-"
    elif hostname == "www.michaelseibel.com":
        prefix = "michael-seibel-"

    slug = page.title.lower()
    slug = re.sub(r"&", " and ", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return f"{prefix}{slug}.md"


def capture_page(url: str) -> CapturedPage:
    html_text = fetch(url)
    metadata = MetadataParser()
    metadata.feed(html_text)
    title = clean_title(metadata.title, url, metadata)
    body_parser = ArticleMarkdownParser(url, target_class_for_url(url))
    body_parser.feed(html_text)
    content = body_parser.markdown
    if not content:
        raise ValueError(f"No article body captured for {url}")
    content = tidy_markdown(content)

    overrides = PAGE_OVERRIDES.get(url, {})
    return CapturedPage(
        url=url,
        title=title,
        author=overrides.get("author", "Unknown"),
        source_type=overrides.get("source_type", "YC-affiliated partner blog post"),
        status=overrides.get("status", "YC-affiliated public essay"),
        published=published_date(html_text, url),
        summary=overrides.get("summary", "Full captured content preserved below."),
        content=content,
    )


def render_markdown(page: CapturedPage, captured_date: str) -> str:
    lines = [
        f"# {page.title}",
        "",
        f"- Type: {page.source_type}",
        f"- Status: {page.status}",
        f"- URL: {page.url}",
        f"- Author: {page.author}",
        f"- Published: {page.published}",
        f"- Captured: {captured_date}",
        "- Method: scripts/capture_partner_blog_pages.py",
        "- Caveat: references/caveats/yc-founder-partner-source.md",
        "",
        "## Summary",
        "",
        f"- {page.summary}",
        "",
        "## Content",
        "",
        page.content,
        "",
    ]
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", default=DEFAULT_URLS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--captured-date", default=dt.date.today().isoformat())
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = ROOT_DIR / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for url in args.urls:
        page = capture_page(url)
        output_path = output_dir / slug_for(page)
        output_path.write_text(render_markdown(page, args.captured_date), encoding="utf-8")
        print(f"Wrote {output_path.relative_to(ROOT_DIR)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
