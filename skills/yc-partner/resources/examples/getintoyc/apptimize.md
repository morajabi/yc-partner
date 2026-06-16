# Apptimize

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/apptimize/
- Author: Get into YC / public founder-submitted application
- Published: 2021-10-09
- Captured: 2026-06-16

## Summary

- Company: Apptimize
- Batch: 2013 Summer
- Application outcome: Successful
- Modified: 2021-10-22
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: A platform that empowers product teams to efficiently run A/B tests.
- Outcome label: Successful

## Content

### Company

#### [If you have a demo, what's the url? Demo can be anything that shows us how the product works. Usually that's a video or screen recording.](https://getintoyc.com/question/if-you-have-a-demo-whats-the-url-demo-can-be-anything-that-shows-us-how-the-product-works-usually-thats-a-video-or-screen-recording/)

yc.apptimize.com/admin

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

Apptimize lets you AB test mobile applications. You keep the native experience without needing to
push changes blindly or rely on users to update. There's a web interface to manage experiments, and
a WYSIWYG interface for non-programmers. Apptimize removes the pain of designing a controlled
experiment, serving variations, collecting results, and calculating statistical significance. Right
now you have to be a developer and statistician to AB test a mobile app, but we make it so that non-
programmers can AB test too. Apptimize makes optimization as easy for mobile as it is for web.
Apptimize technology could transform the process of testing and pushing changes and be integrated
into 100% of apps.

### Founders

#### [Please tell us about an interesting project, preferably outside of class or work, that two or more of you created together. Include urls if possible.](https://getintoyc.com/question/please-tell-us-about-an-interesting-project-preferably-outside-of-class-or-work-that-two-or-more-of-you-created-together-include-urls-if-possible/)

We prototyped an app called Firesale that helps people sell unwanted stuff. To create a market of
buyers, we brought on full-time Craigslist market makers. The Craigslist expert users complained
about the process of being first to email a poster, so we optimized the messaging to make
transacting as fast for them as possible. They also complained about Craigslist lacking a
reputation/identity system, so we implemented one. We put Firesale on hold to work on Apptimize.

#### [Please tell us in one or two sentences about something impressive that each founder has built or achieved.](https://getintoyc.com/question/please-tell-us-in-one-or-two-sentences-about-something-impressive-that-each-founder-has-built-or-achieved/)

Nancy: trader who ran the Fixed Income Quantitative Strategies team at GETCO (GETCO grew from 100 to
500 people to become the premiere algorithmic trading company); world class expert in Fixed Income
trading and exchanges.

Jeremy: owned IndexedDB (the emerging w3c standard for storing data in a browser) within Chrome;
edited the spec, worked closely with Mozilla and Microsoft on the design, and wrote most of the
initial implementation in Chrome/WebKit; simultaneously started the London Chrome team.

#### [Please tell us about the time you most successfully hacked some (non-computer) system to your advantage.](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

Nancy wanted to work in the Middle East but there wasn't a culture of internships. Nancy discovered
if she didn't mention she was just a sophomore she could interview as a consultant (and get a
company car and phone). She was the first student ever hired for Mercury's R&D office in Israel (a
load testing company acquired by HP).

At Google, Jeremy became an expert in free travel. After getting on shortlists for university
recruiting, he positioned himself as a datacenter expert and visited many across America. After
targeting developer relations, Jeremy got on the shortlist for places like Moscow, Berlin, Manila,
Singapore, Sydney, and Tokyo, giving talks, meeting partners, and exploring- all for free.

#### [How long have the founders known one another and how did you meet? Have any of the founders not met in person?](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

We met a couple years ago through mutual friends and started working together when Jeremy convinced
Nancy to leave NYC for the Bay.

#### [If we fund you, which of the founders will commit to working exclusively (no school, no other jobs) on this project for the next year?](https://getintoyc.com/question/if-we-fund-you-which-of-the-founders-will-commit-to-working-exclusively-no-school-no-other-jobs-on-this-project-for-the-next-year/)

Nancy and Jeremy are committed to exclusively working on Apptimize for the next few years.

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

Apptimize works and we just launched our private beta this week! We have 100+ signups but we only
accepted 2 friends this week because we are working closely with our first customers to shape the
future of our product.

The beta has the Android library, a website dashboard to manage experiments, and a results page
showing statistics and conclusions. The WYSIWYG interface will be ready in a few weeks. Our research
suggested starting with Android because Android developers rely on freemium (compared to iOS who
make a lot off premium) and want to AB test to optimize in-app purchases, etc. Our iOS version is
coming in a few weeks.

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

We started in January, and Apptimize is currently ~8K lines of code (not including libraries, html,
or css) and works end-to-end. The frontend is JS, CSS, and Angular. We're on EC2 mainly using
PostgreSQL, nginx, and Netty/Java.

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

We picked this idea because Jeremy had looked for a mobile AB testing solution when working on
Drawchat, but couldn't find one. Three 50+ people companies, 3 YC companies, and 10+ indie
developers have signed up to beta test our product. All the programmers/contractors we've
interviewed have also asked to sign up for our private beta. This is an immediate need for most
mobile companies.

Nancy is an expert in experiment design and data analysis. Jeremy is an expert in mobile and has
built many efficient, scalable backends. We both love being data driven and view life as an
experiment.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Most wait for app store approval and push many changes simultaneously. They eyeball the results and
haphazardly rollback suspect changes.

Desperate people resort to basic, home-grown solutions. Because of other projects, Switchboard and
Clutch.io evolved incomplete solutions (we noticed errors: randomization mistakes that mess up the
experiments, poor error handling, malformed responses that'd crash your app!).

There hasn't been much focused effort towards creating a seamless AB testing experience for native
apps. AB testing for mobile is a technologically harder problem than for websites due to challenges
particular to mobile devices (ie. intermittent internet, lack of cookies/iframes, users running
different versions). Existing solutions ignore complexity whereas we view handling it as our core
business.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Several companies very recently entered the game. Swrve has so far focused on games. Pathmapp is
focusing on overall analytics (pretty different from our approach). Abstate is unlaunched. Artisan
and Arise.io have buggy, immature products. A risk is that Visual Website Optimizer or Optimizely
will decide to focus on expanding from websites into native apps. Native might be a natural next
step for them since they offer web app support in premium plans, so we'll grow aggressively.

We think there's no dominant player because nobody has made anything good yet. Our goal is to be the
best.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

Our competitors are developers building for other developers, so most only offer programmatic
interfaces. We understand often the goal setters and decision makers aren't programmers. Apptimize
makes it simple for non-technical owners, product managers, designers, and marketers via a WYSIWYG
interface and a website to control and create experiments.

Our experimental setup, results, and analysis will be superior. Stanford PhD's helped with our
statistics by pointing out problems with competitors' setups (ie. fixed sample sizes, small data set
handling).

We'll target companies who don't monetize through app sales, instead using apps for branding,
coupons, other off-app conversions. Although our first users are indie developers, most profitable
apps make < $2K per month, so we'll grow to targeting corporations like United, Starbucks.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

The plan is a monthly subscription. We'll offer customers help with experiment design. If we charge
premium customers $1K per month and get 200 customers (less than 2 sales a week) over 2 years we'd
make ~$2.4MM per year 2 years in. Artisan (launched this month) claims to charge $1K-$10K per month,
so that's possibly a better price.

Ultimately we want to be the default way people change their apps. Everyone would use Apptimize to
test each idea, and then use Apptimize to deliver the change to users. 100% of apps would use our
library to reduce time to propagate changes and tighten the app development cycle. We'd help erase
the line between apps and the web.

#### [How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?](https://getintoyc.com/question/how-will-you-get-users-if-your-idea-is-the-type-that-faces-a-chicken-and-egg-problem-in-the-sense-that-it-wont-be-attractive-to-users-till-it-has-a-lot-of-users-eg-a-marketplace-a-dating-site-an-ad-network-how-will-you-overcome-that/)

Our first customers are our friends' startups. To target our next customers, we downloaded their
apps and their competitors' apps and are designing experiments for them. If they find the pre-
designed experiments useful, they can easily start testing with those the instant they sign up.

We'll offer customer referral rewards such as temporary premium memberships. We also want to make it
easy to see and implement case study results by suggesting experiments to potential users. For
marketing, we will ask and answer stackoverflow and Quora questions regarding how people AB test on
mobile.

We could partner with companies in related fields like App Annie or Parse.

### Others

#### [If you had any other ideas you considered applying with, please list them. One may be something we've been waiting for. Often when we fund people it's to do something they list here and not in the main application.](https://getintoyc.com/question/if-you-had-any-other-ideas-you-considered-applying-with-please-list-them-one-may-be-something-weve-been-waiting-for-often-when-we-fund-people-its-to-do-something-they-list-here-and-not-in-the-main-application/)

EEG machine to read babies' minds. We like playing with our Emotiv machine, know prominent
MIT/Stanford researchers, and see parallels between EEG analysis and high frequency market data for
financial instruments (both systems produce massive amounts of data that seem random but aren't).

A page-less browser using crowdsourcing. It'd show logical dependencies, assumptions, relationships
between ideas, and best arguments for and against each belief.

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

People think it's red, but no one knows the best button color.
