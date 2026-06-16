# Dropbox

- Type: Public YC application example
- Status: Public example application from Get into YC
- URL: https://getintoyc.com/company/dropbox/
- Author: Get into YC / public founder-submitted application
- Published: 2021-07-21
- Captured: 2026-06-16

## Summary

- Company: Dropbox
- Batch: 2007 Summer
- Application outcome: Successful
- Modified: 2021-11-10
- Captured only because Get into YC labels this application as Successful.
- Recognized email addresses were redacted.
- Description: A cloud storage service that lets you save files online and sync them to your devices.
- Outcome label: Successful

## Content

### Company

#### [If you have a demo, what's the url? Demo can be anything that shows us how the product works. Usually that's a video or screen recording.](https://getintoyc.com/question/if-you-have-a-demo-whats-the-url-demo-can-be-anything-that-shows-us-how-the-product-works-usually-thats-a-video-or-screen-recording/)

Here's a screencast that I'll also put up on news.yc: http://www.getdropbox.com/screencast/ If you
do have a Windows box or two, here's the latest build:
http://www.getdropbox.com/u/2/DropboxInstaller.exe

#### [What is your company going to make? Please describe your product and what it does or will do.](https://getintoyc.com/question/what-is-your-company-going-to-make-please-describe-your-product-and-what-it-does-or-will-do/)

Dropbox synchronizes files across your/your team's computers. It's much better than uploading or
email, because it's automatic, integrated into Windows, and fits into the way you already work.
There's also a web interface, and the files are securely backed up to Amazon S3. Dropbox is kind of
like taking the best elements of subversion, trac and rsync and making them "just work" for the
average individual or team. Hackers have access to these tools, but normal people don't. It's
currently in private beta and I add batches of people every few days.

There are lots of interesting possible features. One is syncing Google Docs/Spreadsheets (or other
office web apps) to local .doc and .xls files for offline access, which would be strategically
important as few web apps deal with the offline problem.

### Founders

#### [Please tell us about an interesting project, preferably outside of class or work, that two or more of you created together. Include urls if possible.](https://getintoyc.com/question/please-tell-us-about-an-interesting-project-preferably-outside-of-class-or-work-that-two-or-more-of-you-created-together-include-urls-if-possible/)

Accolade Online SAT prep (launched in 2004) (http://www.accoladeprep.com/); a poker bot (here's an
old screenshot: https://www.accoladeprep.com/sshot2.gif ; it's using play money there but worked
with real money too.)

#### [Please tell us in one or two sentences about something impressive that each founder has built or achieved.](https://getintoyc.com/question/please-tell-us-in-one-or-two-sentences-about-something-impressive-that-each-founder-has-built-or-achieved/)

Drew - Programming since age 5; startups since age 14; 1600 on SAT; started profitable online SAT
prep company in college (accoladeprep.com). For fun last summer reverse engineered the software on a
number of poker sites and wrote a real-money playing poker bot (it was about break-even; see
screenshot url later in the app.)

#### [How long have the founders known one another and how did you meet? Have any of the founders not met in person?](https://getintoyc.com/question/please-tell-us-about-the-time-you-most-successfully-hacked-some-non-computer-system-to-your-advantage/)

There's a joke in here somewhere.

#### [If we fund you, which of the founders will commit to working exclusively (no school, no other jobs) on this project for the next year?](https://getintoyc.com/question/if-we-fund-you-which-of-the-founders-will-commit-to-working-exclusively-no-school-no-other-jobs-on-this-project-for-the-next-year/)

Drew

#### [Do any founders have other commitments between X and Y inclusive?](https://getintoyc.com/question/do-any-founders-have-other-commitments-between-x-and-y-inclusive/)

No; I'm leaving Bit9 in a few weeks to work on this full time regardless of YC funding.

#### [Do any founders have commitments in the future (e.g. finishing college, going to grad school), and if so what?](https://getintoyc.com/question/do-any-founders-have-commitments-in-the-future-eg-finishing-college-going-to-grad-school-and-if-so-what/)

No. Probably moving to SF in September

### Progress

#### [How far along are you?](https://getintoyc.com/question/how-far-along-are-you/)

Prototype - done in Feb. Beta - in people's hands now. Version I can charge for: 6-8 weeks?

#### [How long have each of you been working on this? How much of that has been full-time? Please explain.](https://getintoyc.com/question/how-long-have-each-of-you-been-working-on-this-how-much-of-that-has-been-full-time-please-explain/)

3 months part time. About ~5KLOC client and ~2KLOC server of python, C++, Cheetah templates,
installer scripts, etc.

### Idea

#### [What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?](https://getintoyc.com/question/whats-new-about-what-youre-making-what-substitutes-do-people-resort-to-because-it-doesnt-exist-yet-or-they-dont-know-about-it/)

Most small teams have a few basic needs: (1) team members need their important stuff in front of
them wherever they are, (2) everyone needs to be working on the latest version of a given document
(and ideally can track what's changed), (3) and team data needs to be protected from disaster. There
are sync tools (e.g. beinsync, Foldershare), there are backup tools (Carbonite, Mozy), and there are
web uploading/publishing tools (box.net, etc.), but there's no good integrated solution.

Dropbox solves all these needs, and doesn't need configuration or babysitting. Put another way, it
takes concepts that are proven winners from the dev community (version control, changelogs/trac,
rsync, etc.) and puts them in a package that my little sister can figure out (she uses Dropbox to
keep track of her high school term papers, and doesn't need to burn CDs or carry USB sticks
anymore.)

At a higher level, online storage and local disks are big and cheap. But the internet links in
between have been and will continue to be slow in comparison. In "the future", you won't have to
move your data around manually. The concept that I'm most excited about is that the core technology
in Dropbox -- continuous efficient sync with compression and binary diffs -- is what will get us
there.

#### [Who are your competitors, and who might become competitors? Who do you fear most?](https://getintoyc.com/question/who-are-your-competitors-and-who-might-become-competitors-who-do-you-fear-most/)

Carbonite and Mozy do a good job with hassle-free backup, and a move into sync would make sense.
Sharpcast (venture funded) announced a similar app called Hummingbird, but according to Jeff (who is
good friends with the tech lead) they're taking an extraordinarily difficult approach involving NT
kernel drivers. Google's coming out with GDrive at some point. Microsoft's Groove does sync and is
part of Office 2007, but is very heavyweight and doesn't include any of the web stuff or backup.
There are apps like Omnidrive and Titanize but the implementations are buggy or have bad UIs.

#### [What do you understand about your business that other companies in it just don't get?](https://getintoyc.com/question/what-do-you-understand-about-your-business-that-other-companies-in-it-just-dont-get/)

Competing products work at the wrong layer of abstraction and/or force the user to constantly think
and do things. The "online disk drive" abstraction sucks, because you can't work offline and the OS
support is extremely brittle. Anything that depends on manual emailing/uploading (i.e. anything web-
based) is a non-starter, because it's basically doing version control in your head. But virtually
all competing services involve one or the other.

With Dropbox, you hit "Save", as you normally would, and everything just works, even with large
files (and binary diffs ensure that only the changed portions go over the wire).

#### [How do or will you make money? How much could you make?](https://getintoyc.com/question/how-do-or-will-you-make-money-how-much-could-you-make/)

The current plan is a freemium approach, where we give away free 1GB accounts and charge for
additional storage (maybe ~$5/mo or less for 10GB for individuals and team plans that start at maybe
$20/mo.). It's hard to get consumers to pay for things, but fortunately small/medium businesses
already pay for solutions that are subsets of what Dropbox does and are harder to use. There will be
tiered pricing for business accounts (upper tiers will retain more older versions of documents, have
branded extranets for secure file sharing with clients/partners, etc., and an 'enterprise' plan that
features, well, a really high price.)

I've already been approached by potential partners/customers asking for a web services API to
programmatically create Dropboxes (e.g. to handle file sharing for Assembla.com, a web site for
managing global dev teams). There's a natural synergy between project mgmt/groupware web apps (which
do to-do lists, calendaring, etc. well but not files) and Dropbox for file sharing. I've also had
requests for an enterprise version that would sit on a company's network (as opposed to my S3 store)
for which I could probably charge a lot.

### Equity

#### [Have you incorporated, or formed any legal entity (like an LLC) yet?](https://getintoyc.com/question/have-you-incorporated-or-formed-any-legal-entity-like-an-llc-yet/)

No

### Legal

#### [Are any of the founders covered by noncompetes or intellectual property agreements that overlap with your project? If so, please explain.](https://getintoyc.com/question/are-any-of-the-founders-covered-by-noncompetes-or-intellectual-property-agreements-that-overlap-with-your-project-if-so-please-explain/)

Drew: Some work was done at the Bit9 office; I consulted an attorney and have a signed letter
indicating Bit9 has no stake/ownership of any kind in Dropbox

#### [Who writes code, or does other technical work on your product? Was any of it done by a non-founder? Please explain.](https://getintoyc.com/question/who-writes-code-or-does-other-technical-work-on-your-product-was-any-of-it-done-by-a-non-founder-please-explain/)

No

### Others

#### [If you had any other ideas you considered applying with, please list them. One may be something we've been waiting for. Often when we fund people it's to do something they list here and not in the main application.](https://getintoyc.com/question/if-you-had-any-other-ideas-you-considered-applying-with-please-list-them-one-may-be-something-weve-been-waiting-for-often-when-we-fund-people-its-to-do-something-they-list-here-and-not-in-the-main-application/)

One click screen sharing (already done pretty well by Glance); a wiki with version-controlled
drawing canvases that let you draw diagrams or mock up UIs (Thinkature is kind of related, but this
is more text with canvases interspersed than a shared whiteboard) to help teams get on the same page
and spec things out better (we use Visio and Powerpoint at Bit9, which suck for working
collaboratively); some ideas surrounding better web analytics for newbies

#### [Please tell us something surprising or amusing that one of you has discovered.](https://getintoyc.com/question/please-tell-us-something-surprising-or-amusing-that-one-of-you-has-discovered/)

The ridiculous things people name their documents to do versioning, like "proposal v2 good revised
NEW 11-15-06.doc", continue to crack me up.
