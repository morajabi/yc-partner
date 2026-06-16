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
Give a source-grounded first-pass review with an evidence ledger, highest-impact fixes, score, helpful notes, and a fun fact.
```

## Review Output

### One-Line Read

Paystack is building APIs and tools that let African merchants accept online payments from local and international customers.

### Evidence Ledger

- Product: PCI-compliant payments infrastructure and APIs, with examples of live demo merchants.
- User: African merchants and developers who cannot easily accept online payments, recurring payments, one-click payments, local card schemes, mobile money, and international cards.
- Proof users care: 12 pilot merchants, about 400 merchants on the waitlist, $1,300 revenue, live transactions, a dozen pilots, 150 merchant conversations, and pilot merchants using the product even before settlement was implemented.
- Founder-market fit: Founder had direct startup pain from trying to accept online payments in 2010 and spent 2014 implementing payments and disbursement solutions for banks.
- Unique insight: The infrastructure existed in pieces; the hard part was integrating it locally and serving merchant/developer needs better than banks or global payment companies.
- Distribution: Word of mouth, local developer community, merchant outreach, integrations with Shopify/Eventbrite/WooCommerce, and Access Bank customer access.
- Main risks: Fintech compliance and fraud risk, settlement trust, technical ownership, contractor-built Android library, single-founder setup, and vague growth denominators.

### What Works

This application has unusually strong founder-market fit. It is not an abstract "Stripe for X" clone. The founder experienced the problem as a merchant, then spent a year implementing bank payment infrastructure, then built the missing developer-facing layer. That is exactly the kind of market knowledge YC can use when partners are not the domain experts.

The user evidence is also strong for a private beta. "12 pilot merchants" and "$1,300 revenue" are small numbers, but the quality of the evidence is better than the size suggests. The most compelling sentence is that merchants were willing to use the product without settlement for six weeks. That points to pain and trust, not just curiosity.

The differentiation answer is practical. Paystack explains why local financial institutions move slowly, why global companies may miss local card/payment schemes, and why local non-financial companies are the real competition.

### Highest-Impact Fixes

1. Clarify technical ownership.

The application says the Android library was written by a contractor. That may be fine, but for a fintech infrastructure startup, YC will care who owns core technical execution. The answer should make clear who built and maintains the payment APIs, vault, anti-fraud, chargeback protection, compliance work, and integrations.

2. Make the growth metrics defensible.

"Waiting list at 10x" and "transaction volume at 15x" sound impressive, but without baseline and time window they are hard to evaluate. A better answer would say: starting point, ending point, period, transaction count, transaction value, and whether the volume came from repeat merchant behavior.

3. Address trust, settlement, and fraud head-on.

The application says merchants used Paystack without settlement, which is powerful evidence. It also creates the obvious partner question: why did they trust you, how did you handle settlement risk, and what happens at scale? For fintech, naming the hard part makes the application stronger.

4. Explain the founder/team setup.

The public application mostly reads as one founder with employee/advisory pools. YC accepts solo founders, but one-person startups are harder. Paystack should show the actual execution capacity around engineering, compliance, banking relationships, sales, and support.

### Score

- Application strength: 0.80
- Interview-pull signal from text: 0.74
- Confidence: Medium

Why not higher: key fintech execution risks are not fully answered, and the team/technical ownership picture is incomplete. Why high: the founder has unusually relevant lived and professional experience, the merchant pain is concrete, and the early user pull looks real despite small revenue.

### Helpful Notes

- Paul Graham's YC interview essay says YC partners often rely on founders as domain experts if the founders know what they are talking about and are not misleading. Paystack's strongest case is that the founder can teach YC about African merchant payments from direct experience ([Billionaires Build](https://www.paulgraham.com/ace.html)).
- The official YC FAQ says YC considers startups in any field, not only software, but the application still needs the founding team's ability to build the product. For Paystack, that means technical ownership and regulatory execution should be more explicit ([YC FAQ](https://www.ycombinator.com/faq)).
- The customer-learning evidence is strong: 150 merchant conversations plus merchants using an incomplete settlement flow. The next revision should turn that learning into concrete product decisions, not just state that demand is amazing.

### Fun Fact

When asked whether Africa-based companies need more progress to be accepted, Paul Graham replied that they need no more progress than companies from other continents. That is useful context for Paystack-style applications: geography is not the issue; clarity, founder strength, user pull, and execution risk are ([PG thread](https://x.com/paulg/status/1642566043053826048)).

### Source Trail

- [Paystack public application](https://getintoyc.com/company/paystack/)
- [Paul Graham: Billionaires Build](https://www.paulgraham.com/ace.html)
- [YC FAQ](https://www.ycombinator.com/faq)
- [Michael Seibel: How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)
- [PG thread with geography reply](https://x.com/paulg/status/1642566043053826048)
