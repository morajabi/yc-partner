# Application Research Guide

Use this when the user provides URLs, public founder handles, a company website, GitHub links, LinkedIn links, demo videos, or asks for a deeper analysis of the application beyond pasted answers.

Never copy private application data, private transcripts, or private founder data into this repository.

## Boundary

- Public research is supporting context, not a substitute for the application answers.
- Use public sources to verify, sharpen, or challenge claims. Do not speculate from weak signals.
- Do not browse private or authenticated pages unless the user explicitly provides access and the data is needed for the review.
- Do not scrape contact details, private emails, phone numbers, private screenshots, or hidden profile data into durable resources.
- If researching the live web for a founder/application review, cite public URLs in the response. Do not add those private founder profiles to this public skill repo unless the user explicitly contributed them for public use.

## Founder Profiles

When founder bios are thin but public links exist, create short private working profiles for the review:

- Current role and responsibility from the application.
- Technical-founder status and whether they can build the product without outside help, matching the YC form's technical-founder definition (`../resources/application-form/fall-2026-application-form-questions.md:105`, `../resources/application-form/fall-2026-application-form-questions.md:109`).
- Work history, education, notable projects, open source, products launched, prior startups, domain expertise, and evidence of unusual speed.
- How the founders know each other and whether they have worked together before. Jessica Livingston says cofounder history is valuable and that new cofounders with no history can be a major risk (`../resources/interviews/the-social-radar-y-combinators-secret-weapon-jessica-livingston-co-founder-of-yc-author-h9MUuhsDJOM.md:424`).
- Commitment signal: whether founders will work exclusively on the project if accepted, because the YC form asks this directly (`../resources/application-form/fall-2026-application-form-questions.md:114`).

Do not overvalue prestigious affiliations. Treat school, employer, and awards as signals to inspect, then ask what the founder has actually built. Jessica says early investors have little data and may look at where founders went to college and what they built before; the second half matters just as much for non-elite founders (`../resources/interviews/the-social-radar-y-combinators-secret-weapon-jessica-livingston-co-founder-of-yc-author-h9MUuhsDJOM.md:443`).

## Company Profile

Create a concise private working company profile before judging the answers:

- One-sentence description in plain English.
- Current product state: idea, prototype, launched, paid, retained, revenue, or growth.
- Target user/customer and the urgent pain.
- Current traction and what is verified by public links or user-provided evidence.
- Demo/product links, login requirements, app store/product pages, public GitHub, docs, changelog, blog posts, launch posts, or videos.
- Main competitors and adjacent YC-funded companies.
- The strongest true claim the company can make today.
- The freshest take: what is different from the graveyard of previous attempts in the category.

If a demo or founder video is present, transcribe or review it when the user asks. Use `guides/application-hygiene.md` and `guides/application-review.md` for video expectations.

## Public Website And Demo Review

When reading the company website, look for:

- Does the website explain what the product does faster than the YC application?
- Does it name the customer and pain clearly?
- Is there real product surface, screenshots, docs, pricing, sign-up, changelog, GitHub activity, or a demo?
- Does the public story contradict the YC application?
- Are claims like "used by X" or "revenue/customer" supported by public evidence or user-provided proof?

Do not mark the absence of public proof as dishonesty. Instead, distinguish:

- `Verified from public source`
- `Claimed in application`
- `Needs founder confirmation`
- `Inference`

## YC-Funded Company Check

Use the public YC company directory when relevant:

- Official YC FAQ says YC will consider startups in any field and points founders to the Startup Directory for funded examples (`../resources/yc-website/frequently-asked-questions.md:111`).
- The FAQ also says YC already funding a similar company will not affect acceptance chances (`../resources/yc-website/frequently-asked-questions.md:135`).
- The local directory capture includes company, batch, YC URL, industry, sectors, tags, one-liner, stage, region, website, and some group-partner fields (`../resources/yc-company-directory/README.md:11`).

Use similar YC-funded companies to ask sharper questions, not to discourage the founder:

- `YC has funded adjacent companies. What is different about your wedge, customer, timing, distribution, product insight, or execution?`
- `If a partner knows the space because YC has funded it before, what question would they ask first?`
- `Does your answer explain why users choose you rather than the obvious adjacent company?`

Label directory comparisons as context. Do not imply YC wants clones, avoid long market maps, and never claim a specific partner will be interested unless framed as inference from public data.

## Output Shape

For deep reviews, add a short section before the critique:

```md
## Working Profile

Company: ...
Founders: ...
Public evidence checked: ...
Strongest current claim: ...
Main uncertainty: ...
```

Then review the application against that profile. If public research reveals a stronger fact than the draft includes, tell the founder to add the fact. If it reveals a contradiction, ask for correction or clarification.
