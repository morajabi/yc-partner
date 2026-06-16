# Standard Treasury

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/standard-treasury/
- Author: Get into YC / public founder-submitted application
- Published: 2021-10-09
- Captured: 2026-06-16

## Summary

- Company: Standard Treasury
- Batch: 2013 Summer
- Application outcome: Successful
- Modified: 2021-10-22
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: Offers standard APIs that facilitate businesses in transfers and other transactions with banks.
- Outcome label: Successful

## Content

### Company

#### [If you have a demo, what's the url? Demo can be anything that shows us how the product works. Usually that's a video or screen recording.](https://getintoyc.com/question/if-you-have-a-demo-whats-the-url-demo-can-be-anything-that-shows-us-how-the-product-works-usually-thats-a-video-or-screen-recording/)

No online demo yet. It might be awhile before we have a dashboard and mocking up a fake API for you
doesn't seem worth it.

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

We are building APIs for commercial banking services by building on top of multiple large banks.

If someone needs advice they can call Goldman. If they just need to transact then they can use one
of our APIs. We will build commercial banking middleware that will sit on top of banks just like
Twilio sits on top of multiple phone carriers. It is much easier because we'll have (mostly) RESTful
APIs with good documentation, etc, and (if we choose) cheaper because of bulks rates.

1) Delivered programmatically, using good APIs - Anything transactional shouldn't involved a human
being. Most banks suck at technology and admit that. They're excited to have us resell their
services.

2) Narrow to start, but ultimately broad services - We want to abstract away the pain of dealing
with banks for transactional services like ACH, F/X, wires, factoring, short-term loans, etc, just
as Stripe, Braintree, and others have done for getting a Merchant ID. We are starting with ACH and
F/X as foundational products.

3) Multiple banking partners - We're willing to endure the pain of setting up commercial contracts
with many banks and then offering the transactional services (via API) in an intelligently routed
way. We've gotten verbal agreement from Wells Fargo, and are pretty far along with JPMorgan and
Capital One. Will start with other banks shortly.

#### [Where do you live now, and where would the company be based after YC?](https://getintoyc.com/question/where-do-you-live-now-and-where-would-the-company-be-based-after-yc/)

SF. SF.

### Founders

#### [Please tell us about an interesting project, preferably outside of class or work, that two or more of you created together. Include urls if possible.](https://getintoyc.com/question/please-tell-us-about-an-interesting-project-preferably-outside-of-class-or-work-that-two-or-more-of-you-created-together-include-urls-if-possible/)

http://deciens.com/ We raised the money, we have made investments. We have been to YC demo days and
invested in Keychain Logistics.

#### [Please tell us in one or two sentences about something impressive that each founder has built or achieved.](https://getintoyc.com/question/please-tell-us-in-one-or-two-sentences-about-something-impressive-that-each-founder-has-built-or-achieved/)

ZT reorganized child welfare investigations in New York City. He got tons and tons of data, wrote R
code to analyze it, set up ethnographic research conducted by his team, etc. He sniffed out details,
wrote a report, and then helped implement the changes to a staff of 2000, and a budget in the tens
of millions.

Dan built Giftly, particular the proprietary stored value product, from a regulatory, legal, risk,
etc, perspective.

#### [Please tell us about the time you most successfully hacked some (non-computer) system to your advantage.](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

When I started in Newark, I didn't have a computer or an email, and City Hall didn't have wireless.
So I tracked down one of the wireless networks I could find - owned by a bails bondsman close to the
court, and negotiated with them for their wireless password.

I once spent hours looking at floorplans and historic housing lottery data so that my roommate and I
could pick a HUGE double with our own bathroom despite having a terrible pick at Brown.

#### [How long have the founders known one another and how did you meet? Have any of the founders not met in person?](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

We've known each other since we were 16, when met at Harvard summer school.

#### [Do any founders have other commitments between X and Y inclusive?](https://getintoyc.com/question/do-any-founders-have-other-commitments-between-x-and-y-inclusive/)

No.

#### [Do any founders have commitments in the future (e.g. finishing college, going to grad school), and if so what?](https://getintoyc.com/question/do-any-founders-have-commitments-in-the-future-eg-finishing-college-going-to-grad-school-and-if-so-what/)

No.

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

We're far along on regulatory/commercial contract/legal stuff. Once we have that settled, there is a
lot of backend, unsexy stuff to do to make it as pretty/smooth as we'd like: settlement files over
SFTP, testing required by the banking partner, automatic underwriting built on
Microbilt/LexusNexus/Iovation, etc, and then launch.

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

Pre-development. We've incorporated. I'm still at Stripe. Dan's still at Giftly. It didn't make
sense to start until one of the banks signalled a willingness to sign a commercial agreement as
their was nothing to integrate with. Ready to start now. Raising money because of non-trivial
commercial and regulatory costs. Far along with recruiting the rest of the early team and
considering raising a seed round.

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

We started by thinking about ACH, which is a problem that Dan actually had in his work. Zac sees how
hard it is for even Stripe to deal with Wells Fargo on F/X, wires, etc.

Dan knows a ton about payments. Zac won finance prizes @ Brown. We both want to disrupt banking and
have been talking about it for years.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

When most businesses wants to do something financial they have to call their bank and talk to a
person - except for getting a MID. That doesn't make sense. Getting a wire, as an example, often
involves twenty minutes, a painful conversation, and $30. Even non-quant hedge funds needing to
convert EURO to GBP have to pick up the phone and talk to a bank's trading desk.

No one has built developer friendly bank back-end processing, so you have to deal with banks, which
overcharge, are slow, and are not developer friendly. Wells Fargo, for example, does offers an API
which costs more than their other options and, well, is not very good.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Possible competitors: Square, Stripe, Braintree, Wells Fargo, JP Morgan, Bloomberg, Intuit, PayPal

Banks cannot innovate on technology. A senior exec at JPMC told us that even if building good APIs
was a Jamie Dimon priority it couldn't get done before 2017.

Commercial banking broadly - including every service we're imagining other than ACH (F/X, Wires,
Factoring, Lending, Account Creation/Deletion, etc) - is not something that the innovative payments
companies plan to provide to others, although they're all services they, themselves, need. Stripe,
for example, is trying to make payments work on the web. We're trying to make commercial banking
work in the world. They're both trillion dollar problems, but they're different.

So, who do I fear most? I fear regulators the most. Banks can't beat us on technology but we might
be so successful they beat us with the law.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

People who run banks don't care about providing high quality technology services, and the people who
care about technology don't want to work with (or buy) a bank. Schlep blindness, as it were.

Also, there is great power in abstracting away thinking about your particular bank. Take ACH: since
we are willing to suffer through forming eight banking relationships, we can provide next-day
payouts to 80% of checking accounts in the US. Everyone else can only do next-day payouts on their
one bank.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

We make money on transactions.

For a (very, very) rough guide, profits at ten biggest banks last year were $120b. Let's call 50% of
that transactional/FICC/pure commercial banking as we define it.

As for TAM, SAM, SOM, using big-O:

Total addressable market: O(100s of billions)

Serviceable available market through APIs: O(10s of billions)

Share of market: O(10s of billions)

#### [How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?](https://getintoyc.com/question/how-will-you-get-users-if-your-idea-is-the-type-that-faces-a-chicken-and-egg-problem-in-the-sense-that-it-wont-be-attractive-to-users-till-it-has-a-lot-of-users-eg-a-marketplace-a-dating-site-an-ad-network-how-will-you-overcome-that/)

Working the network, undercutting others on price and (especially) ease, directly reaching out to
every startup that needs banking services beyond payments that exists or is founded for traction.

We've focused our user research on three customer segments: (a) Corporate treasury departments (a
heretofore undisrupted part of most enterprises) (b) hedge, private equity, and venture funds (minus
quants/HF) and their back offices (c) technically inclined SMEs and startups who aren't served well
by big banks.

### Legal

#### [Are any of the founders covered by noncompetes or intellectual property agreements that overlap with your project? If so, please explain.](https://getintoyc.com/question/are-any-of-the-founders-covered-by-noncompetes-or-intellectual-property-agreements-that-overlap-with-your-project-if-so-please-explain/)

We both have CIIAA's that could cover this work.

Dan's company is pretty far away.

Zac declared this idea when he signed his at Stripe. He's asked Stripe for an IP waiver letter, or
whatever it's called.

(I also described this entire idea in a youtube video I sent to you in December before we didn't
accept a late interview, so...there is a lot of documentary evidence that I had this IP before
Stripe).

#### [Who writes code, or does other technical work on your product? Was any of it done by a non-founder? Please explain.](https://getintoyc.com/question/who-writes-code-or-does-other-technical-work-on-your-product-was-any-of-it-done-by-a-non-founder-please-explain/)

No. (Our code was not written by a non-founder)

### Others

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

"The failure, if it was one, lay in the fact that, having too much to hold on to, they slowly lost
what they had. On the whole, it was those who had least who were able to move most freely to the new
world which was coming into existence." --That reading The Making of the Middle Ages can make you
think of everything from startups to the state of America in the world (this happened in December)
