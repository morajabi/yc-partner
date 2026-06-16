# CommandBar

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/commandbar/
- Author: Get into YC / public founder-submitted application
- Published: 2024-06-21
- Captured: 2026-06-16

## Summary

- Company: CommandBar
- Batch: 2020 Summer
- Application outcome: Successful
- Modified: Unknown
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: Make web apps easier to navigate and learn.
- Outcome label: Successful

## Content

### Company

#### [Describe what your company does in 50 characters or less.](https://getintoyc.com/question/describe-what-your-company-does-in-50-characters-or-less/)

Make web apps easier to navigate and learn.

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

Foobar is a searchbar built into web apps that allows end-users to discover and actually execute
commands - not just search - straight from the searchbar. It comes as a configurable web component
that a front-end developer can start prototyping in minutes using our web interface. Foobar makes it
much easier for end-users to access the functionality they want wherever they are in your site, and
configuring Foobar is also much easier than trying to build a perfect UI that works for different
types of users (power users, new users, etc).

We believe Foobar will improve onboarding, feature discovery, and long-term usability for web apps,
ultimately driving better conversion and retention. As well as the web component, our tool includes
a web interface for maintenance (adding and updating commands), personalization (customizing who
sees what commands), and analytics (how Foobar is being used).

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

Not far.

We originally decided to build Foobar as a feature for a different web app that the 3 of us were
working on (https://codepost.io). While building it, we decided to turn it into a product -- a
component that could be used across sites and configured via a web interface -- instead of just a
codePost feature. While building our prototype, we have pitched Foobar to 4 apps: Kapwing
(https://www.kapwing.com/), StdLib (https://stdlib.com/), Plan (https://getplan.co/), and
Meetingbird (acq by Front) (https://meetingbird.com/). All 4 have committed to piloting Foobar (for
free).

We're about 2-3 weeks away from having our prototype ready to go live in these web apps. If that
goes well, we'll look to expand to 10-20 more apps (sourced from people we know and our network).

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

3 weeks, full-time. Before that, the 3 founders worked on a different project for the past 12
months, full-time: https://codepost.io, a web app used by CS teachers (mostly at universities) to
review student code. The 3 of us built the product and scaled it to 60 universities. (NB: we applied
to YC with codePost as our idea in 2016, but didn't start working on the project until early 2019).
When we realized Foobar had the chance to be a bigger company than codePost, we decided to pivot to
it full-time.

#### [Are people using your product?](https://getintoyc.com/question/are-people-using-your-product/)

Yes

#### [How many active users or customers do you have? If you have some particularly valuable customers, who are they? If you're building hardware, how many units have you shipped?](https://getintoyc.com/question/how-many-active-users-or-customers-do-you-have-if-you-have-some-particularly-valuable-customers-who-are-they-if-youre-building-hardware-how-many-units-have-you-shipped/)

Four companies have committed to piloting Foobar: Kapwing (https://www.kapwing.com/), StdLib
(https://stdlib.com/), Plan (https://getplan.co/), and Meetingbird (acq by Front)
(https://meetingbird.com/). An alpha is also live in our old company's site (codePost).

#### [Do you have revenue?](https://getintoyc.com/question/do-you-have-revenue/)

No

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

We originally decided to build Foobar into codePost because we were facing some UX challenges.
codePost is a relatively complex web app. Many of our users are power users; some spend 20+ hours a
week using it to review student code. We found it difficult to create a UI that made functionality
easily available to these power users in a way that was also accessible for new users. We were
inspired by other components we'd seen in the wild -- in Superhuman and Google Docs -- that allow
users to actually execute commands via text. We liked the idea of making functionality accessible
without matching GUI elements, and empowering users to easily find what they want to do instead of
churning, wading through help docs, or messaging us via in-app chat.

We decided to work on this full-time when we realized that (a) many web apps face the same problems
that Foobar solves, and (b) there was a lot of functionality we wanted to build into our Foobar that
we thought would be very valuable generally but tedious for others to build. Specifically,
functionality for easy configuration and maintenance, by-user personalization, and data mining.
(Foobar generates really valuable data, because users use it to express their intent around your
site.) The 3 of us (the founders) have domain expertise in building web apps, having spent the last
12 months building and scaling one full-time. We also know people, other web app developers, who
need it: we've pitched 4 so far, and plan to pitch more.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Foobar's job is to make web apps easier to learn and navigate. The most common substitute for Foobar
is to try to design a UI that works for all of your users, resorting to patterns like nested menus
and panels of buttons to handle complexity. Getting this right is obviously really hard. Another
common way to help users navigate a site is search, either home-grown or offered as a service by
vendors like Algolia. Search surfaces content, so doesn't work well in web apps that aren't
structured around hyperlinks or inventory.

Web apps may also resort to "customer success" tools. These include help centers, in-app chat, and
in-app product tours. Intercom is a vendor that offers all 3. Foobar doesn't replace these tools.
Depending on the query, the best path for the user to follow might be to execute the command within
Foobar, execute a related command within Foobar, read a help doc, or initiate a chat. Regardless, we
think Foobar is the best place for a user to start their "how do I do this" journey. In our
experience a user doesn't think "I really want to read a help doc right now": they just want to do
something. Starting with Foobar means a user can quickly find the next steps that gets them closest
to their goal.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

We don't have any unique advantage that prevents someone else from building a Foobar clone. We worry
most about search vendors and customer success vendors, who are solving a similar problem to Foobar.
Also, no-code development tools like Webflow might be able to disintermediate us if web apps are
built using their tool. Obviously we want to differentiate from potential clones by building a great
product. We also think we can build an accumulating advantage against clones (see below).

Another potential "competitor" is that apps will try to build something like Foobar themselves: a
simple command-line-lite GUI with a few actions. To compete against this competitor, we think we
need to make sure Foobar is better than a home-brewed version could be. We're doing this by making
Foobar easy for engineers and non-engineers to configure (adding and maintaining commands),
personalize (show different commands to different users based on personas), integrate with third-
party services (like help centers or APIs like Sendgrid's), and refine based on user data (e.g. A/B
test different commands). We think getting these steps right is key to unlocking value from Foobar,
and they probably exceed the buy vs. build threshold for most companies outside of very large ones.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

We didn't invent the idea of a searchbar that can execute actions. Some examples exist in the wild,
most notably Superhuman. Our unique insight is that this component should be a product that is
bought instead of a feature that is built.

We don't think others get this for three reasons.

(1) A searchbar that can execute actions can be useful in many, many web apps. Way more than have
built their own version to date.

(2) To get the most out of Foobar, you need users to be able to rely on it, just like search. That
means that they get used to pulling it up and finding what they want (or something that works) on
90%+ of searches. To make this happen, you need to be able to add lots of commands to Foobar, remove
ones that aren't working, and personalize responses so users see results that are most likely to be
relevant to them. This functionality is hard to build into a home-grown feature.

(3) It may seem hard to build a moat around a company that sells a "searchbar that can execute
actions", but we think there is an opportunity to build a defensible business here with a durable
competitive advantage. When an app uses Foobar, it creates a map of intents ("clear calendar for
today") to actions (code that actually updates user data), which is essentially an API. We could
make it possible for businesses using Foobar to expose commands they've built to other businesses
using Foobar. This functionality enjoys network effects: more customers means more potential
integrations. We could build a cross-site "meta-Foobar" that centralizes commands from all apps that
use Foobar, used by consumers. More consumers using meta-Foobar means Foobar is more valuable for
apps, which makes meta-Foobar more valuable for consumers, etc.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

If Foobar creates value for web apps (via better conversion and retention) and is easy to configure,
then we should be able to capture some of that value via a subscription fee.

The biggest possible market for Foobar is all internet businesses, since any website could benefit
from Foobar. The key question we need to better understand is: for what types of web apps is Foobar
substantially valuable? We think the answer is: most. Our heuristic is that any web app that is
complex enough to have a help center can probably benefit from Foobar. Even a relatively simple
ecommerce site could benefit by making it easier for users to access important actions like "add to
cart" or "shipping estimate." We plan to answer this question by pitching Foobar to a bunch of
different web apps and seeing where it sticks. If we can match the value proposition of incumbent
"customer success" vendors (like Intercom) then we could charge on the order of what they charge:
$100 to $1000 dollars per month.

#### [How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?](https://getintoyc.com/question/how-will-you-get-users-if-your-idea-is-the-type-that-faces-a-chicken-and-egg-problem-in-the-sense-that-it-wont-be-attractive-to-users-till-it-has-a-lot-of-users-eg-a-marketplace-a-dating-site-an-ad-network-how-will-you-overcome-that/)

First, we'll continue to do what we're doing right now: implementing our prototype Foobar in our own
web app (codePost) and pitch our peers (other web app developers we know or can get connected to) to
have them try it out.

This means "high CAC" initially but it also means we can discover the niches in which Foobar
resonates most strongly and focus our engineering efforts on those niches. The early-adopter niche
might be defined by end-user-type (e.g. lots of power users), app type (e.g. high complexity), or
some characteristic of the development team (e.g. a team that likes to ship lots of new features).

The tough times imposed by COVID-19 may make it harder for us to get users because businesses are
less likely to have spare engineering cycles to implement it, and may be hesitant to spend on a new
tool. To combat these forces, we plan to focus on making it possible for non-developers to configure
Foobar, and to build case studies demonstrating the ROI a web app can achieve with Foobar. The lack
of spare engineering cycles could play to our advantage too: companies will probably be less
interested in building their own Foobars if they see value in the concept.

We do have one idea to scale Foobar faster. We're building a chrome extension to allow end-users to
build a basic Foobar for themselves on top of any app. Usage data (who is using Foobar for what
apps, and how they are using it) should help us understand our early adopter niche. It also gives us
a powerful sales pitch: "look how many people are already using Foobar for your site!"
