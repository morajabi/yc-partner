#!/usr/bin/env python3
"""Capture public YC Library video pages as processed Markdown."""

from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CAPTURED = "2026-06-16"


@dataclass(frozen=True)
class Capture:
    url: str
    output: Path
    type_: str
    author_fallback: str
    summary: list[str]


CAPTURES = [
    Capture(
        url="https://www.ycombinator.com/library/JA-yc-application-tips-when-to-apply",
        output=Path("skills/yc-partner/resources/yc-website/yc-library/yc-application-tips-when-to-apply.md"),
        type_="Official YC Library video transcript",
        author_fallback="Stephanie Simon",
        summary=[
            "Stephanie Simon says founders should apply to YC when they are working on a startup and think YC would benefit the company.",
            "The key application timing guidance is that there is no such thing as too early or too late; YC reads applications year round.",
            "Use for founder doubts about timing, being too early, being too late, or whether the company has to wait for more traction before applying.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/J9-yc-application-tips-you-don-t-need-to-know-someone",
        output=Path("skills/yc-partner/resources/yc-website/yc-library/yc-application-tips-you-dont-need-to-know-someone.md"),
        type_="Official YC Library video transcript",
        author_fallback="Stephanie Simon",
        summary=[
            "Stephanie Simon says founders do not need to know anyone at YC to get in.",
            "She says alumni recommendations are optional when the alum knows the founder well, but hundreds of startups get into each batch without a recommendation.",
            "Use when founders think they need a warm intro, alumni recommendation, or insider access before applying.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/J8-yc-application-tips-include-a-demo",
        output=Path("skills/yc-partner/resources/yc-website/yc-library/yc-application-tips-include-a-demo.md"),
        type_="Official YC Library video transcript",
        author_fallback="Stephanie Simon",
        summary=[
            "Stephanie Simon says more founders should include a product demo in the YC application.",
            "The demo can be unpolished, local, or as rough as a CSV; the important difference is showing that something exists rather than only an idea.",
            "Use when reviewing application hygiene, product evidence, demo links, and founder seriousness.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/It-how-to-apply-and-succeed-at-yc",
        output=Path("skills/yc-partner/resources/yc-website/yc-library/how-to-apply-and-succeed-at-yc.md"),
        type_="Official YC Library video transcript",
        author_fallback="Dalton Caldwell",
        summary=[
            "Dalton Caldwell explains why applying to YC is worth doing, how to think about the application, common excuses not to apply, interview mechanics, and what successful YC founders do during the batch.",
            "Key application guidance includes: the application clarifies founder thinking, the downside of applying is small, avoiding rejection reduces luck surface area, and many common reasons not to apply are not valid.",
            "Use as a broad official YC source for application timing, application quality, interview prep, reapplying, founder posture, and YC value.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/IJ-successful-yc-application-video-teespring-yc-w2013",
        output=Path("skills/yc-partner/resources/examples/teespring-yc-w2013-application-video.md"),
        type_="Public YC application video transcript",
        author_fallback="Y Combinator",
        summary=[
            "Official YC Library transcript of Teespring's successful YC W2013 application video.",
            "The video gives a concise product explanation, revenue progress, recent monthly revenue, growth, scaling need, and why YC could help.",
            "Use as an example of a short application video with concrete traction and a clear ask, not as a universal script or YC policy.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/II-successful-yc-application-video-zenefits-yc-w2013",
        output=Path("skills/yc-partner/resources/examples/zenefits-yc-w2013-application-video.md"),
        type_="Public YC application video transcript",
        author_fallback="Y Combinator",
        summary=[
            "Official YC Library transcript of Zenefits' successful YC W2013 application video.",
            "The video explains the product workflow, target customer, founder background, broker economics, regulatory work, payroll integrations, and early traction.",
            "Use as an example of explaining a boring but high-value B2B problem with domain insight and specific business-model detail.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/IH-successful-yc-application-video-flip-yc-w2015",
        output=Path("skills/yc-partner/resources/examples/flip-yc-w2015-application-video.md"),
        type_="Public YC application video transcript",
        author_fallback="Y Combinator",
        summary=[
            "Official YC Library transcript of Flip's successful YC W2015 application video.",
            "The video gives founder background, domain connection to sneakers, product mechanics, market behavior, revenue model, and seller/liquidity evidence.",
            "Use as an example of founder-market fit and a narrow wedge into a larger marketplace.",
        ],
    ),
    Capture(
        url="https://www.ycombinator.com/library/IG-successful-yc-application-video-campus-job-yc-w2015",
        output=Path("skills/yc-partner/resources/examples/campus-job-yc-w2015-application-video.md"),
        type_="Public YC application video transcript",
        author_fallback="Y Combinator",
        summary=[
            "Official YC Library transcript of Campus Job's successful YC W2015 application video.",
            "The video explains the marketplace, founder roles, seven-week user and job-listing traction, revenue model, sales pipeline, and market-size ambition.",
            "Use as an example of concise marketplace explanation with early supply/demand metrics and founder roles.",
        ],
    ),
]


class DataPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data_page: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if "data-page" in attrs_dict:
            self.data_page = attrs_dict["data-page"]


def fetch_article(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = DataPageParser()
    parser.feed(html)
    if not parser.data_page:
        raise RuntimeError(f"missing data-page payload for {url}")
    data = json.loads(unescape(parser.data_page))
    return data["props"]["article"]


def date_only(value: str | None) -> str:
    if not value:
        return "Unknown"
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def duration(value: int | None) -> str:
    if value is None:
        return "unknown"
    minutes, seconds = divmod(value, 60)
    return f"{minutes:02d}:{seconds:02d}"


def wrap_transcript(text: str) -> str:
    paragraphs = []
    for para in text.strip().split("\n\n"):
        para = " ".join(para.split())
        if not para:
            continue
        paragraphs.append(textwrap.fill(para, width=100))
    return "\n\n".join(paragraphs)


def markdown(capture: Capture, article: dict) -> str:
    author = article.get("author") or capture.author_fallback
    youtube_url = article.get("link")
    video_id = article.get("youtube_id")
    transcript = article.get("transcript") or ""
    if not transcript.strip():
        raise RuntimeError(f"missing transcript for {capture.url}")

    lines = [
        f"# {article['title']}",
        "",
        f"- Type: {capture.type_}",
        "- Status: Official YC public source",
        f"- URL: {youtube_url}",
        f"- Author: {author}",
        f"- Published: {date_only(article.get('created_at'))}",
        f"- Captured: {CAPTURED}",
        "- Method: YC Library data-page transcript",
        "- Caveat: references/caveats/official-yc-source.md",
        "",
        "## Summary",
        "",
    ]
    lines.extend(f"- {item}" for item in capture.summary)
    lines.extend(
        [
            f"- YC Library URL: {capture.url}.",
            f"- Video ID: {video_id}; duration: {duration(article.get('video_duration'))}; YC Library view count at capture: {article.get('youtube_view_count')}.",
            "",
            "## Transcript",
            "",
            wrap_transcript(transcript),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for capture in CAPTURES:
        article = fetch_article(capture.url)
        output = ROOT / capture.output
        text = markdown(capture, article)
        if args.dry_run:
            print(f"--- {capture.output}")
            print(text[:1000])
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
