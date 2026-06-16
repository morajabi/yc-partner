# Example Run: Dropbox Public YC Application Review

- Source application: [Dropbox on Get into YC](https://getintoyc.com/company/dropbox/)
- Source status: Public historical YC application example labeled successful by Get into YC.
- Review mode: Broad first-pass YC Partner review.
- Caveat: This is a demo of the skill's review behavior, not a modern admissions prediction and not YC feedback.

## What This Demo Shows

- How YC Partner treats an early, pre-revenue application when the product and founder signal are strong.
- How it separates real strengths from missing evidence, instead of flattening everything into "too early" or "obviously great."
- How it uses source-backed notes and directional rewrites without trying to ghostwrite the final application.

## Prompt

```text
Use YC Partner to review this public YC application: https://getintoyc.com/company/dropbox/
Give a source-grounded first-pass review with an evidence ledger, highest-impact fixes, score, helpful notes, and a fun fact.
```

## Review Output

### One-Line Read

Dropbox is building automatic file sync and backup for individuals and teams, packaged so nontechnical users get version-control-like benefits without thinking about version control.

### Evidence Ledger

- Product: Working prototype and private beta; screencast and Windows build were provided.
- User: Individuals and small teams that need files to stay current across computers without emailing, USB sticks, manual uploads, or brittle online-drive workflows.
- Proof users care: Private beta usage, a concrete little-sister use case, partner/customer interest in APIs, and requests for enterprise/network deployment.
- Progress: Built in roughly 3 months part-time, with about 5K lines of client code and 2K lines of server code.
- Founder signal: Drew is the technical founder, has built a profitable SAT prep business, and had prior hacker/project evidence. He also says he is leaving his job to work on Dropbox full-time regardless of YC.
- Unique insight: Existing products operate at the wrong abstraction layer; the real user desire is "hit save and everything works."
- Market path: Starts with simple individual/team sync and expands into paid storage, team plans, API integrations, enterprise deployments, and collaboration workflows.
- Main risks: Private beta traction is not quantified; team is effectively solo; business model is still a plan; legal/IP risk is mentioned but would need current documentation.

### What Works

The application has unusually clear founder-product fit. It does not say "cloud collaboration platform" and hope the reader guesses the product. It explains a painful workflow: people manually version files through email, USB sticks, web uploads, and document names like "proposal v2." That is exactly the kind of concrete user behavior that makes an application easier to believe.

The strongest answer is the "what do you understand" answer. The insight is not just "sync is useful." It is that manual web uploads and online-disk abstractions force users to think about file movement. Dropbox's answer makes the product feel obvious after you read it, which is a strong sign.

The founder signal is also strong for an early company. YC says many accepted companies are very early, but the application still needs compensating evidence when there is little revenue or scale. Here the compensation is a real build, a demo, technical ownership, startup history, and full-time commitment.

### Highest-Impact Fixes

1. Quantify the beta.

The application says Dropbox is in private beta and batches of people are being added, but it does not say how many active users, how often they sync, whether they keep using it, or what failures users tolerate because the product is valuable. If I were revising this today, I would add one sentence with the current beta count, active usage, retention/frequency, and strongest usage anecdote.

2. Make the first sentence even more direct.

The opening is already clear, but the strongest modern version would lead with the user-visible action, then add the technical depth:

> Dropbox keeps a folder automatically synced across your computers and backed up online, so individuals and teams can work on the latest version of their files without emailing, uploading, or carrying USB drives.

That is not a copy-paste suggestion; it is the direction. The real answer should use the founder's own wording.

3. Address the solo-founder risk directly.

The application shows Drew is committing full-time, but it does not explain how he will cover product, infrastructure, customer support, sales, and hiring if usage starts growing. YC accepts solo founders, but the application should make the compensating strength obvious: exceptional shipping speed, technical depth, and a plan for help.

4. Turn partner/customer interest into evidence.

"Potential partners/customers asking for an API" is useful, but it would be stronger if named, dated, and tied to concrete demand. For example: who asked, what workflow they wanted, whether they would pay, and whether this was a one-off request or a pattern.

### Score

- Application strength: 0.84
- Interview-pull signal from text: 0.78
- Confidence: Medium

Why not higher: the application is excellent for an early product, but a text-only review still lacks beta usage counts, retention, and revenue evidence. Why high anyway: the product is understandable, the demo exists, the user pain is concrete, and the founder has strong technical and commitment signal.

### Helpful Notes

- Official YC guidance says it is not a mistake to apply early; YC recommends applying once you have a founding team and an idea you are excited about. For Dropbox, the important point is not stage, it is that the application gives early-stage evidence: demo, prototype, user pain, and founder ability ([YC FAQ](https://www.ycombinator.com/faq)).
- Michael Seibel's pitch test is useful here: start with what the company does in simple language, not with why the idea is impressive. Dropbox mostly passes that test because the application describes the user path and the pain plainly ([How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)).
- Paul Graham's YC interview essay says partners dig into who the first users are and how founders know they want the product. Dropbox has good qualitative evidence, but the next improvement would be making beta usage more measurable ([Billionaires Build](https://www.paulgraham.com/ace.html)).

### Fun Fact

The historical W23 recap said 52% of that batch was accepted with just an idea and no product, and 77% without revenue. Dropbox was already past that bar in this application because it had a working demo and beta users, even though it was still very early ([PG thread with W23 recap](https://x.com/paulg/status/1642566043053826048)).

### Source Trail

- [Dropbox public application](https://getintoyc.com/company/dropbox/)
- [YC FAQ](https://www.ycombinator.com/faq)
- [Michael Seibel: How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)
- [Paul Graham: Billionaires Build](https://www.paulgraham.com/ace.html)
- [YC application video guidance](https://www.ycombinator.com/video)
