# Courier

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/courier/
- Author: Get into YC / public founder-submitted application
- Published: 2023-04-21
- Captured: 2026-06-16

## Summary

- Company: Courier
- Batch: 2019 Summer
- Application outcome: Successful
- Modified: 2023-04-21
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: A single API for multi-channel user notifications.
- Outcome label: Successful

## Content

### Company

#### [Describe what your company does in 50 characters or less.](https://getintoyc.com/question/describe-what-your-company-does-in-50-characters-or-less/)

A single API for multi-channel user notifications.

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

Courier makes it easy to add multiple channels for user notifications. Think of how Slack or Twitch
intelligently route notifications to the right medium - if you're active in your browser it shows it
via browser push, if you're idle it'll send it to mobile push, or it can always fall back on email.
Courier also makes it easy to add emerging notification channels like notifying users within their
own Slack organization, via your instance of Intercom, or over a messaging channel like WhatsApp.
Finally Courier can further reduce engineering costs by delivering out-of-the-box UI kits for
managing notification preferences and subscribing to content.

#### [Where do you live now, and where would the company be based after YC?](https://getintoyc.com/question/where-do-you-live-now-and-where-would-the-company-be-based-after-yc/)

San Francisco

### Founders

#### [Please tell us in one or two sentences about something impressive that each founder has built or achieved.](https://getintoyc.com/question/please-tell-us-in-one-or-two-sentences-about-something-impressive-that-each-founder-has-built-or-achieved/)

Over a two year period my team and I rebuilt the legacy experience of Eloqua by adding a new REST
API atop the legacy .NET codebase and building one of the first enterprise Single Page Applications
to power our new UI/UX in 2010. We leveraged our new UX to win deals we were previously losing to
Marketo, took the company through an IPO, and ultimately sold it to Oracle where it is now the
Oracle Marketing Cloud.

#### [Do any founders have commitments in the future (e.g. finishing college, going to grad school), and if so what?](https://getintoyc.com/question/do-any-founders-have-commitments-in-the-future-eg-finishing-college-going-to-grad-school-and-if-so-what/)

None.

#### [Which category best applies to your company?](https://getintoyc.com/question/which-category-best-applies-to-your-company/)

Developer Tools

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

I have an early prototype that is not yet ready for release.

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

I have been working on Courier since roughly New Years Eve; none of that time has been full-time. I
go full-time on Courier starting this Monday, April 1.

#### [Are people using your product?](https://getintoyc.com/question/are-people-using-your-product/)

No

#### [When will you have a prototype or beta?](https://getintoyc.com/question/when-will-you-have-a-prototype-or-beta/)

Friends & family MVP by end of April, public beta by end of May.

#### [Do you have revenue?](https://getintoyc.com/question/do-you-have-revenue/)

No

#### [If you are applying with the same idea as a previous batch, did anything change? If you applied with a different idea, why did you pivot and what did you learn from the last idea?](https://getintoyc.com/question/if-you-are-applying-with-the-same-idea-as-a-previous-batch-did-anything-change-if-you-applied-with-a-different-idea-why-did-you-pivot-and-what-did-you-learn-from-the-last-idea/)

N/A

#### [If you have already participated or committed to participate in an incubator, "accelerator" or "pre-accelerator" program, please tell us about it.](https://getintoyc.com/question/if-you-have-already-participated-or-committed-to-participate-in-an-incubator-accelerator-or-pre-accelerator-program-please-tell-us-about-it/)

N/A

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

At Winmore we developed a collaboration feature for users to work together using tools like real-
time chat on RFPs they are pursuing. We struggled to make user notifications as smooth of an
experience as what we were used to out of our preferred tools, e.g. Slack. As head of both
engineering and product I searched for a solution to this but all existing solutions are either too
limited (only a couple of channels) or too focused on the marketing use-case instead of
product/engineering usage.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Most companies that support multi-channel notifications have to build that support internally.
Twitch just launched their "Smart Notifications", built by an internal engineering team. Existing
multi-channel offerings (Amazon Pinpoint, Twilio Notify, etc.) usually only support a couple of
channels - and they only support themselves as providers for those channels. Courier is agnostic to
the underlying provider, similar to Segment, Zapier, etc.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Competitors line up in two categories: marketing focused, such as Iterable (https://iterable.com/),
and engineer focused, such as Twilio Notify. Iterable is easily the most robust competitor in this
space, but is focused on a different buyer persona and thus a different set of features. With the
acquisition of SendGrid, I expect Twilio to re-invest in this space in the future - currently Twilio
Notify is not a compelling product. I still expect whatever solution Twilio brings to market to be
Twilio+SendGrid-centric rather than open to many providers, but given their dominance in both of
those respective channels, they're certainly who I fear the most.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

The applicability of the Segment or Stripe playbooks of locking in new startups while they're young
and looking for an easy implementation-path and then scaling revenue commensurately as their revenue
grows is huge, and is different from the martech playbook competitors like Iterable are running.
This playbook requires targeting engineers looking for fast solutions to common early problems as
well as features that let you scale pricing and penetration within those customers as they
themselves grow.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

Courier has three paid pricing plans that discriminate based upon the number of notifications sent
per month. This maps to how incumbent single-channel notification providers charge and I expect
Courier to be able to charge prices comparable to a single-channel provider. The customer will be
paying for both Courier and the underlying providers so it may result in Courier only being able to
charge some fraction of a comparable single-channel provider.

There are at least two existing individual channels that support $100M+ ARR (and in some cases much,
much more) and two more supporting $10M+ ARR in revenue for the leader(s) in that space: email
(SendGrid), SMS (Twilio), mobile push (Amazon SNS, OneSignal, Urban Airship), browser push (Pusher).
Achieving revenues in excess of $100M ARR is achievable.

#### [How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?](https://getintoyc.com/question/how-will-you-get-users-if-your-idea-is-the-type-that-faces-a-chicken-and-egg-problem-in-the-sense-that-it-wont-be-attractive-to-users-till-it-has-a-lot-of-users-eg-a-marketplace-a-dating-site-an-ad-network-how-will-you-overcome-that/)

Content marketing and developer relations to attract engineers who are tasked with adding
notifications to their products.

### Equity

#### [Have you incorporated, or formed any legal entity (like an LLC) yet?](https://getintoyc.com/question/have-you-incorporated-or-formed-any-legal-entity-like-an-llc-yet/)

No

#### [What kind of entity and in what state or country was the entity formed?](https://getintoyc.com/question/what-kind-of-entity-and-in-what-state-or-country-was-the-entity-formed/)

Delaware C Corp

#### [Please describe the breakdown of the equity ownership in percentages among the founders, employees and any other stockholders. If there are multiple founders, be sure to give the equity ownership of each founder.](https://getintoyc.com/question/please-describe-the-breakdown-of-the-equity-ownership-in-percentages-among-the-founders-employees-and-any-other-stockholders-if-there-are-multiple-founders-be-sure-to-give-the-equity-ownership-of-each-founder/)

100% owned by myself.

#### [Please provide any other relevant information about the structure or formation of the company.](https://getintoyc.com/question/please-provide-any-other-relevant-information-about-the-structure-or-formation-of-the-company/)

100% of issued shares owned by Troy Goode (myself). Stripe Atlas' standard configuration.

### Legal

#### [Are any of the founders covered by noncompetes or intellectual property agreements that overlap with your project? If so, please explain.](https://getintoyc.com/question/are-any-of-the-founders-covered-by-noncompetes-or-intellectual-property-agreements-that-overlap-with-your-project-if-so-please-explain/)

I am covered by a standard (for California / Bay Area) Inventions Assignment document for my current
employer relevant to any competing technology, work done on company time, or on company
resources/hardware until the end of this week. Starting this Monday, April 1 I am full-time on
Courier and not covered by any IP agreement.

#### [Who writes code, or does other technical work on your product? Was any of it done by a non-founder? Please explain.](https://getintoyc.com/question/who-writes-code-or-does-other-technical-work-on-your-product-was-any-of-it-done-by-a-non-founder-please-explain/)

All technical work has been performed by myself.

#### [Is there anything else we should know about your company?](https://getintoyc.com/question/is-there-anything-else-we-should-know-about-your-company/)

None

### Others

#### [If you had any other ideas you considered applying with, please list them. One may be something we've been waiting for. Often when we fund people it's to do something they list here and not in the main application.](https://getintoyc.com/question/if-you-had-any-other-ideas-you-considered-applying-with-please-list-them-one-may-be-something-weve-been-waiting-for-often-when-we-fund-people-its-to-do-something-they-list-here-and-not-in-the-main-application/)

A more abstract version of Courier that I have considered is an OEM integrations provider. Think:
embeddable Zapier or IFTTT. B2B applications often need to let their users enable integrations
between their service and other services, but this is built by hand today. Tools like Zapier or
IFTTT are currently focused on enabling the end-user, but not on letting a SaaS provider easily
offer certain out-of-the-box integrations.

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

When I incorporated Courier via Stripe Atlas in January, it was the middle of the government
shutdown. Atlas uses Rocket Lawyer to file the necessary paperwork, including for your EIN. After
some time it became clear that my EIN was taking longer than anticipated to arrive so I checked in
with the folks at Stripe, who then checked in with Rocket Lawyer - turns out any 3rd-party agent
registering an EIN on behalf of someone else must do so with the IRS via fax. With the government
shutdown the fax lines were also down; I suppose there was simply nobody there to pick up whatever
papers were arriving at the fax machine!

Rather than wait through what was expected to be at least a multi-week delay after the government
opened back up, I instead used the IRS website to apply for my EIN. It was free, took roughly 30
seconds, and the EIN document was emailed to me within a minute or two...
