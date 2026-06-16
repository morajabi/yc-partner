# Resources

This folder contains processed Markdown source files only.

Every source file should use this compact shape:

1. `# Title`
2. Metadata bullets: `Type`, `Status`, `URL`, `Author`, `Published`, `Captured`, optional `Method`, and optional `Caveat`.
3. One `## Summary` section for concise bullets, table of contents, capture notes, or reviewer comments.
4. One source-content section such as `## Content`, `## Transcript`, `## Essay Text`, or `## Page Text`.

Preserve the full processed source content. Put extracted guidance, application relevance, caveats, and cross-source synthesis in `indexes/` or `guides/`, not in extra sections inside source files.

For repeated caveats, link to a shared file from the metadata block:

- `Caveat: references/caveats/official-yc-source.md`
- `Caveat: references/caveats/yc-founder-partner-source.md`
- `Caveat: references/caveats/yc-rfs-source.md`
- `Caveat: references/caveats/founder-story.md`

Do not commit raw HTML, downloaded media, raw transcripts, caption JSON, screenshots, private applications, or personal founder data.

## Resource Buckets

- `application-form/` - official YC application form questions and batch-specific prompt captures.
- `yc-website/` - official YC website, YC Blog, and YC Library material.
- `yc-company-directory/` - parsed public YC company directory data plus derived group partner profile summaries.
- `rfs/` - official YC Requests for Startups sections, split into one processed Markdown file per RFS.
- `yc-youtube/` - official YC YouTube transcripts.
- `yc-partners/` - YC partner blogs, talks, and related material.
- `tweets/` - public tweets and X threads from YC-affiliated people and other relevant startup sources.
- `interviews/` - interviews with Paul Graham, Jessica Livingston, YC partners, and YC-affiliated startup thinkers.
- `pg-essays/` - Paul Graham essays.
- `social-radars/` - Social Radars podcast page captures and notes.
- `founder-stories/` - YC founder stories from renowned startups.
- `dalton-michael/` - Dalton + Michael video transcripts.
- `examples/` - public example applications, founder videos, and demo videos.
- `external/` - non-YC public context, clearly labeled.
