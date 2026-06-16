# Proxino (Taazr)

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/proxino-taazr/
- Author: Get into YC / public founder-submitted application
- Published: 2021-10-31
- Captured: 2026-06-16

## Summary

- Company: Proxino (Taazr)
- Batch: 2010 Summer
- Application outcome: Successful
- Modified: Unknown
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: Detect bugs in live web applications through a statistical inference.
- Outcome label: Successful

## Content

### Company

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

Taazr detects bugs in live web applications through statistical inference.

Think of a web application as a black box, with its inputs as HTTP requests and its outputs as HTTP
response data. After a client instruments her web app with our javascript, Taazr will collect
request/response data to build a model of expected behavior. When an "anomalous" response is
detected, we notify our client, sending along details about the potentially faulty request/response
pair.

### Founders

#### [Please tell us about an interesting project, preferably outside of class or work, that two or more of you created together. Include urls if possible.](https://getintoyc.com/question/please-tell-us-about-an-interesting-project-preferably-outside-of-class-or-work-that-two-or-more-of-you-created-together-include-urls-if-possible/)

For a mobile development class, we created a Barefoot Running application[1] for the iPhone. The app
allows users to report and view the location of glass shards - centralized in an off-site database -
and keeps track of speed and distance data throughout a run.

We also jointly created BijectKarma, a community connecting designers and developers[2]. We had
trouble attracting initial users, however, and the site was taken offline.

#### [Please tell us in one or two sentences about something impressive that each founder has built or achieved.](https://getintoyc.com/question/please-tell-us-in-one-or-two-sentences-about-something-impressive-that-each-founder-has-built-or-achieved/)

Ethan was admitted to CS PhD programs at Stanford, Berkeley, and MIT for research on automatic
software development (e.g. automatically finding bugs, fixing bugs, generating test suites).

Muzzammil is a member of the core development team for GuardRails, a secure web application
framework, which will be published at USENIX 2011 and presented at RubyNation. He is also the
founder of Wahoobooks, a site where U.Va. students can list used textbooks.

#### [Please tell us about the time you most successfully hacked some (non-computer) system to your advantage.](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

A Computer Science degree from U.Va. typically requires that you complete many courses within a
variety of unrelated disciplines. Most of our peers must take classes in Physics, Chemistry, and a
"fake" humanities listing called Science, Technology and Society. We escaped such requirements
through a little-known option to pursue a BA in Computer Science, in place of the Engineering
School's BS. With this degree, we completed the core CS curriculum and any other classes that caught
our interest, but we avoided the rigidly defined ABET requirements of the Engineering school. This
left us more time to pursue research and hack on web applications.

#### [How long have the founders known one another and how did you meet? Have any of the founders not met in person?](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

1.5 years. Ethan was Muzzammil's TA.

While working on a problem set, Muzzammil mentioned his interest in startups. Ethan asked if he had
heard of Y Combinator, which of course Muzzammil had. As it turned out, we were both fishing for
potential co-founders.

### Idea

#### [Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?](https://getintoyc.com/question/why-did-you-pick-this-idea-to-work-on-do-you-have-domain-expertise-in-this-area-how-do-you-know-people-need-what-youre-making/)

Finding and fixing software bugs is expensive. Taazr will save companies time and money by
identifying bugs and potential fixes in web applications. We chose to work on Taazr primarily due to
our familiarly with related research fields, but also because it represents a challenging problem.

Ethan has two years of experience hacking with the Automatic Program Repair (APR) research group at
U.Va, where he's worked with state-of-the-art techniques in program analysis, testing, and
statistical debugging. He has published work increasing the efficiency and scalability of APR.

Muzzammil has a year of experience with the GuardRails research group at UVA, where he helped create
a secure web framework for Ruby on Rails. His work is published in USENIX 2011 and will also be
presented at RubyNation.

More generally, Taazr was inspired by the Cooperative Bug Isolation Project [2], in combination with
ideas gleaned from our respective research groups at U.Va.

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Uncaught program bugs are expensive, and for this reason, good developers take care in testing their
code. However, even the best test suites will not catch all program bugs. Taazr will identify such
bugs earlier in the development cycle, and companies will save money that otherwise might have been
spent on code maintenance and customer support.

We believe that statistical debugging is uniquely suited to web applications, due to the relative
ease with which web apps can be instrumented through lightweight and unobtrusive javascript. While
statistical debugging has succeeded in a research context on desktop software, automatically finding
bugs in live web applications remains an open industrial problem.

However, our ultimate aim is not just to find bugs in web applications, but also to fix them. This
will likely require tighter integration - server-side - between our tools and a developer's code.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Coverity and Klocwork also find program bugs, but they don't target web applications. Moreover,
engineers use their products throughout the development process, whereas Taazr operates,
automatically, on live production code.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

Writing code is much like putting words to paper, an act of creation. When you write, it is
important to spell things correctly, but few writers spend much time on this task, for they have
spellcheckers. We think that testing should be just as straightforward. It is quite important, but
should not monopolize your attention.

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

Taazr will charge clients monthly. We see a market opportunity in the tens of millions.

### Others

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

You can start small word-memes among family and friends. Choose a word that is fairly obscure (but
not obviously so), something like pedantic, sycophant or obsequious. Over a few days, casually
inject it into conversation.

Listen throughout the next week. The word will come up with surprising frequency. You can also do
this with unique inflections, and distinct rhythms of speech.
