#!/usr/bin/env python3
"""Capture public Get into YC example applications.

Successful applications are written as processed Markdown resources. All public
company applications, successful and unsuccessful, are also converted into JSONL
eval fixtures so the yc-partner skill can be evaluated without using the known
outcome label in the model-facing prompt.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import socket
import sys
import time
import textwrap
import unicodedata
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://getintoyc.com/"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "skills" / "yc-partner" / "resources" / "examples" / "getintoyc"
DEFAULT_EVAL_DIR = ROOT_DIR / "evals" / "yc-application-review"
USER_AGENT = "yc-partner-capture/1.0 (+local public research)"

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

SECTIONS = {
    "company-anchor": "Company",
    "founders": "Founders",
    "category": "Category",
    "progress": "Progress",
    "idea": "Idea",
    "equity": "Equity",
    "legal": "Legal",
    "others": "Others",
    "curious": "Curious",
}

SECTION_ORDER = [
    "Company",
    "Founders",
    "Category",
    "Progress",
    "Idea",
    "Equity",
    "Legal",
    "Others",
    "Curious",
]

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


@dataclass(frozen=True)
class QuestionAnswer:
    section: str
    question: str
    question_url: str
    answer: str


@dataclass(frozen=True)
class Application:
    url: str
    slug: str
    company: str
    description: str
    batch: str
    status: str
    published: str
    modified: str
    qas: list[QuestionAnswer]


class CompanyLinkParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}
        href = attrs_by_name.get("href", "")
        if "/company/" not in href:
            return
        url = urljoin(self.base_url, href).split("#", 1)[0]
        if url.startswith(self.base_url) and url not in self.urls:
            self.urls.append(url)


class ApplicationParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.skip_depth = 0
        self.section: str | None = None
        self.question_depth = 0
        self.answer_depth = 0
        self.question_parts: list[str] = []
        self.question_href = ""
        self.answer_parts: list[str] = []
        self.link_stack: list[tuple[str, list[str]]] = []
        self.pending_question = ""
        self.pending_question_url = ""
        self.qas: list[QuestionAnswer] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}
        classes = set(attrs_by_name.get("class", "").split())

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return
        if tag in SKIP_TAGS:
            self.skip_depth = 1
            return

        section = section_for(attrs_by_name, classes)
        if section and not self.question_depth and not self.answer_depth:
            self.section = section
            return

        if not self.section:
            return

        if self.question_depth:
            if tag not in VOID_TAGS:
                self.question_depth += 1
            if tag == "a":
                self.question_href = urljoin(self.base_url, attrs_by_name.get("href", ""))
            return

        if self.answer_depth:
            if tag not in VOID_TAGS:
                self.answer_depth += 1
            if tag == "a":
                self.link_stack.append((urljoin(self.base_url, attrs_by_name.get("href", "")), []))
            elif tag == "br":
                self.add_answer_text("\n")
            elif tag == "li":
                self.add_answer_text("\n- ")
            return

        if tag == "div" and "card-top" in classes:
            self.question_depth = 1
            self.question_parts = []
            self.question_href = ""
            return

        if tag == "div" and "card-bottom" in classes:
            self.answer_depth = 1
            self.answer_parts = []
            self.link_stack = []
            return

    def handle_endtag(self, tag: str) -> None:
        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth = max(0, self.skip_depth - 1)
            return

        if self.question_depth:
            if tag not in VOID_TAGS:
                self.question_depth -= 1
                if self.question_depth == 0:
                    self.pending_question = normalize_inline("".join(self.question_parts))
                    self.pending_question_url = self.question_href
            return

        if self.answer_depth:
            if tag == "a" and self.link_stack:
                href, parts = self.link_stack.pop()
                text = normalize_inline("".join(parts))
                if text:
                    if href and href != text and not text.startswith("http"):
                        self.add_answer_text(f"[{text}]({href})")
                    else:
                        self.add_answer_text(text)
            elif tag == "p":
                self.add_answer_text("\n\n")

            if tag not in VOID_TAGS:
                self.answer_depth -= 1
                if self.answer_depth == 0:
                    answer = scrub_contact_info(normalize_block("".join(self.answer_parts)))
                    if self.section and self.pending_question and answer:
                        self.qas.append(
                            QuestionAnswer(
                                section=self.section,
                                question=scrub_contact_info(self.pending_question),
                                question_url=self.pending_question_url,
                                answer=answer,
                            )
                        )
                    self.pending_question = ""
                    self.pending_question_url = ""
            return

    def handle_data(self, data: str) -> None:
        text = normalize_inline(data)
        if not text:
            return
        if self.question_depth:
            append_text(self.question_parts, text)
        elif self.answer_depth:
            self.add_answer_text(text)

    def add_answer_text(self, text: str) -> None:
        target = self.link_stack[-1][1] if self.link_stack else self.answer_parts
        append_text(target, text)


def main() -> int:
    args = parse_args()
    socket.setdefaulttimeout(args.timeout)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not args.skip_evals:
        args.eval_dir.mkdir(parents=True, exist_ok=True)

    captured_on = dt.datetime.now(dt.timezone.utc).date()
    urls = discover_company_urls(args.source_url, args)
    applications: list[Application] = []

    for index, url in enumerate(urls, start=1):
        html = fetch_with_retry(url, args)
        app = parse_application(url, html)
        applications.append(app)
        print(
            f"{index:02d}/{len(urls)} {app.status:12} {len(app.qas):02d} answers {app.company}",
            flush=True,
        )
        if args.sleep:
            time.sleep(args.sleep)

    successful = [app for app in applications if app.status.lower() == "successful"]
    unsuccessful = [app for app in applications if app.status.lower() == "unsuccessful"]
    if len(successful) != args.expected_successful:
        raise RuntimeError(f"Expected {args.expected_successful} successful apps, found {len(successful)}")
    if len(unsuccessful) != args.expected_unsuccessful:
        raise RuntimeError(
            f"Expected {args.expected_unsuccessful} unsuccessful apps, found {len(unsuccessful)}"
        )

    for app in successful:
        output_path = args.output_dir / f"{app.slug}.md"
        output_path.write_text(render_resource_markdown(app, captured_on), encoding="utf-8")

    (args.output_dir / "README.md").write_text(render_resource_readme(successful, captured_on), encoding="utf-8")

    if not args.skip_evals:
        fixtures_path = args.eval_dir / "fixtures.jsonl"
        with fixtures_path.open("w", encoding="utf-8") as handle:
            for app in applications:
                handle.write(json.dumps(render_eval_fixture(app), ensure_ascii=True, sort_keys=True))
                handle.write("\n")

    print(f"Wrote {len(successful)} successful resources to {args.output_dir.relative_to(ROOT_DIR)}")
    if not args.skip_evals:
        print(f"Wrote {len(applications)} eval fixtures to {(args.eval_dir / 'fixtures.jsonl').relative_to(ROOT_DIR)}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=SOURCE_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--eval-dir", type=Path, default=DEFAULT_EVAL_DIR)
    parser.add_argument("--skip-evals", action="store_true")
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--sleep", type=float, default=0.15)
    parser.add_argument("--expected-successful", type=int, default=36)
    parser.add_argument("--expected-unsuccessful", type=int, default=23)
    return parser.parse_args()


def discover_company_urls(source_url: str, args: argparse.Namespace) -> list[str]:
    html = fetch_with_retry(source_url, args)
    parser = CompanyLinkParser(source_url)
    parser.feed(html)
    if not parser.urls:
        raise RuntimeError(f"No company URLs found at {source_url}")
    return parser.urls


def fetch_with_retry(url: str, args: argparse.Namespace) -> str:
    last_error: Exception | None = None
    for attempt in range(1, args.retries + 1):
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml",
                },
            )
            with urlopen(request, timeout=args.timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except Exception as error:  # noqa: BLE001 - this is a script-level retry boundary.
            last_error = error
            if attempt == args.retries:
                break
            time.sleep(min(2.0 * attempt, 6.0))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}") from last_error


def parse_application(url: str, html: str) -> Application:
    canonical = extract_meta(html, r'<link\s+rel="canonical"\s+href="([^"]+)"') or url
    company = extract_meta(html, r"<h1[^>]*>\s*<span[^>]*>(.*?)</span>\s*</h1>")
    description = extract_meta(html, r'id="text_block-62-70"[^>]*>.*?<span[^>]*>(.*?)</span>')
    batch = extract_meta(html, r"Batch:&nbsp;\s*<span[^>]*>(.*?)</span>")
    status = extract_meta(html, r"Status:&nbsp;\s*<span[^>]*>(.*?)</span>")
    published = normalize_date(extract_meta(html, r'"datePublished":"([^"]+)"'))
    modified = normalize_date(extract_meta(html, r'property="article:modified_time"\s+content="([^"]+)"'))

    parser = ApplicationParser(canonical)
    parser.feed(html)
    qas = parser.qas

    batch = batch or "Unknown"
    missing = [
        name
        for name, value in {
            "company": company,
            "description": description,
            "status": status,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing {', '.join(missing)} for {url}")
    if not qas:
        raise RuntimeError(f"No application answers found for {url}")

    return Application(
        url=canonical,
        slug=slugify(company),
        company=scrub_contact_info(company),
        description=scrub_contact_info(description),
        batch=batch,
        status=status,
        published=published or "Unknown",
        modified=modified or "Unknown",
        qas=qas,
    )


def render_resource_markdown(app: Application, captured_on: dt.date) -> str:
    return f"""# {app.company}

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: {app.url}
- Author: Get into YC / public founder-submitted application
- Published: {app.published}
- Captured: {captured_on.isoformat()}

## Summary

- Company: {app.company}
- Batch: {app.batch}
- Outcome label: {app.status}
- Description: {app.description}
- Modified: {app.modified}
- Capture detail: Get into YC labels this application as Successful; navigation, login controls, ads, comments, and site chrome were omitted.
- Privacy: recognized email addresses were redacted.

## Content

{render_application_body(app)}
"""


def render_application_body(app: Application) -> str:
    output: list[str] = []
    qas_by_section: dict[str, list[QuestionAnswer]] = {section: [] for section in SECTION_ORDER}
    for qa in app.qas:
        qas_by_section.setdefault(qa.section, []).append(qa)

    for section in SECTION_ORDER:
        qas = qas_by_section.get(section, [])
        if not qas:
            continue
        output.append(f"### {section}")
        output.append("")
        for qa in qas:
            question = markdown_link(qa.question, qa.question_url)
            output.append(f"#### {question}")
            output.append("")
            output.append(wrap_markdown_block(qa.answer))
            output.append("")

    return "\n".join(output).strip()


def render_resource_readme(apps: list[Application], captured_on: dt.date) -> str:
    rows = "\n".join(
        f"- `{app.slug}.md` - {app.company}, {app.batch}, {len(app.qas)} captured answers."
        for app in sorted(apps, key=lambda app: app.company.lower())
    )
    return f"""# Get into YC Successful Applications

Processed Markdown captures of public applications from `https://getintoyc.com/` that the source site labels as Successful.

- Captured: {captured_on.isoformat()}
- Count: {len(apps)}
- Capture script: `scripts/capture_getintoyc_examples.py`

Only successful examples are stored in this resource folder. Unsuccessful public examples are used in eval fixtures under `evals/yc-application-review/fixtures.jsonl`.

## Files

{rows}
"""


def render_eval_fixture(app: Application) -> dict[str, object]:
    successful = app.status.lower() == "successful"
    return {
        "id": f"getintoyc-{app.slug}",
        "task": "yc_application_review_outcome_calibration",
        "source": "getintoyc",
        "source_url": app.url,
        "company": app.company,
        "batch": app.batch,
        "prompt": (
            "Review the YC application below as yc-partner. Estimate whether it is likely to earn "
            "a YC interview, give an interview_likelihood score from 0.0 to 1.0, list the strongest "
            "positive evidence, list the biggest risks or missing specifics, and suggest direct "
            "non-ghostwritten improvements. Do not use or infer from any external knowledge about "
            "the company; judge only the application text."
        ),
        "application_markdown": render_eval_application(app),
        "expected": {
            "known_outcome": "successful" if successful else "unsuccessful",
            "score_band": "high" if successful else "low_or_mixed",
            "interview_likelihood_min": 0.6 if successful else None,
            "interview_likelihood_max": None if successful else 0.55,
            "rubric": [
                "Directly answers what the company makes and why users need it.",
                "Separates evidence from inference and does not overclaim.",
                "Cites concrete users, traction, revenue, speed, founder insight, or market timing when present.",
                "Calls out vague, missing, or weak application answers without rewriting the application as final copy.",
                "Does not leak or rely on the hidden known_outcome label.",
            ],
        },
    }


def render_eval_application(app: Application) -> str:
    return f"""# {app.company}

- Source: public Get into YC application text
- Batch: {app.batch}
- Description: {app.description}

{render_application_body(app)}
"""


def markdown_link(text: str, href: str) -> str:
    escaped = text.replace("[", "\\[").replace("]", "\\]")
    if not href:
        return escaped
    return f"[{escaped}]({href})"


def section_for(attrs: dict[str, str], classes: set[str]) -> str | None:
    if "section-wrapper" not in classes:
        return None
    section = SECTIONS.get(attrs.get("id", ""))
    if section == "Category":
        return None
    return section


def extract_meta(html: str, pattern: str) -> str:
    match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return scrub_contact_info(strip_tags(match.group(1)))


def strip_tags(value: str) -> str:
    return normalize_inline(re.sub(r"<[^>]+>", " ", value))


def normalize_date(value: str) -> str:
    if not value:
        return ""
    return value.split("T", 1)[0]


def append_text(parts: list[str], text: str) -> None:
    if parts and not parts[-1].endswith((" ", "\n")) and text and text[0] not in ".,:;!?)]":
        parts.append(" ")
    parts.append(text)


def normalize_inline(value: str) -> str:
    value = normalize_unicode(unescape(value))
    value = re.sub(r"[ \t\r\n]+", " ", value)
    return value.strip()


def normalize_block(value: str) -> str:
    value = normalize_unicode(unescape(value))
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_unicode(value: str) -> str:
    replacements = {
        "\u00a0": " ",
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
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def scrub_contact_info(value: str) -> str:
    return EMAIL_RE.sub("[redacted email]", value)


def wrap_markdown_block(value: str) -> str:
    paragraphs = []
    for paragraph in value.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if paragraph.startswith("- "):
            paragraphs.append(paragraph)
        else:
            paragraphs.append(textwrap.fill(paragraph, width=100))
    return "\n\n".join(paragraphs)


def slugify(value: str) -> str:
    value = normalize_unicode(value).lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "application"


if __name__ == "__main__":
    sys.exit(main())
