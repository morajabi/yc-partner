# Scripts

Put reusable processing scripts here.

Scripts should convert public source material into processed Markdown files under `skills/yc-partner/resources/`.

Do not write raw scraper output, downloaded media, private application data, credentials, or `.env` content into this repository.

## YouTube Transcription

Use `transcribe_youtube.py` to convert public YouTube videos into processed Markdown resource files.
It prefers manual YouTube captions, then automatic captions, then falls back to downloaded audio and local Whisper transcription.
Large downloaded inputs, model files, pip downloads, and yt-dlp extractor cache files are cached under `.source/`, which is ignored by git.
When Node or Deno is available, the script lets yt-dlp use it for YouTube JavaScript challenge solving and caches yt-dlp's remote EJS component under `.source/yt-dlp-cache`.

Install the Python tools into the ignored local environment:

```sh
scripts/bootstrap-transcription.sh
```

Run a transcription:

```sh
.source/venv/bin/python scripts/transcribe_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Useful options:

```sh
.source/venv/bin/python scripts/transcribe_youtube.py --output-dir skills/yc-partner/resources/dalton-michael "https://www.youtube.com/watch?v=VIDEO_ID"
.source/venv/bin/python scripts/transcribe_youtube.py --caption-mode skip --model medium.en "https://www.youtube.com/watch?v=VIDEO_ID"
.source/venv/bin/python scripts/transcribe_youtube.py --allow-openai-fallback "https://www.youtube.com/watch?v=VIDEO_ID"
```
