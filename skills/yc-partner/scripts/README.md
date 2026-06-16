# YC Partner Agent Runtime Scripts

These scripts are internal helpers for agents using the installed YC Partner skill with a founder's private application material. The skill should run them on the user's behalf; founders should not need to know the command-line details.

Do not commit generated transcripts, extracted audio, `.env` files, or founder-provided videos to this repository.

## Transcribe Founder And Demo Videos

`transcribe-videos.mjs` extracts audio from founder/demo videos with `ffmpeg`, sends only the derived audio to OpenAI's audio transcription API, and writes private Markdown transcripts for YC Partner analysis.

Ask the user only for local video paths and an `OPENAI_TOKEN` made available in their local environment. Do not ask them to paste the token into chat. The helper reads `OPENAI_TOKEN` from the current working directory's `.env` file or from the shell environment.

Agent-owned command shape:

```sh
node /path/to/yc-partner/skills/yc-partner/scripts/transcribe-videos.mjs \
  --founder founder-video.mp4 \
  --demo demo-video.mov
```

Run it from the directory that contains the founder's application draft and private `.env` file, not from the skill repository.

The helper expects:

- `OPENAI_TOKEN` in `.env` in the current working directory, or exported in the shell environment.
- `ffmpeg` installed and available on `PATH`.
- Video files readable from the current working directory.

By default it writes ignored private output under:

- `.yc-partner/audio/` for extracted audio.
- `.yc-partner/chunks/` for split audio when a file exceeds the OpenAI upload limit.
- `.yc-partner/transcripts/` for Markdown transcripts.

The script creates `.yc-partner/.gitignore` so generated private outputs are not committed accidentally. It never prints the token or `.env` contents. It emits `[info]`, `[warn]`, and `[error]` logs for the agent to translate into concise user-facing status or next steps.

Useful internal options:

```sh
node /path/to/yc-partner/skills/yc-partner/scripts/transcribe-videos.mjs \
  --founder founder-video.mp4 \
  --demo demo-video.mov \
  --language en \
  --audio-bitrate 48k \
  --chunk-seconds 600
```

After transcription, pass the generated transcript paths to YC Partner with the application draft.
