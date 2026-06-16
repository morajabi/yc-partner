# Example Run: Paystack Public YC Application Review

- Source application: [Paystack on Get into YC](https://getintoyc.com/company/paystack/)
- Source status: Public historical YC application example labeled successful by Get into YC.
- Review mode: Broad first-pass YC Partner review.
- Caveat: This is a demo of the skill's review behavior, not a modern admissions prediction and not YC feedback.

## What This Demo Shows

- How YC Partner handles a market where the founder knows more than the reviewer.
- How it weighs founder-market fit and customer pull against fintech execution, trust, compliance, and technical ownership risk.
- How it treats geography as context, not as a reason to discount the application.

## Prompt

```text
Use YC Partner to review this public YC application: https://getintoyc.com/company/paystack/
Give a source-grounded first-pass review with a quick overview, scorecard, highest-ROI fixes, application tips, office-hours startup advice, hygiene, and a fun fact.
```

## Review Output

### Overview

- Strong founder-market fit: this reads like a founder who has lived the payment problem and then worked close to the underlying banking infrastructure.
- The early user pull is promising despite small revenue, especially merchants using the product before settlement was complete.
- The biggest risks are fintech execution risks: technical ownership, settlement trust, fraud/compliance, and vague growth denominators.

### Scorecard

- Application strength: 0.80
- Text-only interview likelihood: 0.74
- Fixes: 4
- Good areas: 3
- Risks: 4
- Highest-impact changes: clarify technical ownership; make growth metrics defensible; address settlement/fraud risk directly.
- Caveat: this is a text-only estimate from a public historical example, not YC feedback or an admissions prediction.

### What's Good

- Strong market knowledge: the founder experienced the merchant payment problem directly and later implemented bank payment infrastructure.
- Strong early customer signal: 12 pilot merchants, about 400 merchants on the waitlist, $1,300 revenue, live transactions, and 150 merchant conversations.
- Strong pain evidence: merchants using Paystack before settlement was implemented suggests urgency and trust, not just curiosity.

### Highest-ROI Risks

- Technical ownership is not obvious enough for a fintech infrastructure company.
- "10x" waitlist and "15x" transaction growth need baselines, time windows, transaction count, and repeat behavior.
- Trust, settlement, chargebacks, fraud, and compliance are obvious partner questions and should be answered before the reader has to ask.
- The founder/team setup needs clearer coverage across engineering, banking relationships, sales, compliance, and support.

### Changes To Make

1. Clarify who owns the core technology.

The contractor-built Android library may be fine, but the application should make clear who built and maintains the payment APIs, vault, anti-fraud, chargeback protection, compliance work, and integrations. YC's FAQ says non-software and complex companies are fine, but the team still has to show it can build what matters ([YC FAQ](https://www.ycombinator.com/faq)).

2. Replace growth multiples with denominated metrics.

"10x" and "15x" sound exciting but are hard to evaluate without a starting point, ending point, period, and repeat behavior. For example: transaction count, transaction value, number of repeat merchants, and whether the same merchants kept processing after the first transaction.

3. Name the hard fintech risk.

The strongest version does not hide settlement and trust. It says why merchants trusted Paystack before settlement, how settlement risk was handled, what the fraud/chargeback plan is, and what changes at higher volume.

4. Make founder-market fit teach the reader.

The application should not just say the founder knows payments. It should include one or two concrete lessons from the 150 merchant conversations or bank implementation work that a generic "Stripe for Africa" pitch would miss.

### Fun Fact

When asked whether Africa-based companies need more progress to be accepted, Paul Graham replied that they need no more progress than companies from other continents. For Paystack-style applications, geography is context; the real questions are clarity, founder strength, user pull, and execution risk ([PG thread](https://x.com/paulg/status/1642566043053826048)).

### Tips

- Application tip: explain the domain in plain English. Paul Graham says YC partners may rely on founders as domain experts when the founders know what they are talking about and are candid about risks ([Billionaires Build](https://www.paulgraham.com/ace.html)).
- Application tip: do not rely on "Stripe for Africa" as the main explanation. Use it only after the reader understands the local payment workflow and why existing options fail.
- Application tip: for fintech, put credibility near the risk. If the hard parts are settlement, fraud, compliance, and bank integrations, the application should show who handles each one.

### Office Hours

- Startup advice: treat settlement trust as the product, not a back-office detail. If merchants trust you with money before the product is complete, learn exactly why.
- Startup advice: pick the first merchant segment where urgency is highest and integrations are repeatable. Broad "African merchants" is a market; the first wedge should be narrower.
- Startup advice: turn the 150 merchant conversations into product decisions. What did you remove, add, or prioritize because of those conversations?

### Hygiene

- Add baselines and time windows for all growth multiples.
- Clarify founder/team responsibilities and technical ownership.
- Keep compliance and settlement claims precise; do not state more certainty than the evidence supports.

### Next Questions

- Who built and maintains each critical part of the payment stack?
- What are the exact starting/ending values behind the 10x and 15x claims?
- What did the 150 merchant conversations change in the product?

### Sources

- [Paystack public application](https://getintoyc.com/company/paystack/)
- [Paul Graham: Billionaires Build](https://www.paulgraham.com/ace.html)
- [YC FAQ](https://www.ycombinator.com/faq)
- [PG thread with geography reply](https://x.com/paulg/status/1642566043053826048)
