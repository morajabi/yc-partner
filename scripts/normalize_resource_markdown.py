#!/usr/bin/env python3
"""Normalize processed resource Markdown files.

This keeps source files in the compact shape expected by AGENTS.md:
title, compact metadata, one Summary section, then full captured content.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ROOT_DIR / "skills" / "yc-partner" / "resources"

DROP_SECTION_TITLES = {
    "key guidance",
    "application/interview relevance",
    "caveats",
    "why this may match inline",
    "possible inline framing",
}

SKIP_META_LABELS = {
    "processed",
    "processing notes",
    "privacy notes",
    "source title",
    "transcript source",
    "capture method",
}

LABEL_MAP = {
    "source type": "Type",
    "source status": "Status",
    "original public url": "URL",
    "original url": "URL",
    "author/channel": "Author",
    "channel": "Author",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[DEFAULT_ROOT])
    parser.add_argument("--check", action="store_true", help="Report files that would change.")
    args = parser.parse_args()

    files: list[Path] = []
    for path in args.paths:
        resolved = path if path.is_absolute() else ROOT_DIR / path
        if resolved.is_dir():
            files.extend(
                file
                for file in resolved.rglob("*.md")
                if file.name != "README.md" and ".env" not in file.name
            )
        elif resolved.suffix == ".md" and resolved.name != "README.md":
            files.append(resolved)

    changed: list[Path] = []
    for file in sorted(set(files)):
        original = file.read_text(encoding="utf-8")
        normalized = normalize_markdown(original)
        if normalized != original:
            changed.append(file)
            if not args.check:
                file.write_text(normalized, encoding="utf-8")

    for file in changed:
        print(relative(file))

    if args.check and changed:
        return 1
    return 0


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        return text

    first_section = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    title = lines[0].rstrip()
    metadata_lines = lines[1:first_section]
    section_lines = lines[first_section:]

    metadata, meta_summary = parse_metadata(metadata_lines)
    sections = parse_sections(section_lines)

    summary_lines: list[str] = []
    content_blocks: list[tuple[str, list[str]]] = []
    active_content_heading: str | None = None
    active_content_body: list[str] = []

    for heading, body in sections:
        normalized_heading = heading[3:].strip().lower()
        clean_body = trim_blank_edges(body)
        if normalized_heading == "summary":
            summary_lines.extend(clean_summary(clean_body))
        elif normalized_heading in {"application metadata", "metadata", "source article context"}:
            summary_lines.extend(clean_summary(clean_body))
        elif normalized_heading == "source link":
            continue
        elif normalized_heading in DROP_SECTION_TITLES:
            if active_content_heading is not None:
                content_blocks.append((active_content_heading, trim_blank_edges(active_content_body)))
                active_content_heading = None
                active_content_body = []
            continue
        elif normalized_heading in {
            "full processed text",
            "extracted page content",
            "user-provided excerpt",
            "content",
            "transcript",
            "essay text",
            "page text",
        }:
            if active_content_heading is not None:
                content_blocks.append((active_content_heading, trim_blank_edges(active_content_body)))
            active_content_heading = normalized_content_heading(normalized_heading, metadata, clean_body)
            active_content_body = clean_body[:]
        else:
            if active_content_heading is not None:
                active_content_body.extend(["", heading, "", *clean_body])
            else:
                content_blocks.append((heading, clean_body))

    if active_content_heading is not None:
        content_blocks.append((active_content_heading, trim_blank_edges(active_content_body)))

    summary_lines = remove_pending(summary_lines)
    summary_lines.extend(meta_summary)
    summary_lines = unique_preserving_order([sanitize_note(line) for line in summary_lines])
    summary_lines = [line for line in summary_lines if line and not should_drop_summary_note(line)]
    metadata, summary_lines = ensure_minimal_metadata(metadata, summary_lines)
    add_inferred_caveat(metadata, metadata_labels(metadata))
    if not summary_lines:
        summary_lines = ["- Full captured content preserved below."]

    output: list[str] = [title, ""]
    output.extend(metadata)
    output.extend(["", "## Summary", ""])
    output.extend(summary_lines)
    output.append("")

    if content_blocks:
        for index, (heading, body) in enumerate(content_blocks):
            if len(body) > 1 and body[0] == "_No content extracted._":
                body = body[1:]
            output.append(heading)
            output.append("")
            output.extend(body if body else ["_No content extracted._"])
            if index != len(content_blocks) - 1:
                output.append("")
    else:
        output.extend(["## Content", "", "_No content extracted._"])

    return "\n".join(output).rstrip() + "\n"


def parse_metadata(lines: list[str]) -> tuple[list[str], list[str]]:
    metadata: list[str] = []
    summary: list[str] = []
    index = 0
    seen_labels: set[str] = set()

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if not stripped.startswith("- "):
            summary.append(f"- {sanitize_note(stripped)}")
            index += 1
            continue

        body = stripped[2:]
        label, value = split_label(body)
        normalized_label = normalize_label(label)

        if normalized_label in {"processing notes", "privacy notes"}:
            nested, index = consume_nested_bullets(lines, index + 1)
            summary.extend(f"- {sanitize_note(item)}" for item in nested)
            continue

        if normalized_label in SKIP_META_LABELS:
            if value:
                summary.append(f"- {sanitize_note(value)}")
            index += 1
            continue

        label = LABEL_MAP.get(normalized_label, label.strip())
        if label == "Captured or processed date":
            label = "Captured"

        if label.lower() in {"batch", "batch/application cycle", "related public url", "referenced url", "company", "person", "use", "scope", "video id", "duration", "transcript language", "transcription method"}:
            if value:
                summary.append(f"- {label}: {sanitize_note(value)}")
            index += 1
            continue

        if label not in {"Type", "Status", "URL", "Author", "Published", "Captured", "Method", "Caveat"}:
            if value:
                summary.append(f"- {label}: {sanitize_note(value)}")
            index += 1
            continue

        if label in seen_labels:
            index += 1
            continue
        seen_labels.add(label)
        metadata.append(f"- {label}: {sanitize_note(value)}")
        index += 1

    add_inferred_caveat(metadata, seen_labels)
    return metadata, summary


def consume_nested_bullets(lines: list[str], start: int) -> tuple[list[str], int]:
    items: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.startswith("  - "):
            items.append(line[4:].strip())
            index += 1
            continue
        if not line.strip():
            index += 1
            continue
        break
    return items, index


def parse_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_body))
            current_heading = line.rstrip()
            current_body = []
        elif current_heading is not None:
            current_body.append(line.rstrip())

    if current_heading is not None:
        sections.append((current_heading, current_body))
    return sections


def split_label(text: str) -> tuple[str, str]:
    if ":" not in text:
        return text.strip(), ""
    label, value = text.split(":", 1)
    return label.strip(), value.strip()


def normalize_label(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def content_heading(metadata: list[str], body: list[str]) -> str:
    joined_meta = "\n".join(metadata).lower()
    joined_body = "\n".join(body[:10]).lower()
    if "youtube" in joined_meta or "transcript" in joined_meta:
        return "## Transcript"
    if "essay" in joined_meta:
        return "## Essay Text"
    if "website" in joined_meta or "faq" in joined_meta or "application form" in joined_meta:
        return "## Page Text"
    if "transcript" in joined_body:
        return "## Transcript"
    return "## Content"


def normalized_content_heading(heading: str, metadata: list[str], body: list[str]) -> str:
    if heading in {"transcript", "content"}:
        return "## " + heading.title()
    if heading == "essay text":
        return "## Essay Text"
    if heading == "page text":
        return "## Page Text"
    if heading == "extracted page content":
        return "## Page Text"
    if heading == "user-provided excerpt":
        return "## Content"
    return content_heading(metadata, body)


def ensure_minimal_metadata(
    metadata: list[str], summary: list[str]
) -> tuple[list[str], list[str]]:
    joined = "\n".join(summary).lower()
    has_type = any(line.startswith("- Type:") for line in metadata)
    has_status = any(line.startswith("- Status:") for line in metadata)
    has_url = any(line.startswith("- URL:") for line in metadata)
    has_author = any(line.startswith("- Author:") for line in metadata)
    has_captured = any(line.startswith("- Captured:") for line in metadata)
    has_method = any(line.startswith("- Method:") for line in metadata)

    if "yc playlist: dalton & michael" in joined:
        additions: list[str] = []
        if not has_type:
            additions.append("- Type: Dalton + Michael video transcript")
        if not has_status:
            additions.append("- Status: YC founder/partner source")
        if not has_url:
            video = find_summary_value(summary, "Video")
            if video:
                additions.append(f"- URL: {video}")
                summary = remove_summary_label(summary, "Video")
        if not has_author:
            additions.append("- Author: Dalton Caldwell and Michael Seibel")
        if not has_captured:
            downloaded = find_summary_value(summary, "Downloaded")
            if downloaded:
                additions.append(f"- Captured: {downloaded}")
                summary = remove_summary_label(summary, "Downloaded")
        if not has_method:
            additions.append("- Method: YouTube auto-generated captions")
        metadata = additions + metadata
        summary = remove_summary_label(summary, "Source")

    return metadata, summary


def find_summary_value(summary: list[str], label: str) -> str | None:
    prefix = f"- {label}:"
    for line in summary:
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def remove_summary_label(summary: list[str], label: str) -> list[str]:
    prefix = f"- {label}:"
    return [line for line in summary if not line.startswith(prefix)]


def clean_summary(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    expanded_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") and " - " in stripped:
            expanded_lines.extend(split_embedded_bullets(stripped))
        else:
            expanded_lines.append(line)

    for paragraph in split_paragraphs(expanded_lines):
        if all(line.strip().startswith("- ") for line in paragraph):
            cleaned.extend(sanitize_note(line.strip()) for line in paragraph)
            continue
        text = " ".join(line.strip() for line in paragraph).strip()
        if not text:
            continue
        if text.startswith("- "):
            cleaned.append(sanitize_note(text))
        else:
            cleaned.append(f"- {sanitize_note(text)}")
    return cleaned


def split_embedded_bullets(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("- "):
        return [line]
    parts = re.split(r"\s+- (?=[A-Z][A-Za-z0-9 /+().&-]{1,50}:)", line[2:])
    return [f"- {part.strip()}" for part in parts if part.strip()]


def split_paragraphs(lines: list[str]) -> list[list[str]]:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line)
        elif current:
            paragraphs.append(current)
            current = []
    if current:
        paragraphs.append(current)
    return paragraphs


def remove_pending(lines: list[str]) -> list[str]:
    return [line for line in lines if "pending manual" not in line.lower()]


def should_drop_summary_note(line: str) -> bool:
    value = line.strip().lower().removeprefix("- ").strip()
    if not value or value == ".":
        return True
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return True
    drop_fragments = (
        "body text was normalized into markdown",
        "page headings and body text were normalized into markdown",
        "section headings and body text were normalized into markdown",
        "navigation, scripts, images",
        "navigation, footer links",
        "navigation, table of contents",
        "navigation, batch tabs",
        "site chrome",
        "processed from the public",
        "converted from local html capture",
        "generated by `scripts/",
        "split from the public single-page",
        "section anchor:",
    )
    return any(fragment in value for fragment in drop_fragments)


def sanitize_note(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    lower = text.lower()
    if "not independently fetched" in lower or "not independently reverified" in lower:
        return ""
    text = text.replace("user-provided", "pasted public")
    text = text.replace("User-provided", "Pasted public")
    text = text.replace("; YC-affiliated context, not official YC guidance", "; YC founder/partner source")
    text = text.replace("; YC-affiliated context, not official YC website guidance", "; YC founder/partner source")
    text = text.replace(", not official YC guidance", "")
    text = text.replace(", not official YC website guidance", "")
    text = text.replace("not official current YC application policy", "YC founder/partner source")
    text = text.replace("provided capture", "capture")
    text = text.replace("Provided capture", "Capture")
    text = text.replace("Pasted public external founder anecdote", "Public founder anecdote")
    text = text.replace("pasted public external founder anecdote", "public founder anecdote")
    text = text.replace("Not verified against an original URL in this capture", "Public founder story context")
    text = text.replace("Anecdotal context only; not official YC guidance", "Founder-story context")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def add_inferred_caveat(metadata: list[str], seen_labels: set[str]) -> None:
    if "Caveat" in seen_labels:
        return
    joined = "\n".join(metadata).lower()
    caveat: str | None = None
    if "private local review material" in joined or "private" in joined:
        caveat = "references/caveats/private-local-material.md"
    elif "requests for startups" in joined or "rfs" in joined:
        caveat = "references/caveats/yc-rfs-source.md"
    elif "official yc" in joined or "y combinator" in joined and "yc website" in joined:
        caveat = "references/caveats/official-yc-source.md"
    elif any(
        name in joined
        for name in (
            "paul graham",
            "jessica livingston",
            "sam altman",
            "garry tan",
            "michael seibel",
            "dalton caldwell",
            "jared friedman",
        )
    ):
        caveat = "references/caveats/yc-founder-partner-source.md"
    elif "founder anecdote" in joined or "founder story" in joined:
        caveat = "references/caveats/founder-story.md"

    if caveat:
        metadata.append(f"- Caveat: {caveat}")
        seen_labels.add("Caveat")


def metadata_labels(metadata: list[str]) -> set[str]:
    labels: set[str] = set()
    for line in metadata:
        if line.startswith("- ") and ":" in line:
            labels.add(line[2:].split(":", 1)[0].strip())
    return labels


def trim_blank_edges(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def unique_preserving_order(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for line in lines:
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(line)
    return unique


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT_DIR))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
