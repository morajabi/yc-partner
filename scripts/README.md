# Scripts

Put reusable processing scripts here.

Scripts should convert public source material into processed Markdown files under `skills/yc-partner/resources/`.

Do not write raw scraper output, downloaded media, private application data, credentials, or `.env` content into this repository.

## Resource Connection Audit

Use `audit_resource_connections.py` to find processed resource files that are not directly referenced by indexes, guides, references, `SKILL.md`, `AGENTS.md`, or the README.
It hides intentionally bulk-routed folders like RFS pages, GetIntoYC examples, Dalton/Michael imports, and the YC company directory unless `--show-bulk` is provided.

```sh
python3 scripts/audit_resource_connections.py
python3 scripts/audit_resource_connections.py --show-bulk
```

## YC Website Capture

Use `capture_yc_web_pages.py` to fetch public pages from `https://www.ycombinator.com` and convert their main content to processed Markdown with compact metadata.
The script refuses non-`www.ycombinator.com` URLs and writes to `skills/yc-partner/resources/yc-website/` by default.

```sh
python3 scripts/capture_yc_web_pages.py
python3 scripts/capture_yc_web_pages.py https://www.ycombinator.com/faq
```

## Paul Graham HTML Conversion

Use `convert_pg_html_to_markdown.py` to convert local Paul Graham essay HTML captures into processed Markdown files under `skills/yc-partner/resources/pg-essays/`.
It removes page chrome, scripts, images, and translation-link blocks, then writes compact metadata and normalized Markdown.

```sh
python3 scripts/convert_pg_html_to_markdown.py /path/to/paul-graham-*.html
```

The script contains an explicit filename-to-URL map for the currently supported local captures. Add to that map when importing more PG essays.

## Sam Altman Startup Playbook Capture

Use `capture_startup_playbook.py` to fetch the public single-page Startup Playbook and split it into one processed Markdown file per chapter under `skills/yc-partner/resources/yc-partners/startup-playbook/`.
The script uses only Python's standard library and does not persist raw HTML.

```sh
python3 scripts/capture_startup_playbook.py
python3 scripts/capture_startup_playbook.py --output-dir skills/yc-partner/resources/yc-partners/startup-playbook
```

## YC-Affiliated Partner Blog Capture

Use `capture_partner_blog_pages.py` to fetch supported public blog pages from YC-affiliated partners and write processed Markdown files under `skills/yc-partner/resources/yc-partners/`.
The script currently supports `blog.samaltman.com` and `www.michaelseibel.com`, uses only Python's standard library, and does not persist raw HTML.

```sh
python3 scripts/capture_partner_blog_pages.py
python3 scripts/capture_partner_blog_pages.py https://blog.samaltman.com/applying-to-yc
```

## Get into YC Example Application Capture

Use `capture_getintoyc_examples.py` to fetch public example applications from `https://getintoyc.com/`.
The script writes only applications labeled `Successful` into `skills/yc-partner/resources/examples/getintoyc/`, and writes eval fixtures for both successful and unsuccessful applications into `evals/yc-application-review/fixtures.jsonl`.
It uses only Python's standard library and does not persist raw HTML.

```sh
python3 scripts/capture_getintoyc_examples.py
```

## Lago YC Application Capture

Use `capture_lago_yc_application.py` to fetch Lago's public blog post with the application that got them into YC, write `skills/yc-partner/resources/examples/lago-yc-application.md`, and upsert the successful eval fixture `getlago-lago` into `evals/yc-application-review/fixtures.jsonl`.

```sh
python3 scripts/capture_lago_yc_application.py
```

## YC Company Directory Capture

Use `capture_yc_company_directory.py` to fetch the public YC company directory from `https://www.ycombinator.com/companies`.
The script writes normalized company records into `skills/yc-partner/resources/yc-company-directory/`, then derives group partner profiles from public `primary_group_partner` fields on individual company pages.
It uses only Python's standard library and does not persist raw HTML.

```sh
python3 scripts/capture_yc_company_directory.py
python3 scripts/capture_yc_company_directory.py --skip-page-enrichment
```

## YouTube json3 Caption Conversion

Prefer `transcribe_youtube.py` for live YouTube URLs. Use `convert_youtube_json3_to_markdown.py` only when you already have downloaded public `.json3` caption files that need offline conversion into Markdown.

```sh
python3 scripts/convert_youtube_json3_to_markdown.py /path/to/*.json3
```

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
