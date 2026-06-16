#!/usr/bin/env python3
"""Capture official YC Blog posts as processed Markdown."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from datetime import date, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "skills" / "yc-partner" / "resources" / "yc-website" / "yc-blog"


class DataPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data_page: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if "data-page" in attrs_dict:
            self.data_page = attrs_dict["data-page"]


class HtmlToMarkdown(HTMLParser):
    SKIP_TAGS = {"script", "style", "svg", "noscript"}
    BLOCK_TAGS = {
        "blockquote",
        "div",
        "figure",
        "li",
        "ol",
        "p",
        "pre",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.current: list[str] = []
        self.current_prefix = ""
        self.skip_depth = 0
        self.list_depth = 0
        self.link_href: str | None = None
        self.link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()
            self.current_prefix = "#" * min(int(tag[1]) + 1, 6) + " "
        elif tag == "li":
            self.flush()
            self.current_prefix = f"{'  ' * max(self.list_depth - 1, 0)}- "
        elif tag in {"ul", "ol"}:
            self.list_depth += 1
        elif tag == "br":
            self.current.append("\n")
        elif tag == "a":
            attrs_dict = dict(attrs)
            self.link_href = attrs_dict.get("href")
            self.link_text = []
        elif tag in self.BLOCK_TAGS:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "a" and self.link_href is not None:
            text = normalize_space(" ".join(self.link_text))
            if text:
                href = self.link_href
                self.current.append(f"[{text}]({href})" if href else text)
            self.link_href = None
            self.link_text = []
        elif tag in {"ul", "ol"}:
            self.list_depth = max(self.list_depth - 1, 0)
            self.flush()
        elif tag in self.BLOCK_TAGS or tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = normalize_space(data)
        if not text:
            return
        if self.link_href is not None:
            self.link_text.append(text)
        else:
            self.current.append(text)

    def flush(self) -> None:
        text = normalize_space(" ".join(self.current))
        if text:
            line = f"{self.current_prefix}{text}".rstrip()
            if self.current_prefix.startswith("- "):
                self.lines.append(line)
            else:
                self.lines.extend(textwrap.wrap(line, width=100) or [line])
        self.current = []
        self.current_prefix = ""

    def markdown(self) -> str:
        self.flush()
        output: list[str] = []
        previous_blank = True
        for line in self.lines:
            blank = not line.strip()
            if blank and previous_blank:
                continue
            output.append(line)
            previous_blank = blank
        return "\n\n".join(output)


def normalize_space(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = value.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:90].strip("-") or "yc-blog-post"


def fetch_post(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.netloc != "www.ycombinator.com" or not parsed.path.startswith("/blog/"):
        raise ValueError(f"not an official YC Blog URL: {url}")
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = DataPageParser()
    parser.feed(html)
    if not parser.data_page:
        raise RuntimeError(f"missing data-page payload for {url}")
    data = json.loads(unescape(parser.data_page))
    post = data["props"]["post"]
    post["source_url"] = url
    return post


def date_only(value: str | None) -> str:
    if not value:
        return "Unknown"
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def author_name(post: dict) -> str:
    author = post.get("primary_author") or {}
    return author.get("name") or ", ".join(a.get("name", "") for a in post.get("authors", [])).strip(", ") or "Y Combinator"


def post_markdown(post: dict) -> str:
    parser = HtmlToMarkdown()
    parser.feed(post.get("html") or "")
    content = parser.markdown()
    if not content:
        raise RuntimeError(f"empty post content for {post.get('source_url')}")
    return "\n".join(
        [
            f"# {post.get('title') or 'YC Blog Post'}",
            "",
            "- Type: Official YC Blog post",
            "- Status: Official YC public source",
            f"- URL: {post['source_url']}",
            f"- Author: {author_name(post)}",
            f"- Published: {date_only(post.get('published_at') or post.get('created_at'))}",
            f"- Captured: {date.today().isoformat()}",
            "- Method: scripts/capture_yc_blog_pages.py data-page post HTML",
            "- Caveat: references/caveats/official-yc-source.md",
            "",
            "## Summary",
            "",
            f"- Official YC Blog post by {author_name(post)}.",
            f"- Excerpt: {normalize_space(post.get('excerpt') or post.get('custom_excerpt') or '')}",
            "- Full processed post text preserved below.",
            "",
            "## Content",
            "",
            content,
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="Official YC Blog post URLs to capture.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for url in args.urls:
        post = fetch_post(url)
        output = args.output_dir / f"{slugify(post.get('title') or post.get('slug') or url)}.md"
        text = post_markdown(post)
        if args.dry_run:
            print(f"--- {output.relative_to(ROOT)}")
            print(text[:1000])
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
