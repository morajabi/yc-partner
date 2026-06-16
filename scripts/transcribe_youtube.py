#!/usr/bin/env python3
"""Transcribe YouTube videos into processed Markdown resources.

The pipeline is caption-first:
1. Read YouTube metadata with yt-dlp.
2. Use manual captions when available.
3. Fall back to auto captions.
4. Fall back to downloaded audio + local faster-whisper.
5. Optionally fall back to OpenAI transcription when explicitly enabled.

Downloaded captions, audio, and Whisper model files are cached under .source/.
Only the processed Markdown transcript should be written into skills resources.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT_DIR / ".source"
YTDLP_CACHE_DIR = SOURCE_DIR / "yt-dlp-cache"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "skills" / "yc-partner" / "resources" / "yc-youtube"


@dataclass
class TranscriptSegment:
    start: float | None
    end: float | None
    text: str


@dataclass
class TranscriptResult:
    method: str
    language: str | None
    language_probability: float | None
    segments: list[TranscriptSegment]
    notes: list[str]


class TranscriptionError(RuntimeError):
    pass


def main() -> int:
    args = parse_args()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    for url in args.urls:
        try:
            transcribe_url(url, args)
        except Exception as exc:  # noqa: BLE001 - CLI should continue across URLs.
            failures.append(f"{url}: {exc}")
            print(f"ERROR: {url}: {exc}", file=sys.stderr)
            if not args.keep_going:
                break

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe one or more YouTube videos into processed Markdown."
    )
    parser.add_argument("urls", nargs="+", help="YouTube video URLs.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for processed Markdown output. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=SOURCE_DIR / "youtube",
        help="Directory for downloaded metadata, captions, and audio.",
    )
    parser.add_argument(
        "--model-cache-dir",
        type=Path,
        default=SOURCE_DIR / "whisper-models",
        help="Directory for cached local Whisper models.",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Preferred transcript language. Use 'auto' for Whisper language detection.",
    )
    parser.add_argument(
        "--model",
        default="small.en",
        help="faster-whisper model name for local audio fallback. Examples: base.en, small.en, medium.en.",
    )
    parser.add_argument(
        "--caption-mode",
        choices=["prefer", "only", "skip"],
        default="prefer",
        help="Use YouTube captions before audio fallback, only captions, or skip captions.",
    )
    parser.add_argument(
        "--allow-openai-fallback",
        action="store_true",
        help="If local transcription fails, use OpenAI transcription when OPENAI_API_KEY or OPENAI_TOKEN is available.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing Markdown output.",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue to the next URL when one video fails.",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=40,
        help="Treat transcripts shorter than this as failed and try the next fallback.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retries for yt-dlp network operations.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve metadata and choose output paths without downloading or writing transcripts.",
    )
    return parser.parse_args()


def transcribe_url(url: str, args: argparse.Namespace) -> None:
    metadata = load_metadata(url, args)
    video_id = require_video_id(metadata)
    cache_dir = args.cache_dir / video_id
    cache_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = cache_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    title = metadata.get("title") or video_id
    output_path = args.output_dir / f"{slugify(title)}-{video_id}.md"
    if output_path.exists() and not args.force:
        raise TranscriptionError(f"{output_path} already exists; pass --force to overwrite")

    print(f"\nVideo: {title}")
    print(f"ID: {video_id}")
    print(f"Output: {relative_to_root(output_path)}")

    if args.dry_run:
        return

    errors: list[str] = []
    result: TranscriptResult | None = None

    if args.caption_mode != "skip":
        for caption_kind in ("manual", "automatic"):
            try:
                result = try_caption_transcript(
                    url=url,
                    metadata=metadata,
                    video_id=video_id,
                    cache_dir=cache_dir,
                    language=args.language,
                    caption_kind=caption_kind,
                    retries=args.retries,
                    min_words=args.min_words,
                )
                if result:
                    break
            except Exception as exc:  # noqa: BLE001 - fallback chain should continue.
                errors.append(f"{caption_kind} captions failed: {exc}")
                print(f"Caption fallback note: {caption_kind} captions failed: {exc}", file=sys.stderr)

    if result is None and args.caption_mode != "only":
        try:
            audio_path = download_audio(url, video_id, cache_dir, args.retries)
            result = transcribe_with_faster_whisper(
                audio_path=audio_path,
                language=args.language,
                model_name=args.model,
                model_cache_dir=args.model_cache_dir,
                min_words=args.min_words,
            )
        except Exception as exc:  # noqa: BLE001 - optional OpenAI fallback can continue.
            errors.append(f"local faster-whisper failed: {exc}")
            print(f"Audio fallback note: local faster-whisper failed: {exc}", file=sys.stderr)

    if result is None and args.allow_openai_fallback:
        try:
            audio_path = find_cached_audio(cache_dir) or download_audio(url, video_id, cache_dir, args.retries)
            result = transcribe_with_openai(
                audio_path=audio_path,
                language=args.language,
                min_words=args.min_words,
            )
        except Exception as exc:  # noqa: BLE001 - final fallback should report all context.
            errors.append(f"OpenAI fallback failed: {exc}")
            print(f"Audio fallback note: OpenAI fallback failed: {exc}", file=sys.stderr)

    if result is None:
        detail = "; ".join(errors) if errors else "no transcript source found"
        raise TranscriptionError(detail)

    markdown = build_markdown(metadata, result, errors)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {relative_to_root(output_path)} via {result.method}")


def load_metadata(url: str, args: argparse.Namespace) -> dict[str, Any]:
    cmd = ytdlp_command(
        "--dump-single-json",
        "--skip-download",
        "--ignore-no-formats-error",
        "--no-check-formats",
        "--no-playlist",
        "--retries",
        str(args.retries),
        "--fragment-retries",
        str(args.retries),
        "--extractor-retries",
        str(args.retries),
        "--socket-timeout",
        "30",
        url,
    )
    completed = run(cmd, capture=True, retries=args.retries)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise TranscriptionError(f"yt-dlp returned invalid metadata JSON: {exc}") from exc


def require_video_id(metadata: dict[str, Any]) -> str:
    video_id = metadata.get("id")
    if not isinstance(video_id, str) or not video_id.strip():
        raise TranscriptionError("yt-dlp metadata did not include a video id")
    return video_id.strip()


def try_caption_transcript(
    *,
    url: str,
    metadata: dict[str, Any],
    video_id: str,
    cache_dir: Path,
    language: str,
    caption_kind: str,
    retries: int,
    min_words: int,
) -> TranscriptResult | None:
    subtitle_map_name = "subtitles" if caption_kind == "manual" else "automatic_captions"
    subtitle_map = metadata.get(subtitle_map_name) or {}
    chosen_language = choose_caption_language(subtitle_map, language)
    if chosen_language is None:
        return None

    caption_dir = cache_dir / "captions" / caption_kind
    caption_dir.mkdir(parents=True, exist_ok=True)
    before = set(caption_dir.glob("*"))

    caption_flag = "--write-subs" if caption_kind == "manual" else "--write-auto-subs"
    cmd = ytdlp_command(
        "--skip-download",
        "--ignore-no-formats-error",
        "--no-check-formats",
        caption_flag,
        "--sub-langs",
        chosen_language,
        "--sub-format",
        "vtt/srt/best",
        "--no-playlist",
        "--retries",
        str(retries),
        "--fragment-retries",
        str(retries),
        "--extractor-retries",
        str(retries),
        "-o",
        str(caption_dir / "%(id)s.%(ext)s"),
        url,
    )
    run(cmd, capture=True, retries=retries)

    candidates = sorted(
        [
            path
            for path in caption_dir.glob(f"{video_id}.*")
            if path not in before and path.suffix.lower() in {".vtt", ".srt"}
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        candidates = sorted(
            [
                path
                for path in caption_dir.glob(f"{video_id}.*")
                if path.suffix.lower() in {".vtt", ".srt"}
            ],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    if not candidates:
        raise TranscriptionError(f"yt-dlp did not write {caption_kind} captions for {chosen_language}")

    caption_path = candidates[0]
    segments = parse_caption_file(caption_path)
    validate_transcript(segments, min_words)
    return TranscriptResult(
        method=f"YouTube {caption_kind} captions ({caption_path.name})",
        language=chosen_language,
        language_probability=None,
        segments=segments,
        notes=[f"Caption file cached at {relative_to_root(caption_path)}."],
    )


def choose_caption_language(subtitle_map: dict[str, Any], preferred: str) -> str | None:
    if not subtitle_map:
        return None
    languages = list(subtitle_map.keys())
    if preferred == "auto":
        return languages[0]
    if preferred in subtitle_map:
        return preferred
    if preferred == "en":
        for candidate in ("en-US", "en-GB", "en-CA", "en-AU"):
            if candidate in subtitle_map:
                return candidate
    for candidate in languages:
        if candidate.lower().startswith(f"{preferred.lower()}-"):
            return candidate
    if preferred == "en":
        for candidate in languages:
            if candidate.lower().startswith("en"):
                return candidate
    return None


def download_audio(url: str, video_id: str, cache_dir: Path, retries: int) -> Path:
    audio_dir = cache_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    cached = find_cached_audio(cache_dir)
    if cached:
        print(f"Using cached audio: {relative_to_root(cached)}")
        return cached

    cmd = ytdlp_command(
        "--no-playlist",
        "--extract-audio",
        "--audio-format",
        "m4a",
        "--audio-quality",
        "0",
        "--retries",
        str(retries),
        "--fragment-retries",
        str(retries),
        "--extractor-retries",
        str(retries),
        "-o",
        str(audio_dir / "%(id)s.%(ext)s"),
        url,
    )
    run(cmd, capture=False, retries=retries)

    cached = find_cached_audio(cache_dir)
    if not cached:
        raise TranscriptionError("yt-dlp did not produce an audio file")
    return cached


def find_cached_audio(cache_dir: Path) -> Path | None:
    audio_dir = cache_dir / "audio"
    for suffix in (".m4a", ".mp3", ".opus", ".webm", ".wav"):
        matches = sorted(audio_dir.glob(f"*{suffix}"), key=lambda path: path.stat().st_mtime, reverse=True)
        if matches:
            return matches[0]
    return None


def transcribe_with_faster_whisper(
    *,
    audio_path: Path,
    language: str,
    model_name: str,
    model_cache_dir: Path,
    min_words: int,
) -> TranscriptResult:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise TranscriptionError(
            "faster-whisper is not installed. Run scripts/bootstrap-transcription.sh first."
        ) from exc

    model_cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"Running local Whisper model {model_name}; this can take a while on long videos.")
    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8",
        download_root=str(model_cache_dir),
    )
    language_arg = None if language == "auto" else language
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language_arg,
        vad_filter=True,
        beam_size=5,
        best_of=5,
    )
    segments = [
        TranscriptSegment(start=segment.start, end=segment.end, text=clean_text(segment.text))
        for segment in segments_iter
        if clean_text(segment.text)
    ]
    validate_transcript(segments, min_words)
    return TranscriptResult(
        method=f"local faster-whisper ({model_name})",
        language=getattr(info, "language", language_arg),
        language_probability=getattr(info, "language_probability", None),
        segments=segments,
        notes=[
            f"Audio cached at {relative_to_root(audio_path)}.",
            f"Model cache at {relative_to_root(model_cache_dir)}.",
        ],
    )


def transcribe_with_openai(*, audio_path: Path, language: str, min_words: int) -> TranscriptResult:
    load_dotenv_if_available()
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_TOKEN")
    if not api_key:
        raise TranscriptionError("OPENAI_API_KEY or OPENAI_TOKEN is not set")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise TranscriptionError("openai is not installed. Run scripts/bootstrap-transcription.sh first.") from exc

    client = OpenAI(api_key=api_key)
    language_arg = None if language == "auto" else language
    print("Running explicit OpenAI transcription fallback.")
    with audio_path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language_arg,
            response_format="verbose_json",
        )

    raw_segments = getattr(transcript, "segments", None) or []
    if raw_segments:
        segments = [
            TranscriptSegment(
                start=segment_start(segment),
                end=segment_end(segment),
                text=clean_text(segment_text(segment)),
            )
            for segment in raw_segments
        ]
        segments = [segment for segment in segments if segment.text]
    else:
        text = clean_text(getattr(transcript, "text", "") or str(transcript))
        segments = [TranscriptSegment(start=None, end=None, text=text)] if text else []

    validate_transcript(segments, min_words)
    return TranscriptResult(
        method="OpenAI transcription fallback (whisper-1)",
        language=language_arg,
        language_probability=None,
        segments=segments,
        notes=[f"Audio cached at {relative_to_root(audio_path)}."],
    )


def segment_start(segment: Any) -> float | None:
    value = segment.get("start") if isinstance(segment, dict) else getattr(segment, "start", None)
    return float(value) if value is not None else None


def segment_end(segment: Any) -> float | None:
    value = segment.get("end") if isinstance(segment, dict) else getattr(segment, "end", None)
    return float(value) if value is not None else None


def segment_text(segment: Any) -> str:
    return segment.get("text", "") if isinstance(segment, dict) else getattr(segment, "text", "")


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(ROOT_DIR / ".env", override=False)


def parse_caption_file(path: Path) -> list[TranscriptSegment]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".srt":
        return parse_srt(text)
    return parse_vtt(text)


def parse_vtt(text: str) -> list[TranscriptSegment]:
    segments: list[TranscriptSegment] = []
    lines = text.replace("\ufeff", "").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "-->" not in line:
            i += 1
            continue
        start, end = parse_timestamp_line(line)
        i += 1
        cue_lines: list[str] = []
        while i < len(lines) and lines[i].strip():
            cue_lines.append(lines[i].strip())
            i += 1
        text_line = clean_caption_text(" ".join(cue_lines))
        if text_line:
            segments.append(TranscriptSegment(start=start, end=end, text=text_line))
        i += 1
    return collapse_repeated_segments(segments)


def parse_srt(text: str) -> list[TranscriptSegment]:
    segments: list[TranscriptSegment] = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n"))
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        timestamp_index = next((idx for idx, line in enumerate(lines) if "-->" in line), None)
        if timestamp_index is None:
            continue
        start, end = parse_timestamp_line(lines[timestamp_index])
        text_line = clean_caption_text(" ".join(lines[timestamp_index + 1 :]))
        if text_line:
            segments.append(TranscriptSegment(start=start, end=end, text=text_line))
    return collapse_repeated_segments(segments)


def parse_timestamp_line(line: str) -> tuple[float | None, float | None]:
    left, right = line.split("-->", 1)
    return parse_timestamp(left.strip()), parse_timestamp(right.strip().split()[0])


def parse_timestamp(value: str) -> float | None:
    value = value.replace(",", ".")
    parts = value.split(":")
    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
    except ValueError:
        return None
    return None


def clean_caption_text(value: str) -> str:
    value = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", " ", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return clean_text(value)


def clean_text(value: str) -> str:
    value = value.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def collapse_repeated_segments(segments: list[TranscriptSegment]) -> list[TranscriptSegment]:
    collapsed: list[TranscriptSegment] = []
    previous_text = ""
    for segment in segments:
        text = segment.text
        if not text or text == previous_text:
            continue
        if previous_text and text.startswith(previous_text):
            text = text[len(previous_text) :].strip()
        if text:
            collapsed.append(TranscriptSegment(segment.start, segment.end, text))
            previous_text = segment.text
    return collapsed


def validate_transcript(segments: list[TranscriptSegment], min_words: int) -> None:
    words = count_words(" ".join(segment.text for segment in segments))
    if words < min_words:
        raise TranscriptionError(f"transcript has only {words} words; expected at least {min_words}")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def build_markdown(
    metadata: dict[str, Any],
    result: TranscriptResult,
    fallback_errors: list[str],
) -> str:
    title = metadata.get("title") or metadata.get("id") or "Untitled YouTube Video"
    url = metadata.get("webpage_url") or metadata.get("original_url") or ""
    author = metadata.get("channel") or metadata.get("uploader") or ""
    published = format_upload_date(metadata.get("upload_date") or metadata.get("release_date"))
    processed = dt.date.today().isoformat()
    source_status = infer_source_status(metadata)
    caveat = (
        "references/caveats/official-yc-source.md"
        if "Official YC" in source_status
        else "references/caveats/yc-founder-partner-source.md"
    )
    duration = format_duration(metadata.get("duration"))
    language_line = result.language or ""
    if result.language_probability is not None:
        language_line = f"{language_line} ({result.language_probability:.2%} probability)".strip()

    full_text = assemble_full_text(result.segments)
    timestamped = format_timestamped_segments(result.segments)

    summary_lines = [
        "- Full transcript preserved below.",
        f"- Transcript method: {result.method}; language: {language_line or 'unknown'}; duration: {duration or 'unknown'}; video ID: {metadata.get('id', '')}.",
    ]
    summary_lines.extend(f"- {note}" for note in result.notes)
    if fallback_errors:
        summary_lines.append("- Fallbacks before success: " + "; ".join(fallback_errors) + ".")

    summary_text = "\n".join(summary_lines)
    timestamped_section = f"\n\n### Timestamped Transcript\n\n{timestamped}\n" if timestamped else "\n"

    return f"""# {title}

- Type: YouTube transcript
- Status: {source_status}
- URL: {url}
- Author: {author}
- Published: {published}
- Captured: {processed}
- Method: {result.method}
- Caveat: {caveat}

## Summary

{summary_text}

## Transcript

{full_text}
{timestamped_section}
"""


def indent_bullets(text: str) -> str:
    return "\n".join(f"  {line}" if line else line for line in text.splitlines())


def assemble_full_text(segments: list[TranscriptSegment]) -> str:
    text = merge_segments_text(segments)
    return "\n\n".join(wrap_paragraphs(text))


def merge_segments_text(segments: list[TranscriptSegment]) -> str:
    merged = ""
    for segment in segments:
        merged = append_with_token_overlap(merged, segment.text)
    return clean_text(merged)


def append_with_token_overlap(existing: str, addition: str) -> str:
    addition = clean_text(addition)
    if not existing:
        return addition
    if not addition:
        return existing

    existing_tokens = existing.split()
    addition_tokens = addition.split()
    max_overlap = min(len(existing_tokens), len(addition_tokens), 30)
    overlap = 0
    for size in range(max_overlap, 0, -1):
        if existing_tokens[-size:] == addition_tokens[:size]:
            overlap = size
            break
    new_tokens = addition_tokens[overlap:]
    if not new_tokens:
        return existing
    separator = "" if existing.endswith((" ", "\n")) else " "
    return existing + separator + " ".join(new_tokens)


def wrap_paragraphs(text: str) -> list[str]:
    if not text:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs: list[str] = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current) + len(sentence) > 900 and current:
            paragraphs.append(textwrap.fill(current, width=100))
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        paragraphs.append(textwrap.fill(current, width=100))
    return paragraphs


def format_timestamped_segments(segments: list[TranscriptSegment]) -> str:
    lines: list[str] = []
    for segment in segments:
        if segment.start is None:
            continue
        lines.append(f"[{format_timestamp(segment.start)}] {segment.text}")
    return "\n".join(lines)


def format_timestamp(seconds: float) -> str:
    rounded = int(seconds)
    hours = rounded // 3600
    minutes = (rounded % 3600) // 60
    secs = rounded % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_upload_date(value: Any) -> str:
    if not value:
        return ""
    text = str(value)
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    return text


def format_duration(value: Any) -> str:
    try:
        seconds = int(value)
    except (TypeError, ValueError):
        return ""
    return format_timestamp(float(seconds))


def infer_source_status(metadata: dict[str, Any]) -> str:
    channel = (metadata.get("channel") or metadata.get("uploader") or "").lower()
    if "y combinator" in channel or channel == "yc":
        return "Official YC public source"
    return "Public YouTube source"


def slugify(value: str) -> str:
    value = value.lower()
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:90].strip("-") or "youtube-video"


def ytdlp_command(*args: str) -> list[str]:
    if importlib.util.find_spec("yt_dlp"):
        cmd = [sys.executable, "-m", "yt_dlp"]
    elif executable := shutil.which("yt-dlp"):
        cmd = [executable]
    else:
        raise TranscriptionError("yt-dlp is not installed. Run scripts/bootstrap-transcription.sh first.")

    ffmpeg_location = find_ffmpeg_location()
    if ffmpeg_location:
        cmd.extend(["--ffmpeg-location", ffmpeg_location])
    cmd.extend(["--cache-dir", str(YTDLP_CACHE_DIR)])
    js_runtime = find_js_runtime()
    if js_runtime:
        cmd.extend(["--js-runtimes", js_runtime, "--remote-components", "ejs:github"])
    cmd.append("--no-update")
    cmd.extend(args)
    return cmd


def find_ffmpeg_location() -> str | None:
    executable = shutil.which("ffmpeg")
    if executable:
        return str(Path(executable).parent)
    try:
        import imageio_ffmpeg
    except ImportError:
        return None
    return str(Path(imageio_ffmpeg.get_ffmpeg_exe()).parent)


def find_js_runtime() -> str | None:
    if deno := shutil.which("deno"):
        return f"deno:{deno}"
    if node := shutil.which("node"):
        return f"node:{node}"
    return None


def run(
    cmd: list[str],
    *,
    capture: bool,
    retries: int,
) -> subprocess.CompletedProcess[str]:
    last_error: subprocess.CalledProcessError | None = None
    attempts = max(1, retries)
    for attempt in range(1, attempts + 1):
        try:
            return subprocess.run(
                cmd,
                check=True,
                text=True,
                stdout=subprocess.PIPE if capture else None,
                stderr=subprocess.PIPE if capture else None,
            )
        except subprocess.CalledProcessError as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(min(2**attempt, 10))
                continue
            stderr = (exc.stderr or "").strip()
            detail = stderr[-1200:] if stderr else str(exc)
            raise TranscriptionError(detail) from exc
    raise TranscriptionError(str(last_error))


def relative_to_root(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT_DIR))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
