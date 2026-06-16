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
Give a source-grounded first-pass review with a quick overview, scorecard, highest-ROI fixes, application tips, office-hours startup advice, hygiene, and a fun fact.
```

## Review Output

### Overview

- Strong early application: the product is easy to understand, the pain is concrete, and the demo/prototype does real work.
- The main upgrade is not more ambition. It is making user pull measurable: beta size, active use, retention, and the strongest usage anecdotes.
- The founder case is strong for an early, mostly solo application because technical ownership and commitment are obvious.

### Scorecard

- Application strength: 0.84
- Text-only interview likelihood: 0.78
- Fixes: 4
- Good areas: 3
- Risks: 3
- Highest-impact changes: quantify beta usage; make the opening sentence user-visible; address solo-founder execution risk.
- Caveat: this is a text-only estimate from a public historical example, not YC feedback or an admissions prediction.

### What's Good

- Clear product: automatic file sync and backup for people tired of email attachments, USB drives, manual uploads, and versioned filenames.
- Strong insight: the application understands that users want files to "just work," not another online drive abstraction.
- Strong founder signal: real prototype, demo, technical ownership, prior startup/project history, and stated full-time commitment.

### Highest-ROI Risks

- Beta demand is under-quantified: the application says private beta but not how many users, how active, or how retained.
- Solo-founder risk is real: the application should show how product, infrastructure, support, and early sales will stay fast as usage grows.
- API/partner interest is promising but too vague unless tied to named demand, workflows, payment intent, or repeated requests.

### Changes To Make

1. Quantify the beta.

Add one sentence with current beta count, active users, sync frequency, retention, and the strongest usage anecdote. A small but retained beta is more persuasive than a large vague one.

2. Make the first sentence even more direct.

The opening is already clear, but it can lead with the user-visible action: "Dropbox keeps a folder automatically synced across your computers and backed up online." Michael Seibel's pitch advice is to start with what the company does, not a setup paragraph ([How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)).

3. Address solo-founder execution risk.

Do not apologize for being solo; show the compensating strength. The application should make the reader feel that Drew can ship quickly, keep the system reliable, learn from users, and recruit help when the bottleneck changes.

4. Turn partner/customer interest into evidence.

"Potential partners/customers asking for an API" should become: who asked, what they wanted to build, whether they would pay, and whether the request appeared more than once.

### Fun Fact

The W23 recap said 52% of that batch was accepted with just an idea and no product, and 77% without revenue. Dropbox had already cleared the harder early-stage proof bar in this application because it had a working demo and beta users ([PG thread](https://x.com/paulg/status/1642566043053826048)).

### Tips

- Application tip: YC says applying early is fine; the application still has to show why the early evidence matters ([YC FAQ](https://www.ycombinator.com/faq)).
- Application tip: Use the demo as proof of seriousness. YC's demo guidance says the difference between nothing and something is huge, even if the demo is rough ([YC application tips: include a demo](https://www.ycombinator.com/library/4X-yc-application-tips-include-a-demo)).
- Application tip: Keep rewrites factual. A stronger one-liner should clarify the product, not turn Dropbox into a generic "cloud collaboration platform."

### Office Hours

- Startup advice: the next operating bottleneck is user learning. Find the handful of beta users who would be most upset if Dropbox disappeared and learn exactly why.
- Startup advice: if the product is already valuable, make retention and reliability the scoreboard. Sync is a trust product; one bad failure can erase a lot of goodwill.
- Startup advice: do not get distracted by every possible expansion. Prove the core folder-sync behavior is loved before API, enterprise, and collaboration branches take over.

### Hygiene

- Strong demo signal, but the application should make beta metrics easier to scan.
- No obvious required-field issue in this public text.
- Legal/IP references should be kept precise and current in a real application.

### Next Questions

- How many beta users were active in the last 7 and 30 days?
- What percentage kept using Dropbox after first install?
- What is the strongest user quote or behavior showing they would be upset if it disappeared?

### Sources

- [Dropbox public application](https://getintoyc.com/company/dropbox/)
- [YC FAQ](https://www.ycombinator.com/faq)
- [Michael Seibel: How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)
- [YC application tips: include a demo](https://www.ycombinator.com/library/4X-yc-application-tips-include-a-demo)
- [PG thread with W23 recap](https://x.com/paulg/status/1642566043053826048)
