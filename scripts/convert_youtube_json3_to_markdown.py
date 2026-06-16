#!/usr/bin/env python3
"""Convert downloaded YouTube json3 captions into Markdown transcripts."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "skills" / "yc-partner" / "resources" / "yc-youtube"

VIDEO_METADATA = {
    "B246K_G7mHU": {
        "title": "Inside YC's AI Playbook",
        "channel": "Y Combinator",
        "duration": "46:30",
        "published": "2026-05-27",
    },
    "X_JsIHUfUjc": {
        "title": "How to Build a Self-Improving Company with AI",
        "channel": "Y Combinator",
        "duration": "13:28",
        "published": "2026-05-21",
    },
}


@dataclass(frozen=True)
class CaptionEvent:
    start_ms: int
    text: str


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str, fallback: str) -> str:
    value = html.unescape(value)
    value = value.replace("&", " and ")
    value = re.sub(r"[^\w\s.-]+", "", value, flags=re.ASCII)
    value = re.sub(r"\s+", "-", value.strip().lower())
    value = re.sub(r"-+", "-", value).strip("-.")
    return value[:110] or fallback


def read_events(path: Path) -> list[CaptionEvent]:
    data = json.loads(path.read_text(encoding="utf-8"))
    events: list[CaptionEvent] = []
    last_text = ""

    for event in data.get("events", []):
        segments = event.get("segs") or []
        text = normalize_space(
            "".join(segment.get("utf8", "") for segment in segments)
        )
        if not text or text == "\n":
            continue
        if text == last_text:
            continue
        events.append(CaptionEvent(start_ms=int(event.get("tStartMs", 0)), text=text))
        last_text = text

    return events


def event_text(events: Iterable[CaptionEvent]) -> str:
    pieces: list[str] = []
    for event in events:
        text = event.text
        if not text:
            continue

        if pieces:
            previous = pieces[-1]
            if previous and previous[-1] not in " ([/" and text[0] not in ".,:;!?)]":
                pieces.append(" ")
        pieces.append(text)

    text = normalize_space("".join(pieces))
    text = re.sub(r"\s+([.,:;!?])", r"\1", text)
    return text


def paragraphize(text: str, max_chars: int = 950) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if current and current_len + len(sentence) > max_chars:
            paragraphs.append(" ".join(current))
            current = []
            current_len = 0
        current.append(sentence)
        current_len += len(sentence) + 1

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs


def video_id_from_path(path: Path) -> str:
    match = re.search(r"([A-Za-z0-9_-]{11})", path.name)
    if match:
        return match.group(1)
    match = re.search(r"([A-Za-z0-9_-]{11})", str(path))
    if match:
        return match.group(1)
    raise ValueError(f"Could not infer YouTube video ID from {path}")


def output_path_for(video_id: str, title: str, output_dir: Path) -> Path:
    return output_dir / f"youtube-{slug(title, video_id)}-{video_id}.md"


def render_markdown(path: Path, captured_on: dt.date) -> tuple[Path, str]:
    video_id = video_id_from_path(path)
    metadata = VIDEO_METADATA.get(video_id, {})
    title = metadata.get("title", video_id)
    channel = metadata.get("channel", "Unknown")
    duration = metadata.get("duration", "Unknown")
    published = metadata.get("published", "Unknown")
    official_url = f"https://www.youtube.com/watch?v={video_id}"
    events = read_events(path)
    text = event_text(events)
    paragraphs = paragraphize(text)

    body = [
        f"# {title}",
        "",
        "- Type: Official YC YouTube video transcript",
        "- Status: Official YC public source",
        f"- URL: {official_url}",
        f"- Author: {channel}",
        f"- Published: {published}",
        f"- Captured: {captured_on.isoformat()}",
        "- Method: YouTube `en-orig` auto-generated captions via `scripts/convert_youtube_json3_to_markdown.py`",
        "- Caveat: references/caveats/official-yc-source.md",
        "",
        "## Summary",
        "",
        f"- Full transcript preserved below. Video ID: {video_id}; duration: {duration}.",
        "",
        "## Transcript",
        "",
        "\n\n".join(paragraphs) if paragraphs else "_No transcript text extracted._",
        "",
    ]
    return output_path_for(video_id, title, Path()), "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("caption_files", nargs="+", type=Path)
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        type=Path,
        help="Directory for generated Markdown transcript files.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    captured_on = dt.datetime.now(dt.timezone.utc).date()

    for caption_file in args.caption_files:
        relative_output, markdown = render_markdown(caption_file, captured_on)
        output_path = args.output_dir / relative_output.name
        output_path.write_text(markdown, encoding="utf-8")
        print(output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
