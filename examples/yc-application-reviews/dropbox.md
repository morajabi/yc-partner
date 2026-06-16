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
review my application
```

## Review Output

**Overview**
- Dropbox is automatic file sync, backup, and versioning for individuals and small teams, starting with a Windows client plus web access.
- Strongest signal: Drew built a real product quickly, has a demo/build, understands the workflow pain, and is clearly technical.
- Biggest weakness: the app does not prove user pull yet. “Private beta” and “add batches every few days” need numbers, behavior, and what users learned.
- Biggest application flaw: several founder/legal/hygiene answers are incomplete or too jokey, which creates avoidable doubt.
- Text-only read: plausible-to-strong interview case if the demo is good and user numbers exist; from the text alone, founder/product signal is stronger than customer-demand proof.

**Good**
- The product explanation is unusually plain: sync files across computers, automatic, integrated into Windows, backed up to S3.
- The application shows a working product: screencast plus Windows build. YC explicitly says even rough demos matter because they show seriousness and ability to build ([YC demo advice](https://www.ycombinator.com/library/J8-yc-application-tips-include-a-demo)).
- Founder signal is strong: profitable prior startup, deep programming history, reverse-engineering poker-site software, and solo technical ownership.
- The progress answer is compact and impressive: prototype in February, beta in users’ hands, 7K lines across client/server/installer in three months part-time.
- The differentiation is not “better cloud storage.” It is “wrong layer of abstraction”: competitors make users think; Dropbox hides the machinery.
- Competitor awareness is strong. It names backup tools, sync tools, web upload tools, Google, Microsoft, and specific implementation risks.
- The business model is plausible and staged: consumer freemium, SMB/team plans, enterprise/on-prem requests, API demand.
- The “little sister” and ridiculous document-versioning examples convert technical insight into real user behavior.

**Fix**
1. **Put the strongest traction facts in “How far along are you?”**
   - Current text: “Beta - in people’s hands now.” Better: “X beta users across Y teams have synced Z files/GB; A users have used it for more than B weeks; C teams asked for paid storage/API/on-prem.”
   - YC-style scoring rewards metric quality over metric size: active, retained, high-intent behavior beats vague “users.”

2. **Add what users taught you.**
   - Paul Graham’s compact YC application advice is to explain what you learned from users because it tests whether founders understand users and whether users need the product ([PG essay](https://www.paulgraham.com/users.html)).
   - Dropbox has the raw material: sister using it for term papers, people naming files “proposal v2 good revised NEW,” teams juggling versions. Connect those observations to product decisions.

3. **Clarify the first customer.**
   - The app alternates between normal people, individuals, small teams, SMBs, enterprise, and API partners. The best first wedge seems like small teams collaborating on Office/docs/design files and currently emailing or renaming versions.

4. **Keep the “wrong abstraction” insight front and center.**
   - Michael Seibel says a good unique insight usually comes from customer conversations, product analysis, or personal experience, and should be specific rather than vague ([Seibel](https://www.michaelseibel.com/blog/how-to-pitch-your-company)).
   - Dropbox nails this with “online disk drive” and “manual uploading” being wrong abstractions.

5. **Fix the founder and legal hygiene.**
   - Replace “There’s a joke in here somewhere” with the actual solo-founder/cofounder situation.
   - Change “Who writes code?” from “No” to a direct answer naming Drew and any non-founder contributors.
   - Keep the Bit9/IP disclosure factual and crisp: attorney consulted, signed letter, no ownership claim.

6. **Demote future-feature speculation.**
   - Google Docs/offline sync is interesting, but it distracts from the working product. Keep it to one sentence after the core wedge is clear.

**Score**
Score: application `0.75-0.82`; interview read `0.65-0.75`; confidence medium; text-only, not an admissions prediction.

**Fun Fact**
YC explicitly says many accepted companies are very early: on average, 40% are just an idea and most do not have revenue. So lack of revenue is not the issue here; making founder speed and user pull obvious is ([YC FAQ](https://www.ycombinator.com/faq)).

**Tips**
- Lead with the simple product sentence. YC and YC-affiliated advice repeatedly favor plain, direct descriptions over impressive-sounding language; Seibel’s test is that a reader should quickly understand what you do ([Seibel](https://www.michaelseibel.com/blog/how-to-pitch-your-company)).
- Keep the demo prominent. Dropbox’s screencast/build link is a major strength, and it matches modern YC advice to include a demo even if rough ([YC demo advice](https://www.ycombinator.com/library/J8-yc-application-tips-include-a-demo)).
- Use the founder video separately from the demo. Modern YC says the application video should be one minute of founders talking, not a product demo ([YC video guide](https://www.ycombinator.com/video)).
- Avoid “kind of like Subversion, Trac and rsync” as the main explanation. It helps hackers, but normal-user workflow should come first.
- Do not use jokes in required factual fields. Use the “proposal v2 good revised NEW” joke only where the prompt asks for amusing/surprising.

**Office Hours**
- Before submitting, talk to 10-20 beta users and ask what they would be upset to lose, what they used before, and whether they would pay this month.
- Focus the next 6 weeks on proving retention and willingness to pay, not adding Google Docs sync.
- If SMBs are the target, try charging a few teams now. Even $20/month from 3 teams would sharpen the application more than another roadmap feature.
- Track one core metric: weekly active shared folders, retained synced devices, or teams with multiple active collaborators.

**Hygiene**
- Fix “How long have the founders known one another?” It currently does not answer the prompt.
- Fix “Who writes code?” The answer should name Drew and any non-founder contributors.
- Clarify whether there are cofounders. The current app reads inconsistently.
- Use `https://` links if available and make sure installer/demo links work without friction.
- Add a founder video if this is for a modern YC application; the demo video does not replace it.

**Questions**
1. How many beta users/teams are active, and how many have used Dropbox more than once in the last 7 days?
2. Is Drew actually solo, or are there other founders?
3. Has anyone offered to pay, paid, or asked for business/enterprise deployment?
4. Can you share the demo video or product walkthrough? This application depends heavily on whether the prototype makes “hit Save and everything works” obvious.
