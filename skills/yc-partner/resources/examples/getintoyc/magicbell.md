# MagicBell

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/magicbell/
- Author: Get into YC / public founder-submitted application
- Published: 2021-12-09
- Captured: 2026-06-16

## Summary

- Company: MagicBell
- Batch: 2021 Winter
- Application outcome: Successful
- Modified: 2021-12-09
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: In-app notification center for web & mobile apps
- Outcome label: Successful

## Content

### Company

#### [If you have a demo, what's the url? Demo can be anything that shows us how the product works. Usually that's a video or screen recording.](https://getintoyc.com/question/if-you-have-a-demo-whats-the-url-demo-can-be-anything-that-shows-us-how-the-product-works-usually-thats-a-video-or-screen-recording/)

https://www.youtube.com/watch?v=EeL-GcGmN7E&feature=youtu.be

#### [Describe what your company does in 50 characters or less.](https://getintoyc.com/question/describe-what-your-company-does-in-50-characters-or-less/)

In-app notification center for web & mobile apps

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

MagicBell is an out of the box, notification system with multi-channel delivery. Notifications are
created via the API and the embeddable notification center can be fully customized to match your
product's UI and UX. Companies with existing email notifications can simply bcc them to a project-
specific email address to roll out MagicBell to their users within 30 mins. You can think of it like
a smart router for your company's notifications to your customers.

MagicBell enables you to think in terms of users and respect their notification preferences, instead
of being bogged down by the complexity of understanding platform APIs for different channels.

#### [Where do you live now, and where would the company be based after YC?](https://getintoyc.com/question/where-do-you-live-now-and-where-would-the-company-be-based-after-yc/)

Barcelona. After YC, I'll continue operating from Barcelona. The business is a Delaware C-corp.

### Founders

#### [How many founders are on the team?](https://getintoyc.com/question/how-many-founders-are-on-the-team/)

1

#### [Which category best applies to your company?](https://getintoyc.com/question/which-category-best-applies-to-your-company/)

Developer Tools

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

We have a stable MVP delivering over a million notifications a month for two B2B apps. Here is
what's already deployed:

* The core APIs (notifications/preference management) * Javascript based In-app notification center
with real-time updates * Email source and delivery channel * Open-source libraries for React (to
build custom interfaces) and Ruby (for creating notifications and managing user preferences in
Ruby/Rails apps).

In terms of traction, we are signing up one enterprise lead a week through content on our blog.

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

About six months, of which the last month has been full time.

#### [Are people using your product?](https://getintoyc.com/question/are-people-using-your-product/)

Yes

#### [How many active users or customers do you have? If you have some particularly valuable customers, who are they? If you're building hardware, how many units have you shipped?](https://getintoyc.com/question/how-many-active-users-or-customers-do-you-have-if-you-have-some-particularly-valuable-customers-who-are-they-if-youre-building-hardware-how-many-units-have-you-shipped/)

* MagicBell is powering notifications for SupportBee, my previous company with over 500 enterprise
customers and 20,000 enterprise users. * We are live on another B2B product in the SaaS
collaboration space. They are using the free tier. * We are currently onboarding a series-A funded
insurance marketplace in Europe. They have signed a contract to bill them at $299/mo once they go
live in October.

#### [Do you have revenue?](https://getintoyc.com/question/do-you-have-revenue/)

Yes

#### [We're interested in your revenue over the last several months. (Not cumulative and not GMV).](https://getintoyc.com/question/were-interested-in-your-revenue-over-the-last-several-months-not-cumulative-and-not-gmv/)

August $999

#### [Anything else you would like us to know regarding your revenue or growth rate?](https://getintoyc.com/question/anything-else-you-would-like-us-to-know-regarding-your-revenue-or-growth-rate/)

The august revenue is committed but not yet realized since we are still waiting for our EIN to set
up our bank account and Stripe. We hope to have it all in place by the time YC sends out the
interview invites.

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

I am working on MagicBell because it's a problem faced universally by B2B apps, and one I have
experienced personally at my last company - SupportBee, a shared inbox product.

There, we deliver over a million notifications a month to our users. Before MagicBell, we spent a
significant amount of time writing code to figure out whom to notify (based on the activity and
their preferences), delivering the notification via email, and providing customer support when it
wasn't delivered timely. When our users asked for an in-app notification center and mobile push
notifications, we realized that we'd have to do a lot more work, especially if we wanted to avoid
duplicates across channels. We talked to other companies at our scale and validated that they
struggle with this problem too.

Instead of solving this problem just for SupportBee, we decided to build MagicBell.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Currently, the only substitute is building the notification system in-house. Based on our
experiences, and user interviews, it takes a team of two engineers (frontend+backend) and a designer
a minimum of two months to build a basic real-time notification center with multi-channel delivery.
The team needs to understand and use APIs from Twilio and Pusher, etc. Usage analytics, debugging
logs, fine-tuning the UX, or performing any day-to-day maintenance and troubleshooting is even more
work.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Twilio provides APIs for delivering notifications on different channels and hence could be
considered indirect competition. In fact, Twilio just participated in the Series A funding of XXX,
that's solving the same problem, albeit with a different approach.

It's possible that companies like Pusher or Onesignal offer a competing product in the future.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

In an ideal world, everyone would use our API from day one and skip building email notifications
entirely. However, today, most companies have already invested in their email notifications and are
reluctant to switch to a new API. We find that it's vital not to underestimate this inertia. To help
them migrate to MagicBell, without writing any code to talk to our API, we let them bcc their
existing email notifications to us and embed our notification center in their product. This setup
takes less than 30 mins. Over time they can start using the API to build new notifications. This
quick and low-risk way of delivering value to their users significantly reduces the friction of
adoption.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

We charge a subscription fee for MagicBell's APIs and UI components. The pricing depends on a
combination of the number of channels, active user count, notifications volume, and data retention
period. Given the business model and deep integration into our customers' code-base, we expect low
churn and healthy expansion revenue (150-200% YoY).

At an average revenue per account of $4k/mo and net revenue retention of 150%, we expect to make
$30million/yr in the next five years or so, given the right growth capital. The first-mover
advantage, combined with the growing market opportunity and our team's expertise in SaaS, makes this
a realistic target.

#### [How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?](https://getintoyc.com/question/how-will-you-get-users-if-your-idea-is-the-type-that-faces-a-chicken-and-egg-problem-in-the-sense-that-it-wont-be-attractive-to-users-till-it-has-a-lot-of-users-eg-a-marketplace-a-dating-site-an-ad-network-how-will-you-overcome-that/)

Our blog post describing the challenge of building a complete notification brings us one lead a
week. Given the search volume for relevant keywords, we plan to publish more valuable content to
double down on organic user acquisition.

Additionally, we are implementing several channels to generate growth - cold emails to targeted
companies, a freemium model with a MagicBell branded widgets and partnership with providers of
channel APIs (email/text/push). We hope to accelerate all these efforts with the additional funding
from YC.

### Legal

#### [Who writes code, or does other technical work on your product? Was any of it done by a non-founder? Please explain.](https://getintoyc.com/question/who-writes-code-or-does-other-technical-work-on-your-product-was-any-of-it-done-by-a-non-founder-please-explain/)

Hana (founder) is writing the code with Josue, core team member.

### Others

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

Restaurants and hotels spend an insane amount of money on electricity but obsess over keeping lights
turned off in toilets. Who hasn't found themselves in a dark toilet because the motion sensor
flicked the lights off while you were doing your business? :)

### Curious

#### [What convinced you to apply to Y Combinator? Did someone encourage you to apply?](https://getintoyc.com/question/what-convinced-you-to-apply-to-y-combinator-did-someone-encourage-you-to-apply/)

While I have a great team, as a transgender female founder, I lack the industry network to make this
business become the industry leader it can be. I can benefit tremendously from the advice,
connections, and support that YC offers.

#### [How did you hear about Y Combinator?](https://getintoyc.com/question/how-did-you-hear-about-y-combinator/)

I have been building tech companies since 2007 and known about YC since then. In 2012, I applied
with my last company (SupportBee) but didn't make it in.
