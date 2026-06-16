# AGENTS.md

## Source Of Truth

The root `README.md` is the product source of truth. If lower-level scaffolding disagrees with it, update the skill and repo structure to match the README.

## Goal

`yc-partner` is a public, open source knowledge pack and agent skill for founders applying to Y Combinator.

It should help users:

- Answer pre-application YC questions and doubts before they finish writing.
- Review YC applications with fresh eyes.
- Improve clarity, specificity, and application hygiene.
- Estimate whether the application is likely to earn an interview.
- Prepare for YC interviews.
- Verify advice against YC resources, YC-affiliated material, examples, and founder stories.
- Find relevant YC resources to read or watch.

## Skill Boundary

The skill is the artifact. `skills/yc-partner/SKILL.md` is for founders using the installed skill, not for maintainers building the corpus.

Keep runtime skill instructions focused on:

- How to answer pre-application questions and doubts.
- How to review applications.
- How to prepare founders for interviews.
- What sources to trust.
- How to find bundled resources.
- Tone, posture, required vs optional behavior, and dos/don'ts.

Keep collection, transcription, scraping, indexing, and guide-generation instructions outside the runtime skill, in `AGENTS.md`, `README.md`, `scripts/README.md`, or maintainer docs.

## Public-Safe Boundary

Do not include:

- Private YC applications unless explicitly contributed for public use.
- Personal contact information, private founder profiles, emails, phone numbers, screenshots, internal notes, or unpublished drafts.
- Private anecdotes unless rewritten as approved public examples.
- Secrets, credentials, `.env` files, auth cookies, browser session data, or private API outputs.
- Raw unprocessed HTML, downloaded videos, audio files, screenshots, caption JSON, or temporary scraper outputs.

If a file contains private information or application-specific content, keep it out of `yc-partner`.

## Source Scope

Official YC sources are highest priority for YC-specific guidance:

- YC website pages and guides.
- YC blog posts and essays.
- YC YouTube videos and transcripts.
- Startup School pages, lectures, and transcripts.
- YC Requests for Startups and YC company-directory pages when relevant.
- Public posts by YC partners when published through YC, Startup School, or official/clearly attributable channels.

### YC Company Directory Verification

When asked to check whether a company or founder is YC-affiliated, prefer the official YC Startup Directory and individual company pages first:

- Directory: `https://www.ycombinator.com/companies`
- Company pages: `https://www.ycombinator.com/companies/<slug>`

If a public YC-hosted, website-backed, or user-supplied company-directory API is available for the task, it may be used for lookup, but record the exact source URL, observed batch/status/founders, and capture date. Use third-party mirrors or scraper APIs only as fallback context, not as primary verification.

Also include, clearly labeled:

- Paul Graham essays.
- Jessica Livingston writing/interviews.
- YC partner blogs, tweets, talks, and interviews.
- Dalton + Michael videos.
- Social Radars podcast material.
- Public example YC applications, demo videos, and founder videos.
- Founder stories from renowned YC startups, especially from their YC/early-company days.
- External startup context when useful, labeled as external context, not YC guidance.

## Content Format

Durable source files should be processed Markdown with compact traceable metadata and the full captured content.

Use this shape:

1. `# Title`
2. Compact metadata bullets only:
   - `Type`
   - `Status`
   - `URL`
   - `Author`
   - `Published`
   - `Captured`
   - `Method`, only when useful
   - `Caveat`, only as a short link to `references/caveats/*.md` when a repeated caveat applies
3. One `## Summary` section before the content. Use concise bullets for summary, table of contents, capture notes, source status, or reviewer comments. Do not add separate `Caveats`, `Key Guidance`, `Application/Interview Relevance`, or `Notes` sections to source files.
4. One source-content section such as `## Content`, `## Transcript`, `## Essay Text`, or `## Page Text`. Preserve the full processed Markdown text of YouTube transcripts, podcast transcripts, blog posts, essays, forms, tweets, and similar sources.

Never summarize first and discard detail. Do not create parallel short/source versions by default; use indexes and guides for routing, review notes, source-grounded quotes, and synthesized guidance.

Do not bulk-reprocess existing captures just to migrate formatting. When you read, link, cite, edit, or otherwise touch an existing capture, progressively update that specific file to the latest compact template and refresh any affected indexes, guide references, and `path:line` citations in the same change.

Do not commit raw capture artifacts. If raw capture is needed, keep it outside the repository or in an ignored local staging area, then convert it into clean Markdown before committing.

## X/Tweet Capture Rule

When the user provides pasted X/Twitter text and a public status URL, treat the pasted text as the capture source of truth. Do not try to load X to verify the post body unless the user explicitly asks for that. X pages are often unavailable or incomplete to agents.

For pasted X captures:

- Preserve the provided post text in processed Markdown.
- Include the original public URL and author handle when provided.
- Record visible timestamps, view counts, and UI context as capture details in the single `Summary` section when useful.
- Do not label pasted public-source text as secondhand, excerpted, or unverified in source status or caveats. If capture method matters, use compact neutral wording such as `Method: pasted public text`.
- If useful, derive timestamps from public status IDs locally, but do not replace visible timestamps with an unlabelled derived value.

## Structure

Use this structure unless the README requires a change:

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `AGENTS.md` - maintainer and agent instructions.
- `LICENSE` - open source license.
- `README.md` - human-facing product direction and usage.
- `skillpack.json` - lightweight skillpack-style manifest.
- `skills/yc-partner/SKILL.md` - runtime skill entry point.
- `skills/yc-partner/references/` - compact founder-facing references loaded on demand.
- `skills/yc-partner/references/caveats/` - shared caveat/disclaimer notes linked from compact source metadata.
- `skills/yc-partner/resources/application-form/` - official YC application form questions and batch-specific prompt captures.
- `skills/yc-partner/resources/yc-website/` - official YC website material.
- `skills/yc-partner/resources/rfs/` - official YC Requests for Startups sections.
- `skills/yc-partner/resources/yc-youtube/` - YC YouTube transcripts.
- `skills/yc-partner/resources/yc-partners/` - YC partner blogs, talks, and related material.
- `skills/yc-partner/resources/tweets/` - public tweets and X threads from YC-affiliated people and other relevant startup sources.
- `skills/yc-partner/resources/interviews/` - interviews with Paul Graham, Jessica Livingston, and YC partners.
- `skills/yc-partner/resources/pg-essays/` - Paul Graham essays.
- `skills/yc-partner/resources/social-radars/` - Social Radars podcast transcripts.
- `skills/yc-partner/resources/founder-stories/` - YC founder stories from renowned startups.
- `skills/yc-partner/resources/dalton-michael/` - Dalton + Michael video transcripts.
- `skills/yc-partner/resources/examples/` - public example applications, founder videos, and demo videos.
- `skills/yc-partner/resources/external/` - non-YC public context, clearly labeled.
- `skills/yc-partner/indexes/` - routing maps by application question, FAQ topic, interview topic, source type, and theme.
- `skills/yc-partner/guides/` - maintained Markdown guides updated as resources change; automated updates and optional curated notes live in the same guide files.
- `skills/yc-partner/routing-eval.jsonl` - trigger examples.
- `skills/yc-partner/runbooks/bootstrap.md` - post-install orientation.
- `scripts/` - root-level collection, transcription, extraction, indexing, guide generation, and submitted-video analysis scripts.
- `templates/` - maintainer templates.

## Resource Pipeline

1. Collect public material outside the runtime skill when raw capture is needed.
2. Convert each source into processed Markdown under `skills/yc-partner/resources/`.
3. Immediately inspect the captured content and update relevant indexes under `skills/yc-partner/indexes/` with useful quotes, paragraphs, or facts linked as `path:line`.
4. Update maintained Markdown guides under `skills/yc-partner/guides/` when the source changes application review, interview prep, or resource-selection guidance.
5. Put durable human judgment in optional guide sections or `skills/yc-partner/references/`; do not require a curated companion file for every generated update.
6. Do not leave `Pending manual extraction`, empty guidance placeholders, or deferred indexing notes in source files. If a source is useful enough to capture, index the useful parts during the same change.

## Review Behavior

The skill should be direct, specific, source-grounded, and skeptical without being theatrical.

For pre-application guidance, confidently answer common YC doubts when the corpus supports them: applying with just an idea, whether a school or pedigree matters, solo founders, nontechnical founders, students and Early Decision, international founders, already-funded companies, late applications, reapplying after rejection, whether YC funds a sector, and fear or uncertainty about applying. Prefer official YC sources first, then use partner tweets/posts/interviews and founder stories for extra context. Give the founder a direct answer plus a small set of relevant sources to read, not a broad resource dump.

Internal indexes and guides may cite bundled source files as `path:line` for maintainability. Runtime, founder-facing answers must translate those internal citations into public URLs from source metadata. For YouTube sources, use timestamped public links when the relevant timestamp is available. Do not expose local skill file paths to founders unless they explicitly ask for debugging details about the installed skill.

Prioritize:

- Clear company description.
- Specific user/customer pain.
- Evidence, traction, revenue, usage, and speed.
- Founder insight and founder-market fit.
- Direct answers to each prompt.
- Concrete language over jargon.
- Distinguishing YC guidance, public examples, founder stories, and inference.

Do not act as a ghostwriter. Suggested rewrites are directional examples, not copy-paste final answers.

## Maintenance Rules

- Preserve user privacy.
- Never read, print, modify, or summarize `.env` files.
- Do not add private application data.
- Do not add raw media, raw HTML, or raw caption files.
- Preserve source metadata.
- Label non-official sources clearly.
- Keep guide files current as resources change; preserve manual notes when regenerating or patching guide sections.
- Keep `SKILL.md` concise; move detailed context into bundled resources, indexes, guides, and references.
