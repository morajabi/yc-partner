#!/usr/bin/env python3
"""Capture Social Radars transcript PDFs as processed Markdown."""

from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - CLI dependency check.
    raise SystemExit("pypdf is required. Install it in an ignored venv, e.g. `.source/social-radars-venv/bin/python -m pip install pypdf`.") from exc


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.thesocialradars.com"
EPISODES_URL = f"{SITE}/episodes"
DEFAULT_OUTPUT_DIR = ROOT / "skills" / "yc-partner" / "resources" / "social-radars"
DEFAULT_CACHE_DIR = ROOT / ".source" / "social-radars-transcripts"

OUTPUT_OVERRIDES = {
    "adora-cheung": "adora-cheung-co-founder-of-homejoy-instalab.md",
    "bill-clerico": "bill-clerico-co-founder-ceo-of-wepay.md",
    "brian-armstrong": "brian-armstrong-co-founder-and-ceo-of-coinbase.md",
    "brian-chesky-s1": "brian-chesky-co-founder-ceo-of-airbnb.md",
    "brian-chesky-s2": "brian-chesky-co-founder-ceo-of-airbnb-part-ii.md",
    "david-lieb": "david-lieb-creator-of-google-photos.md",
    "dimitri-dadiomov": "dimitri-dadiomov-co-founder-ceo-of-modern-treasury.md",
    "edith-elliott": "edith-elliott-co-founder-ceo-of-noora-health.md",
    "emmett-shear-s2": "emmett-shear-co-founder-of-twitch.md",
    "garry-tan-s1": "garry-tan-president-and-ceo-of-y-combinator.md",
    "parker-conrad": "parker-conrad-founder-of-zenefits-rippling.md",
    "patrick-john-collison": "patrick-john-collison-co-founders-of-stripe.md",
    "paul-buchheit": "paul-buchheit-creator-of-gmail.md",
    "paul-graham-s1": "paul-graham-co-founder-of-y-combinator-and-viaweb.md",
    "steve-huffman": "steve-huffman-co-founder-ceo-of-reddit.md",
    "tony-xu": "tony-xu-co-founder-ceo-of-doordash.md",
    "tracy-young": "tracy-young-co-founder-ceo-of-plangrid.md",
    "trevor-blackwell": "trevor-blackwell-co-founder-y-combinator-founder-anybots.md",
    "yuri-sagalov": "yuri-sagalov-co-founder-of-aerofs.md",
}


@dataclass(frozen=True)
class Episode:
    id: str
    name: str
    title: str
    description: str
    season: str
    date: str
    duration: str
    audio_url: str
    transcript_url: str


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def asset_url() -> str:
    html = fetch_text(EPISODES_URL)
    match = re.search(r'<script[^>]+src="([^"]+index-[^"]+\.js)"', html)
    if not match:
        raise RuntimeError("could not find Social Radars app JS asset")
    return urljoin(SITE, match.group(1))


def split_object_chunks(js: str) -> list[str]:
    start = js.find('{id:"')
    if start < 0:
        return []
    tail = js[start:]
    chunks = re.split(r'\},\{id:"', tail)
    output = []
    for idx, chunk in enumerate(chunks):
        if idx:
            chunk = '{id:"' + chunk
        else:
            chunk = chunk if chunk.startswith("{") else "{" + chunk
        end = chunk.find("}")
        if end >= 0:
            chunk = chunk[: end + 1]
        output.append(chunk)
    return output


def js_string(chunk: str, field: str) -> str:
    match = re.search(rf'{field}:"((?:\\.|[^"\\])*)"', chunk)
    if not match:
        return ""
    return unescape_js_string(match.group(1))


def unescape_js_string(value: str) -> str:
    value = value.replace(r"\"", '"').replace(r"\'", "'")
    value = value.replace(r"\n", "\n").replace(r"\u0026", "&")
    return value


def discover_episodes() -> list[Episode]:
    js = fetch_text(asset_url())
    episodes = []
    for chunk in split_object_chunks(js):
        if "hasTranscript:!0" not in chunk or "transcriptUrl:" not in chunk:
            continue
        episode_id = js_string(chunk, "id")
        transcript_url = js_string(chunk, "transcriptUrl")
        if not episode_id or not transcript_url:
            continue
        episodes.append(
            Episode(
                id=episode_id,
                name=js_string(chunk, "name"),
                title=js_string(chunk, "title") or js_string(chunk, "name"),
                description=js_string(chunk, "description"),
                season=js_string(chunk, "season") or "Unknown",
                date=js_string(chunk, "date") or "Unknown",
                duration=js_string(chunk, "duration") or "Unknown",
                audio_url=js_string(chunk, "audioUrl"),
                transcript_url=urljoin(SITE, transcript_url),
            )
        )
    return episodes


def slugify(value: str) -> str:
    value = value.lower()
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:90].strip("-") or "social-radars-episode"


def output_name(episode: Episode) -> str:
    return OUTPUT_OVERRIDES.get(episode.id) or f"{slugify(episode.title)}.md"


def download_pdf(episode: Episode, cache_dir: Path, force: bool) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{episode.id}.pdf"
    if path.exists() and not force:
        return path
    request = Request(episode.transcript_url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
    if not data.startswith(b"%PDF"):
        raise RuntimeError(f"not a PDF response for {episode.transcript_url}")
    path.write_bytes(data)
    return path


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text(extraction_mode="layout") or "")
        except TypeError:
            pages.append(page.extract_text() or "")
    text = "\n".join(pages)
    text = text.replace("\uf0b7", "-")
    text = re.sub(r"\n?Transcript by Rev\.com\n?", "\n", text)
    text = re.sub(r"\n?Page \d+ of \d+\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return normalize_transcript_text(text)


def normalize_transcript_text(text: str) -> str:
    entries: list[str] = []
    current = ""
    current_speaker = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "The Social Radars" or line.startswith("Released "):
            continue
        if line.startswith("TSR_") or re.fullmatch(r"Page \d+ of \d+", line):
            continue
        collapsed = re.sub(r"\s{2,}", " ", raw_line).strip()
        if not collapsed:
            continue

        match = re.match(r"^([A-Za-z][A-Za-z .&'-]{0,40}):\s+(\d{2}:\d{2}:\d{2})\s*(.*)$", collapsed)
        if match:
            if current:
                entries.append(current.strip())
            current_speaker = match.group(1).strip()
            current = f"{current_speaker} ({match.group(2)}): {match.group(3).strip()}".rstrip()
            continue

        match = re.match(r"^(\d{2}:\d{2}:\d{2})\s+(.*)$", collapsed)
        if match:
            if current:
                entries.append(current.strip())
            speaker = current_speaker or "Speaker"
            current = f"{speaker} ({match.group(1)}): {match.group(2).strip()}".rstrip()
            continue

        if current:
            current = f"{current} {collapsed}".strip()
        else:
            current = collapsed

    if current:
        entries.append(current.strip())
    return "\n\n".join(entries).strip()


def released_date_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    try:
        first_page = reader.pages[0].extract_text(extraction_mode="layout") or ""
    except TypeError:
        first_page = reader.pages[0].extract_text() or ""
    match = re.search(r"Released\s+([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})", first_page)
    return match.group(1) if match else "Unknown"


def wrapped_transcript(text: str) -> str:
    blocks = []
    for para in re.split(r"\n\s*\n", text):
        para = re.sub(r"[ \t]+", " ", para).strip()
        if not para:
            continue
        blocks.append(textwrap.fill(para, width=100))
    return "\n\n".join(blocks)


def markdown(episode: Episode, transcript_text: str, published: str) -> str:
    summary = [
        f"Full public Social Radars transcript captured from the episode transcript PDF.",
        f"Episode page: {EPISODES_URL}.",
        f"Audio/listen URL: {episode.audio_url or 'Unknown'}.",
        f"Season: {episode.season}; duration: {episode.duration}; listed date: {episode.date}.",
    ]
    if episode.description:
        summary.append(f"Site description: {episode.description}")
    return "\n".join(
        [
            f"# {episode.title}",
            "",
            "- Type: Social Radars podcast transcript",
            "- Status: YC-affiliated public podcast transcript",
            f"- URL: {episode.transcript_url}",
            "- Author: The Social Radars",
            f"- Published: {published}",
            f"- Captured: {date.today().isoformat()}",
            "- Method: scripts/capture_social_radars_transcripts.py transcript PDF extraction",
            "- Caveat: references/caveats/yc-founder-partner-source.md",
            "",
            "## Summary",
            "",
            *[f"- {item}" for item in summary],
            "",
            "## Transcript",
            "",
            wrapped_transcript(transcript_text),
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="*", help="Optional Social Radars episode IDs. Defaults to all transcript-bearing episodes.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    episodes = discover_episodes()
    if args.ids:
        wanted = set(args.ids)
        episodes = [episode for episode in episodes if episode.id in wanted]
        missing = wanted - {episode.id for episode in episodes}
        if missing:
            raise SystemExit(f"episode IDs not found or no transcript URL: {', '.join(sorted(missing))}")

    failures = []
    for episode in episodes:
        try:
            pdf_path = download_pdf(episode, args.cache_dir, args.force_download)
            transcript = extract_pdf_text(pdf_path)
            if len(transcript.split()) < 100:
                raise RuntimeError("extracted transcript is too short")
            published = episode.date if episode.date != "Unknown" else released_date_from_pdf(pdf_path)
            output = args.output_dir / output_name(episode)
            if args.dry_run:
                print(f"--- {output.relative_to(ROOT)} ({len(transcript.split())} words)")
                continue
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(markdown(episode, transcript, published), encoding="utf-8")
            print(f"{output.relative_to(ROOT)} ({len(transcript.split())} words)")
        except Exception as exc:  # noqa: BLE001 - capture should continue across public PDFs.
            failures.append(f"{episode.id}: {exc}")
            print(f"ERROR {episode.id}: {exc}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
