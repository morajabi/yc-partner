# YC Partner

YC Partner is a public knowledge pack and Codex skill for founders applying to Y Combinator.

Think of it as a source-grounded second pair of eyes for your YC application. It helps you answer common YC doubts, review your draft with fresh eyes, prepare for interviews, and find relevant YC resources without turning your application into generic AI-written pitch copy.

It is based on official YC resources, Paul Graham essays, YC partner writing and interviews, Jessica Livingston material, founder stories, example applications, and related public material.

## What It Does

- Reviews YC application drafts for clarity, specificity, evidence, traction, founder-market fit, and application hygiene.
- Answers pre-application questions before you have a finished draft.
- Helps with common doubts: too early, solo founder, nontechnical founder, non-Ivy background, international founder, pre-revenue, reapplying after rejection, and whether YC funds your sector.
- Prepares you for YC interviews with direct questions, weak-point checks, and short-answer practice.
- Gives source-grounded office-hours-style guidance for startup obstacles, tactical operating questions, hiring, launch, customer discovery, runway, and investor meeting prep.
- Points you to a small set of relevant sources instead of dumping a giant reading list on you.
- Can work from founder/demo video transcripts, or help transcribe local videos when your environment is configured for it.

## Installation

The easiest way is to paste this into Codex or Claude Code:

```text
Install YC Partner globally as an agent skill from https://github.com/morajabi/yc-partner.git.
```

Manual Codex, Claude Code, and Claude.ai steps are in [INSTALL.md](INSTALL.md).

## Get Started

Ask:

```text
Use YC Partner to review my YC application
```

Then provide your application text or a path to a Markdown file.

You can also use it before you have a finished draft:

```text
Use YC Partner to answer my questions before I write my YC application
```

For video review, provide local paths to your founder video or demo video. If you want transcription handled locally, your environment needs `ffmpeg` and an `OPENAI_TOKEN`.

## Example Runs

These are demo reviews of public YC applications, included so you can see the kind of feedback YC Partner gives. They are not YC feedback, not admissions predictions, and not templates to copy.

- [Dropbox public application review](examples/yc-application-reviews/dropbox.md) - Shows how the skill handles an early, pre-revenue product with a strong demo, sharp user pain, and clear founder technical signal.

```text
- Dropbox is automatic file sync, backup, and versioning for individuals and small teams, starting with a Windows client plus web access.
- Strongest signal: Drew built a real product quickly, has a demo/build, understands the workflow pain, and is clearly technical.
- Biggest weakness: “Private beta” and “add batches every few days” need numbers, behavior, retention, and what users learned.
```

- [GitLab public application review](examples/yc-application-reviews/gitlab.md) - Shows how the skill reviews a later-stage devtools application with strong traction, revenue, open-source distribution, and a few claim-discipline issues.

```text
GitLab reads as a very strong YC application: open-source code collaboration, deployed mostly on-premise, with 100k+ organizations, named paying customers, 600+ contributors, $1M ARR, and ~60% monthly revenue growth in the submitted text. The application’s strength is not polish; it is concrete proof that real developers and enterprises already care.

“We estimate more than 1M” is too vague. Active how? Monthly active developers? Installations? Users behind firewalls? This matters because YC looks for evidence users want the product, not just big numbers.
```

## Resources Used

YC Partner ships with a processed public corpus, not just a prompt. The current snapshot includes:

- 418 processed Markdown source files across official YC material, partner writing, interviews, transcripts, public examples, podcast notes, and founder stories.
- 195 official YC resources, including YC website/blog/library pages, YouTube transcripts, Requests for Startups, application prompts, and company-directory context.
- 145+ transcript/interview/podcast-note captures from YC, Dalton + Michael, Social Radars, Garry Tan, Jessica Livingston, Gustaf Alstromer, Dalton Caldwell, and Lightcone.
- 74 partner essays/posts from Paul Graham, Sam Altman, Michael Seibel, Jessica Livingston, Geoff Ralston, Harj Taggar, Dalton Caldwell, and other YC-affiliated sources.
- 72 public examples and short-form captures, including YC application/demo examples and public tweet/X captures.
- YC company-directory context with 5,960 public company entries and 17 group-partner profiles.

When YC Partner quotes or cites a resource, it should show the public URL so founders can check the original source instead of being pointed at internal skill files.

## How To Use It

Use this as a fresh reviewer that gives you a high-level perspective on what you wrote. Founders are often too close to their product and know too much; they can become blind to descriptions that are too complicated for a YC partner to understand quickly. This is meant to help you close that gap.

Good uses:

- Paste a full draft and ask for a first-pass review.
- Ask why a specific answer sounds weak or confusing.
- Ask whether your stage, background, team, or sector is a reason not to apply.
- Ask for YC interview practice based on your application.
- Ask for the most relevant YC resources to read next.

## How Not To Use It

Please do not use YC Partner as a ghostwriter. Narrow sample rewrites can be useful when you are stuck on a confusing sentence or one important answer, but treat them as directional examples, not final copy. Plain copy-paste is likely to make your application worse because the model has no deep insight into your company or your unique angle. It may drift toward trendy or impressive-sounding language when what you usually need is the clearest human explanation of what you actually know.

Also do not treat any review, score, or estimate as an admissions prediction. YC decisions depend on the company, founders, timing, market, and information outside this repository.

## Sources

Official YC sources are the strongest source for YC-specific claims. Essays, blog posts, and interviews from YC partners, Paul Graham, Jessica Livingston, and similar YC-affiliated sources add useful perspective. Founder stories, public examples, tweets, and external anecdotes are context, not rules.

## What Not To Trust It For

YC Partner is not legal, immigration, tax, financial, or fundraising advice. For current YC policies, deadlines, terms, visas, incorporation, and funding mechanics, verify against official YC pages.

It is also not a replacement for founder judgment. The point is to help you see your application more clearly, not to outsource your thinking.

## Author Note

Created and maintained by Mo Rajabi as a personal open-source experiment for founders who want sharper, source-grounded YC application feedback. You can use this instead of harassing your friends to proofread/review your YC application and give you terrible advice (I'm joking of course!).

If you notice a mistake or incorrect source, please open an issue and I'll resolve it ASAP.

## Disclaimer

YC Partner is not endorsed by, affiliated with, or sponsored by Y Combinator in any way. It is a personal experiment you can use for educational purposes only.

## License

MIT
