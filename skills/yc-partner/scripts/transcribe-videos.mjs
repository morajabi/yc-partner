#!/usr/bin/env node

import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import { basename, extname, isAbsolute, join, relative, resolve } from "node:path";

const MAX_UPLOAD_BYTES = 25 * 1024 * 1024;
const DEFAULT_MODEL = "gpt-4o-transcribe";
const DEFAULT_OUT_DIR = ".yc-partner";
const DEFAULT_AUDIO_BITRATE = "48k";
const DEFAULT_CHUNK_SECONDS = 600;
const TRANSCRIPT_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions";

const DEFAULT_PROMPT =
  "This is a Y Combinator application video. Preserve startup names, product names, metrics, technical terms, user segments, and founder names as accurately as possible.";

const MIME_TYPES = new Map([
  [".mp3", "audio/mpeg"],
  [".mp4", "video/mp4"],
  [".mpeg", "audio/mpeg"],
  [".mpga", "audio/mpeg"],
  [".m4a", "audio/mp4"],
  [".wav", "audio/wav"],
  [".webm", "audio/webm"],
]);

main().catch((error) => {
  logError(error.message);
  process.exitCode = 1;
});

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    return;
  }

  if (args.inputs.length === 0) {
    printHelp();
    throw new Error("Pass at least one --founder, --demo, or --video file.");
  }

  const cwd = process.cwd();
  const outRoot = resolve(cwd, args.outDir);
  const outRelative = relative(cwd, outRoot);
  if (!outRelative || outRelative.startsWith("..") || isAbsolute(outRelative)) {
    throw new Error("--out must point to a subdirectory inside the current directory.");
  }

  const audioDir = join(outRoot, "audio");
  const chunkDir = join(outRoot, "chunks");
  const transcriptDir = join(outRoot, "transcripts");

  await validateInputFiles(cwd, args.inputs);
  await ensureFfmpeg();
  await preparePrivateOutputDir(outRoot, audioDir, chunkDir, transcriptDir);

  let token;
  const getToken = async () => {
    token ??= await loadOpenAIToken(cwd);
    return token;
  };

  const written = [];
  for (const input of args.inputs) {
    const result = await transcribeVideo({
      cwd,
      input,
      getToken,
      model: args.model,
      language: args.language,
      prompt: args.prompt,
      audioBitrate: args.audioBitrate,
      chunkSeconds: args.chunkSeconds,
      force: args.force,
      audioDir,
      chunkDir,
      transcriptDir,
    });
    written.push(result.transcriptPath);
  }

  console.log("");
  logInfo("Wrote private transcript files:");
  for (const filePath of written) {
    console.log(`- ${relative(cwd, filePath)}`);
  }
}

async function validateInputFiles(cwd, inputs) {
  for (const input of inputs) {
    const sourcePath = resolve(cwd, input.path);
    if (!existsSync(sourcePath)) {
      throw new Error(`File not found: ${input.path}`);
    }

    const sourceStats = await stat(sourcePath);
    if (!sourceStats.isFile()) {
      throw new Error(`Not a file: ${input.path}`);
    }
  }
}

async function transcribeVideo(options) {
  const {
    cwd,
    input,
    getToken,
    model,
    language,
    prompt,
    audioBitrate,
    chunkSeconds,
    force,
    audioDir,
    chunkDir,
    transcriptDir,
  } = options;

  const sourcePath = resolve(cwd, input.path);
  if (!existsSync(sourcePath)) {
    throw new Error(`File not found: ${input.path}`);
  }

  const sourceStats = await stat(sourcePath);
  if (!sourceStats.isFile()) {
    throw new Error(`Not a file: ${input.path}`);
  }

  const baseName = safeStem(sourcePath);
  const label = input.kind === "founder" ? "founder-video" : input.kind === "demo" ? "demo-video" : "video";
  const audioPath = join(audioDir, `${baseName}.m4a`);
  const transcriptPath = join(transcriptDir, `${baseName}.${label}.transcript.md`);

  console.log("");
  logInfo(`Extracting audio: ${relative(cwd, sourcePath)}`);
  if (force || !existsSync(audioPath)) {
    await run("ffmpeg", [
      "-hide_banner",
      "-loglevel",
      "error",
      "-y",
      "-i",
      sourcePath,
      "-vn",
      "-ac",
      "1",
      "-ar",
      "16000",
      "-c:a",
      "aac",
      "-b:a",
      audioBitrate,
      audioPath,
    ]);
  } else {
    logInfo(`Using existing audio: ${relative(cwd, audioPath)}`);
  }

  const audioFiles = await uploadableAudioFiles({
    cwd,
    sourceAudioPath: audioPath,
    chunkDir,
    baseName,
    audioBitrate,
    chunkSeconds,
    force,
  });

  const transcriptParts = [];
  let previousText = "";
  const token = await getToken();
  for (let index = 0; index < audioFiles.length; index += 1) {
    const audioFile = audioFiles[index];
    const partLabel = audioFiles.length === 1 ? "audio" : `chunk ${index + 1}/${audioFiles.length}`;
    logInfo(`Transcribing ${partLabel}: ${relative(cwd, audioFile)}`);

    const text = await transcribeAudioFile({
      token,
      model,
      language,
      prompt: promptWithContext(prompt, previousText),
      audioPath: audioFile,
    });

    transcriptParts.push(text.trim());
    previousText = text.trim();
  }

  const transcript = transcriptParts.filter(Boolean).join("\n\n");
  if (!transcript) {
    logWarn(`No speech was detected for ${relative(cwd, sourcePath)}.`);
  }

  const markdown = buildTranscriptMarkdown({
    kind: input.kind,
    sourcePath,
    audioPath,
    audioFiles,
    transcript,
    model,
    language,
    prompt,
    cwd,
  });

  await writeFile(transcriptPath, markdown, "utf8");
  return { transcriptPath };
}

async function uploadableAudioFiles(options) {
  const { cwd, sourceAudioPath, chunkDir, baseName, audioBitrate, chunkSeconds, force } = options;
  const sourceStats = await stat(sourceAudioPath);

  if (sourceStats.size < MAX_UPLOAD_BYTES) {
    return [sourceAudioPath];
  }

  const fileChunkDir = force ? join(chunkDir, `${baseName}-${Date.now()}`) : join(chunkDir, baseName);
  await mkdir(fileChunkDir, { recursive: true });

  const existingChunks = await listM4aFiles(fileChunkDir);
  if (force || existingChunks.length === 0) {
    logWarn(
      `Audio is ${formatBytes(sourceStats.size)}, above OpenAI's 25 MB upload limit; splitting into ${chunkSeconds}s chunks.`,
    );

    await run("ffmpeg", [
      "-hide_banner",
      "-loglevel",
      "error",
      "-y",
      "-i",
      sourceAudioPath,
      "-f",
      "segment",
      "-segment_time",
      String(chunkSeconds),
      "-reset_timestamps",
      "1",
      "-vn",
      "-ac",
      "1",
      "-ar",
      "16000",
      "-c:a",
      "aac",
      "-b:a",
      audioBitrate,
      join(fileChunkDir, "chunk-%03d.m4a"),
    ]);
  }

  const chunks = await listM4aFiles(fileChunkDir);
  if (chunks.length === 0) {
    throw new Error("Audio exceeded the upload limit, but no chunks were produced.");
  }

  for (const chunk of chunks) {
    const chunkStats = await stat(chunk);
    if (chunkStats.size >= MAX_UPLOAD_BYTES) {
      throw new Error(
        `${relative(cwd, chunk)} is ${formatBytes(chunkStats.size)}, still above 25 MB. Try --audio-bitrate 24k or --chunk-seconds 300.`,
      );
    }
  }

  return chunks;
}

async function transcribeAudioFile({ token, model, language, prompt, audioPath }) {
  const extension = extname(audioPath).toLowerCase();
  const bytes = await readFile(audioPath);
  const form = new FormData();

  form.set("model", model);
  form.set("response_format", "json");
  if (language) {
    form.set("language", language);
  }
  if (prompt) {
    form.set("prompt", prompt);
  }

  form.set("file", new Blob([bytes], { type: MIME_TYPES.get(extension) ?? "application/octet-stream" }), basename(audioPath));

  const response = await fetch(TRANSCRIPT_ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: form,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`OpenAI transcription failed (${response.status}): ${redactLikelySecrets(body)}`);
  }

  const json = await response.json();
  if (!json || typeof json.text !== "string") {
    throw new Error("OpenAI transcription response did not include a text field.");
  }

  return json.text;
}

function buildTranscriptMarkdown(options) {
  const { kind, sourcePath, audioPath, audioFiles, transcript, model, language, prompt, cwd } = options;
  const title = kind === "founder" ? "Founder Video Transcript" : kind === "demo" ? "Demo Video Transcript" : "Video Transcript";
  const processedDate = new Date().toISOString();
  const uploadedAudio =
    audioFiles.length === 1
      ? relative(cwd, audioFiles[0])
      : audioFiles.map((filePath) => relative(cwd, filePath)).join(", ");

  return `# ${title}

- Type: private ${kind} video transcript
- Status: private local review material
- Source: \`${relative(cwd, sourcePath)}\`
- Captured: ${processedDate}
- Method: ffmpeg audio extraction, then OpenAI audio transcription; model \`${model}\`; language \`${language ?? "auto"}\`
- Caveat: references/caveats/private-local-material.md

## Summary

- Keep this transcript out of public repositories unless the founder explicitly chooses to publish it.
- Extracted audio: \`${relative(cwd, audioPath)}\`
- Uploaded audio: \`${uploadedAudio}\`
- Prompt: ${prompt ? yamlString(prompt) : "none"}

## Transcript

${transcript || "_No speech detected._"}
`;
}

async function loadOpenAIToken(cwd) {
  if (process.env.OPENAI_TOKEN) {
    return process.env.OPENAI_TOKEN;
  }

  const envPath = join(cwd, ".env");
  if (!existsSync(envPath)) {
    throw new Error("Missing OPENAI_TOKEN. Add it to .env in the current directory or export it before running this script.");
  }

  const envText = await readFile(envPath, "utf8");
  const env = parseDotEnv(envText);
  if (!env.OPENAI_TOKEN) {
    throw new Error("Missing OPENAI_TOKEN in the current directory's .env file.");
  }

  return env.OPENAI_TOKEN;
}

function parseDotEnv(text) {
  const result = {};

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const normalized = line.startsWith("export ") ? line.slice("export ".length).trim() : line;
    const equalsIndex = normalized.indexOf("=");
    if (equalsIndex === -1) {
      continue;
    }

    const key = normalized.slice(0, equalsIndex).trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)) {
      continue;
    }

    let value = normalized.slice(equalsIndex + 1).trim();
    const quote = value[0];
    if ((quote === "\"" || quote === "'") && value.endsWith(quote)) {
      value = value.slice(1, -1);
    } else {
      const commentIndex = value.search(/\s#/);
      if (commentIndex !== -1) {
        value = value.slice(0, commentIndex).trim();
      }
    }

    result[key] = value;
  }

  return result;
}

async function preparePrivateOutputDir(outRoot, audioDir, chunkDir, transcriptDir) {
  await mkdir(audioDir, { recursive: true });
  await mkdir(chunkDir, { recursive: true });
  await mkdir(transcriptDir, { recursive: true });

  const gitignorePath = join(outRoot, ".gitignore");
  if (!existsSync(gitignorePath)) {
    await writeFile(gitignorePath, "*\n!.gitignore\n", "utf8");
  }
}

async function ensureFfmpeg() {
  try {
    await run("ffmpeg", ["-version"], { quiet: true });
  } catch {
    throw new Error("ffmpeg is required to extract audio before transcription. Install ffmpeg and try again.");
  }
}

function run(command, args, options = {}) {
  return new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(command, args, {
      stdio: options.quiet ? ["ignore", "ignore", "pipe"] : ["ignore", "inherit", "pipe"],
    });

    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("error", rejectPromise);
    child.on("close", (code) => {
      if (code === 0) {
        resolvePromise();
        return;
      }

      rejectPromise(new Error(`${command} exited with ${code}${stderr ? `: ${stderr.trim()}` : ""}`));
    });
  });
}

async function listM4aFiles(dirPath) {
  if (!existsSync(dirPath)) {
    return [];
  }

  const names = await readdir(dirPath);
  return names
    .filter((name) => name.endsWith(".m4a"))
    .sort()
    .map((name) => join(dirPath, name));
}

function parseArgs(argv) {
  const args = {
    inputs: [],
    outDir: DEFAULT_OUT_DIR,
    model: DEFAULT_MODEL,
    language: undefined,
    prompt: DEFAULT_PROMPT,
    audioBitrate: DEFAULT_AUDIO_BITRATE,
    chunkSeconds: DEFAULT_CHUNK_SECONDS,
    force: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    switch (arg) {
      case "--founder":
        args.inputs.push({ kind: "founder", path: requireValue(argv, ++index, arg) });
        break;
      case "--demo":
        args.inputs.push({ kind: "demo", path: requireValue(argv, ++index, arg) });
        break;
      case "--video":
        args.inputs.push({ kind: "video", path: requireValue(argv, ++index, arg) });
        break;
      case "--out":
        args.outDir = requireValue(argv, ++index, arg);
        break;
      case "--model":
        args.model = requireValue(argv, ++index, arg);
        break;
      case "--language":
        args.language = requireValue(argv, ++index, arg);
        break;
      case "--prompt":
        args.prompt = requireValue(argv, ++index, arg);
        break;
      case "--no-prompt":
        args.prompt = undefined;
        break;
      case "--audio-bitrate":
        args.audioBitrate = requireValue(argv, ++index, arg);
        break;
      case "--chunk-seconds":
        args.chunkSeconds = Number.parseInt(requireValue(argv, ++index, arg), 10);
        if (!Number.isFinite(args.chunkSeconds) || args.chunkSeconds <= 0) {
          throw new Error("--chunk-seconds must be a positive integer.");
        }
        break;
      case "--force":
        args.force = true;
        break;
      case "--help":
      case "-h":
        args.help = true;
        break;
      default:
        if (arg.startsWith("-")) {
          throw new Error(`Unknown flag: ${arg}`);
        }
        args.inputs.push({ kind: "video", path: arg });
        break;
    }
  }

  if (isAbsolute(args.outDir)) {
    throw new Error("--out must be a relative path inside the user's current directory.");
  }

  return args;
}

function requireValue(argv, index, flag) {
  const value = argv[index];
  if (!value || value.startsWith("--")) {
    throw new Error(`${flag} requires a value.`);
  }

  return value;
}

function promptWithContext(prompt, previousText) {
  if (!prompt) {
    return undefined;
  }

  const trimmedPrevious = previousText.trim();
  if (!trimmedPrevious) {
    return prompt;
  }

  const context = trimmedPrevious.slice(-700);
  return `${prompt}\n\nPrevious transcript context from the immediately preceding chunk:\n${context}`;
}

function safeStem(filePath) {
  const stem = basename(filePath, extname(filePath));
  const safe = stem
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);

  return safe || `video-${randomUUID()}`;
}

function formatBytes(bytes) {
  const mib = bytes / (1024 * 1024);
  return `${mib.toFixed(1)} MB`;
}

function yamlString(value) {
  const stringValue = String(value);
  return JSON.stringify(stringValue);
}

function redactLikelySecrets(text) {
  return text.replace(/sk-[A-Za-z0-9_-]+/g, "sk-REDACTED");
}

function logInfo(message) {
  console.log(`[info] ${message}`);
}

function logWarn(message) {
  console.warn(`[warn] ${message}`);
}

function logError(message) {
  console.error(`[error] ${message}`);
}

function printHelp() {
  console.log(`Usage:
  node skills/yc-partner/scripts/transcribe-videos.mjs --founder founder.mp4 --demo demo.mov

Reads OPENAI_TOKEN from .env in the current directory, extracts audio with ffmpeg,
uploads only the derived audio to OpenAI, and writes private Markdown transcripts.

Inputs:
  --founder <path>          Founder video file. May be repeated.
  --demo <path>             Demo video file. May be repeated.
  --video <path>            Generic video file. May be repeated.

Options:
  --out <dir>               Private output directory. Default: ${DEFAULT_OUT_DIR}
  --model <model>           Transcription model. Default: ${DEFAULT_MODEL}
  --language <code>         Optional language code, such as en.
  --prompt <text>           Optional transcription prompt.
  --no-prompt               Do not send the default YC application context prompt.
  --audio-bitrate <rate>    ffmpeg AAC bitrate. Default: ${DEFAULT_AUDIO_BITRATE}
  --chunk-seconds <number>  Chunk length when audio exceeds 25 MB. Default: ${DEFAULT_CHUNK_SECONDS}
  --force                   Regenerate existing derived audio/chunks.
  --help                    Show this help.
`);
}
