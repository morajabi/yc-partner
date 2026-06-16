#!/usr/bin/env python3
"""Capture Lago's public successful YC application from the Lago blog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import textwrap
import unicodedata
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://getlago.com/blog/how-we-got-into-yc"
YC_COMPANY_URL = "https://www.ycombinator.com/companies/lago"
OUTPUT_PATH = ROOT_DIR / "skills" / "yc-partner" / "resources" / "examples" / "lago-yc-application.md"
EVALS_PATH = ROOT_DIR / "evals" / "yc-application-review" / "fixtures.jsonl"
USER_AGENT = "yc-partner-capture/1.0 (+local public research)"

COMPANY = "Lago"
DESCRIPTION = "A no-code data tool for Growth teams."
BATCH = "S21"
PUBLISHED = "2022-11-11"
AUTHOR = "Anh-Tho Chuong"
TITLE = "How we got into YC, pre-product, pre-revenue"

SECTIONS = {"Company", "PROGRESS", "Progress", "Idea", "Others", "Curious"}
QUESTION_PREFIXES = (
    "Company name",
    "Company URL",
    "Describe what your company does",
    "What is your company going to make?",
    "Where do you live now,",
    "How far along are you?",
    "How long have each of you been working on this?",
    "Are people using your product?",
    "Do you have revenue?",
    "If you are applying with the same idea",
    "If you have already participated",
    "Why did you pick this idea",
    "What's new about what you're making?",
    "What do you understand about your business",
    "How do or will you make money?",
    "How will you get users?",
    "Is there anything else we should know",
    "If you had any other ideas",
    "Please tell us something surprising",
    "What convinced you to apply",
    "How did you hear about YC?",
)


@dataclass(frozen=True)
class QuestionAnswer:
    section: str
    question: str
    answer: str


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip_depth += 1
        elif tag in {"p", "h1", "h2", "h3", "h4", "div", "br"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in {"p", "h1", "h2", "h3", "h4", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = normalize_inline(data)
        if text:
            self.parts.append(text)

    @property
    def text(self) -> str:
        text = "\n".join(self.parts)
        text = re.sub(r"\n{2,}", "\n", text)
        return text.strip()


def main() -> int:
    args = parse_args()
    captured_on = dt.datetime.now(dt.timezone.utc).date()
    html = fetch(args.url)
    application_text = extract_application_text(html)
    qas = parse_qas(application_text)

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    args.output_path.write_text(render_resource(qas, captured_on, args.url), encoding="utf-8")
    upsert_eval(args.evals_path, qas, args.url)

    print(f"Wrote {args.output_path.relative_to(ROOT_DIR)}")
    print(f"Upserted eval fixture getlago-lago in {args.evals_path.relative_to(ROOT_DIR)}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=SOURCE_URL)
    parser.add_argument("--output-path", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--evals-path", type=Path, default=EVALS_PATH)
    return parser.parse_args()


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def extract_application_text(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    text = parser.text
    start = text.find("LAGO YC Application")
    end = text.find("Share on", start)
    if start == -1 or end == -1:
        raise RuntimeError("Could not locate Lago YC application boundaries in page text")
    return normalize_block(text[start:end])


def parse_qas(application_text: str) -> list[QuestionAnswer]:
    qas: list[QuestionAnswer] = []
    section = ""
    question = ""
    answer: list[str] = []

    for raw_line in application_text.splitlines():
        line = raw_line.strip()
        if not line or line == "LAGO YC Application":
            continue
        if is_section(line):
            flush(qas, section, question, answer)
            section = "Progress" if line == "PROGRESS" else line
            question = ""
            answer = []
            continue
        if is_question(line):
            flush(qas, section, question, answer)
            question = line
            answer = []
            continue
        if question:
            answer.append(line)

    flush(qas, section, question, answer)
    if len(qas) < 15:
        raise RuntimeError(f"Expected at least 15 Lago application answers, found {len(qas)}")
    return qas


def flush(qas: list[QuestionAnswer], section: str, question: str, answer: list[str]) -> None:
    if section and question and answer:
        qas.append(QuestionAnswer(section=section, question=question, answer=normalize_answer(answer)))


def is_section(line: str) -> bool:
    return line in SECTIONS


def is_question(line: str) -> bool:
    return any(line.startswith(prefix) for prefix in QUESTION_PREFIXES)


def normalize_answer(lines: list[str]) -> str:
    joined_lines: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line == "-" and index + 1 < len(lines):
            joined_lines.append(f"- {lines[index + 1]}")
            index += 2
            continue
        if line.startswith("- "):
            joined_lines.append(line)
        elif joined_lines and joined_lines[-1].startswith("- ") and not line.startswith("- "):
            joined_lines[-1] = f"{joined_lines[-1]} {line}"
        else:
            joined_lines.append(line)
        index += 1
    return normalize_block("\n\n".join(joined_lines))


def render_resource(qas: list[QuestionAnswer], captured_on: dt.date, source_url: str) -> str:
    return f"""# Lago YC Application

- Type: Public YC application example
- Status: Public successful application published by the company
- URL: {source_url}
- Author: {AUTHOR} / Lago
- Published: {PUBLISHED}
- Captured: {captured_on.isoformat()}

## Summary

- Supporting YC company URL: {YC_COMPANY_URL}
- Company: {COMPANY}
- Batch: {BATCH}
- Outcome label: Successful
- Description: {DESCRIPTION}
- Source context: The Lago blog post frames this as the application the founders sent to YC before they had a launched product or revenue.
- Capture detail: Lago says this application got into YC on the first attempt; YC batch was verified against the public YC company directory; navigation, sharing controls, related posts, and site chrome were omitted.

## Content

{render_application_body(qas)}
"""


def render_application_body(qas: list[QuestionAnswer]) -> str:
    sections: dict[str, list[QuestionAnswer]] = {}
    for qa in qas:
        sections.setdefault(qa.section, []).append(qa)

    lines: list[str] = []
    for section in ("Company", "Progress", "Idea", "Others", "Curious"):
        if section not in sections:
            continue
        lines.extend([f"### {section}", ""])
        for qa in sections[section]:
            lines.extend([f"#### {qa.question}", "", wrap_markdown_block(qa.answer), ""])
    return "\n".join(lines).strip()


def upsert_eval(path: Path, qas: list[QuestionAnswer], source_url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if path.exists():
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    row = render_eval_fixture(qas, source_url)
    rows = [existing for existing in rows if existing.get("id") != row["id"]]
    rows.append(row)
    path.write_text(
        "".join(json.dumps(existing, ensure_ascii=True, sort_keys=True) + "\n" for existing in rows),
        encoding="utf-8",
    )


def render_eval_fixture(qas: list[QuestionAnswer], source_url: str) -> dict[str, object]:
    return {
        "id": "getlago-lago",
        "task": "yc_application_review_outcome_calibration",
        "source": "lago-blog",
        "source_url": source_url,
        "company": COMPANY,
        "batch": BATCH,
        "prompt": (
            "Review the YC application below as yc-partner. Estimate whether it is likely to earn "
            "a YC interview, give an interview_likelihood score from 0.0 to 1.0, list the strongest "
            "positive evidence, list the biggest risks or missing specifics, and suggest direct "
            "non-ghostwritten improvements. Do not use or infer from any external knowledge about "
            "the company; judge only the application text."
        ),
        "application_markdown": f"""# {COMPANY}

- Source: public Lago blog application text
- Batch: {BATCH}
- Description: {DESCRIPTION}

{render_application_body(qas)}
""",
        "expected": {
            "known_outcome": "successful",
            "score_band": "high",
            "interview_likelihood_min": 0.6,
            "interview_likelihood_max": None,
            "rubric": [
                "Directly answers what the company makes and why users need it.",
                "Separates evidence from inference and does not overclaim.",
                "Cites concrete users, traction, speed, founder insight, or market timing when present.",
                "Calls out missing product/revenue honestly while weighing pre-product evidence.",
                "Does not leak or rely on the hidden known_outcome label.",
            ],
        },
    }


def normalize_inline(value: str) -> str:
    value = normalize_unicode(unescape(value))
    value = re.sub(r"[ \t\r\n]+", " ", value)
    return value.strip()


def normalize_block(value: str) -> str:
    value = normalize_unicode(unescape(value))
    value = value.replace(".Therefore", ". Therefore")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_unicode(value: str) -> str:
    replacements = {
        "\u00a0": " ",
        "\u200d": "\n",
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


if __name__ == "__main__":
    sys.exit(main())
