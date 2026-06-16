# Example Run: GitLab Public YC Application Review

- Source application: [GitLab on Get into YC](https://getintoyc.com/company/gitlab/)
- Source status: Public historical YC application example labeled successful by Get into YC.
- Review mode: Broad first-pass YC Partner review.
- Caveat: This is a demo of the skill's review behavior, not a modern admissions prediction and not YC feedback.

## What This Demo Shows

- How YC Partner reviews a strong application without turning the review into empty praise.
- How it keeps pressure on claim discipline even when the company has real traction, revenue, and usage.
- How it distinguishes "add more proof" from "add more hype."

## Prompt

```text
Use YC Partner to review this public YC application: https://getintoyc.com/company/gitlab/
Give a source-grounded first-pass review with a quick overview, scorecard, highest-ROI fixes, application tips, office-hours startup advice, hygiene, and a fun fact.
```

## Review Output

**Overview**
GitLab reads as a very strong YC application: open-source code collaboration, deployed mostly on-premise, with 100k+ organizations, named paying customers, 600+ contributors, $1M ARR, and ~60% monthly revenue growth in the submitted text ([public application](https://getintoyc.com/company/gitlab/)). The application’s strength is not polish; it is concrete proof that real developers and enterprises already care.

Text-only application strength: **0.88/1.00**
Text-only interview likelihood: **0.85/1.00**
Caveat: this is a review of the written public application, not an admissions prediction.

**Scorecard**

| Area | Read |
|---|---|
| Founder signal | Strong: technical founders, long collaboration, product built by the team/community. |
| Company signal | Very strong: real usage, revenue, named customers, open-source distribution. |
| Application signal | Good but sloppy: clear enough to win, but several answers leave avoidable doubts. |
| Fixes | 8 |
| Good areas | 6 |
| Risks | 5 |

Highest-impact changes: clarify metric quality, sharpen the on-prem/open-source wedge, clean up wording and missing details.

**What’s Good**
- The first product answer is unusually concrete: “run your own GitHub,” self-hosted, merge requests, wikis, issues, CI. YC later used GitLab as an example of a clear application description in Dalton Caldwell’s application talk ([YC video](https://www.youtube.com/watch?v=B5tU2447OK8)).
- The traction is real: 100k+ organizations, 1M estimated active users, named paying customers, $1M ARR, and 600 contributors.
- The insight is strong: open-source developer infrastructure can distribute, improve, and sell into enterprises differently from closed-source competitors.
- The competitor answer names real alternatives and explains concrete differences: self-hosting, clustering/scaling, integration, flexibility, and price.
- The story has founder-market fit: Dmitriy wanted it at a previous job, and most employees were developers.

**Highest-ROI Risks**
- “We estimate more than 1M” is too vague. Active how? Monthly active developers? Installations? Users behind firewalls? This matters because YC looks for evidence users want the product, not just big numbers ([YC application advice](https://www.youtube.com/watch?v=B5tU2447OK8)).
- “Most popular open source version control software” and “more installations than anything else” are strong claims but need evidence or narrower wording.
- The application under-explains revenue quality: $1M ARR and 60% monthly revenue growth are excellent, but the reader needs customer count, ACV range, churn/retention, and whether revenue is recurring subscription revenue.
- The user-learning answer lists channels, but not what users taught them. PG’s compact YC advice is to explain what you learned from users because it tests user attention and depth of need ([PG essay](https://www.paulgraham.com/users.html)).
- Focus risk: they mention on-prem, CI, SaaS, marketing, and GitLab.com. The core wedge is on-prem/open-source enterprise DevOps; don’t let the application sound scattered.

**Highest-ROI Fixes**
1. **Upgrade the traction answer from impressive to airtight.**
   Replace broad claims with denominated metrics: paying organizations, ARR by month, net revenue retention if known, active installations, GitLab.com MAU, contributor growth, and enterprise logo proof. Sam Altman’s Startup Playbook warns against vanity metrics and says retention matters as much as acquisition ([Startup Playbook: Growth](https://playbook.samaltman.com/#growth)).

2. **Make the unique insight sharper.**
   The best sentence is basically: “Developer infrastructure sold to enterprises can grow through open-source adoption first, then convert via enterprise features and support.” That is stronger than “open source markets your product for free.” It explains distribution, product feedback, and monetization in one loop.

3. **Clarify the wedge against GitHub Enterprise and Atlassian.**
   The strongest wedge is not “cheaper.” It is: self-hosted, inspectable, modifiable, integrated code + issues + wiki + CI, and better suited to behind-the-firewall enterprise development. Keep competitor language factual; Sam Altman’s competitor advice is to worry less about competitors and more about making a great product/company ([Startup Playbook: Competitors](https://playbook.samaltman.com/#competition)).

4. **Turn user feedback channels into user lessons.**
   Current answer: “we listen via feedback, merge requests, issues, Twitter…” Better direction: “Enterprise users told us GitHub Enterprise’s VM model didn’t scale for their internal workflows, so we prioritized self-hosting, source access, and integrated CI.” Only use that exact claim if true.

5. **Tighten founder seriousness.**
   “Since 2011, over 10,000 commits” is good but incomplete. Say who is full-time, since when, who writes code, who sells, and how responsibilities split. YC readers explicitly ask who the founders are, what exists today, whether users exist, and what is special ([YC application advice](https://www.youtube.com/watch?v=B5tU2447OK8)).

**Fun Fact**
YC’s Commercial Open Source RFS later named GitLab as one of the open-source companies YC funded, alongside Docker, Apollo, and Supabase, and said YC had funded 150+ open-source companies ([YC RFS: Open Source](https://www.ycombinator.com/rfs#open-source)).

**Tips**
- Lead with the strongest true claim. Michael Seibel’s pitch guidance says to start with what the company does in simple language, not setup or impressiveness ([How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)).
- Keep the “run your own GitHub” phrase. It is compressed and memorable, then the answer can immediately explain why GitLab is more than that.
- Don’t bury named customers. Apple, Qualcomm, NASA, Nasdaq OMX, and Interpol are major proof points; if they are paying or active, state exactly which.
- Include a demo link and founder video, but make sure the founder video follows YC’s rule: one minute, only founders talking, all founders present, no script, no demo replacement ([YC video guide](https://www.ycombinator.com/video)).
- Clean the application before submission. This application won despite typos; a current applicant should not rely on that.

**Office Hours**
- Pick one growth metric for the next month. For GitLab in 2015, I’d choose either new paid enterprise seats, ARR, or retained active self-hosted organizations, not broad “users.”
- Double down on the open-source enterprise loop: community adoption creates trust and feedback; enterprise features convert the highest-need organizations.
- Be careful splitting attention between on-prem, SaaS, and CI. The application’s best wedge is on-prem enterprise Git collaboration; CI and SaaS should reinforce that wedge, not read like separate startups.
- Interview prep should pressure-test the strongest claims: “How do you know you have more installations?”, “Why won’t GitHub fix this?”, “What percentage of users convert to paid?”, “Why is support alone not enough?”

**Hygiene**
Material issues: typos and awkward phrasing (“100.000,” “since than,” “where will be based,” “We offer the a”), missing/empty URL parentheses, an apparently redacted customer name on Get into YC, vague active-user estimate, and unsupported superlative claims. No founder video review was performed; I only reviewed the linked written application.

**Next Questions**
- What exactly counts as an active user in the “more than 1M” estimate?
- How many paying organizations are included in the $1M ARR, and what is the ACV range?
- What period does the ~60% monthly revenue growth cover?
- Which user segment is pulling GitLab.com rather than self-hosted GitLab?
- What did enterprise users teach the team that changed the product roadmap?

**Sources**
- [GitLab public application](https://getintoyc.com/company/gitlab/)
- [YC Startup School: How to Apply and Succeed at YC](https://www.youtube.com/watch?v=B5tU2447OK8)
- [Paul Graham: What I've Learned from Users](https://www.paulgraham.com/users.html)
- [Sam Altman: Startup Playbook - Growth](https://playbook.samaltman.com/#growth)
- [Sam Altman: Startup Playbook - Competitors](https://playbook.samaltman.com/#competition)
- [Michael Seibel: How to Pitch Your Company](https://www.michaelseibel.com/blog/how-to-pitch-your-company)
- [YC application video guide](https://www.ycombinator.com/video)
- [YC RFS: Commercial Open Source Companies](https://www.ycombinator.com/rfs#open-source)
