# Lago YC Application

- Type: Public YC application example
- Status: Public successful application published by the company
- URL: https://getlago.com/blog/how-we-got-into-yc
- Author: Anh-Tho Chuong / Lago
- Published: 2022-11-11
- Captured: 2026-06-16

## Summary

- Supporting YC company URL: https://www.ycombinator.com/companies/lago
- Company: Lago
- Batch: S21
- Application outcome: Successful
- Captured because the Lago blog states the submitted application got into YC on the first attempt.
- YC batch verified against the public YC company directory.
- Description: A no-code data tool for Growth teams.
- Outcome label: Successful
- The Lago blog post frames this as the application the founders sent to YC before they had a launched product or revenue. The post says they got into YC on their first attempt and emphasizes clear, concise communication, fast execution, and a founder-specific advantage or counterintuitive view.

## Content

### Company

#### Company name

Lago

#### Company URL

https://getlago.com/

#### Describe what your company does in 50 characters or less.

A no-code data tool for Growth teams.

#### What is your company going to make? Please describe your product and what it does or will do

Lago is a no-code tool that enables Growth teams to extract, transform and effortlessly take actions
on data, without engineers.

In order to be successful, Growth teams need to iterate fast and take actions on data. Yet, because
of tech bottlenecks it is impossible: since engineers are scarce and focused on building the product
and working on algorithms, prioritizing Growth needs over Product development is most of the time a
losing battle.

That's why we've productized what a tech team should ideally do for Growth teams: use an ETL (e.g.,
Fivetran) to centralize data from different tools to a data warehouse, model it with the help of
data scientists, and use a reverse ETL (e.g., Hightouch, Census) to push it to external tools (e.g.,
CRM, ads tools). Unlike typical datawarehouse setups, our infrastructure refreshes data every
minute, not only once a day. Therefore, Lago centralises constantly unified customer data and
synchronizes it 2-way with Growth tools, in real time.

On top of that, Lago's UX is no-code: we want to make sure every Growth team member can use Lago
without needing an engineer, nor any tech or SQL skills.

The big picture is to build the tool where all Go-to-Market teams (Growth, Sales, Marketing,
Customer Success) collaborate along their users' journey.

Today, these teams work in silos (Customer Success is logged on Zendesk, and does not talk to CRM
team which works on ActiveCampaign), which is, to say the least, sub-efficient. Lago will make
cross-teams and cross-tools workflows possible. This is an even larger pain and market.

#### Where do you live now, and where would the company be based after YC (List as City A, Country A/ City B, Country B)

Currently in Paris, France After product market fit (and... covid): move the Go to Market teams to
the US, Product located both in the US and in France (need to be close to customers), the heart of
Engineering in France (top-notch and affordable engineers) with a mostly remote Engineering team.

### Progress

#### How far along are you?

After a customer discovery phase in Q4 last year, we wrote our first line of code and designed our
first mockups on January 4th 2021.

At the end of January, before we even had a landing page, 70+ startups had already contacted us
(100% inbound) and asked if they could try our product asap.

Our beta is to be launched in a few weeks.

Meanwhile, we've been pitching every version of our Figma prototypes to Growth teams since January,
allowing us to keep our iteration loops super quick and maintain very tight relationships with our
pool of users.

#### How long have each of you been working on this? How much of that has been full-time? Please explain.

We have been working part-time since October 2020 (discovery/user interviews), and decided to start
in January 2021 full-time.

We've also worked with a freelance designer, and a freelance back-end developer to help us move
faster towards the beta launch, and agreed we would hire them full-time as soon as we have product
market fit.

#### Are people using your product? Yes/No

No

#### Do you have revenue? Yes/No

No

#### If you are applying with the same idea as last batch, did anything change? If you applied with a different idea, why did you pivot and what did you learn from the last idea?

N/A

#### If you have already participated or committed to participate in an incubator, "accelerator" or "pre-accelerator" program, please tell us about it.

N/A

### Idea

#### Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?

We experienced the problem firsthand in several startups.

The latest one is

Qonto

(backed by P. Thiel, raised 100M+): we reached the 1M MRR mark 18 months after launch and Qonto is
already a unicorn after only 5 years.

Customer data was scattered among many tools, and we could not take action on data. As a Growth
team, not taking actions on data means no user base, product usage or revenue growth, which hurts
the team's and above all the company's KPIs.

We tested a lot of different tools, none of them could do the job. We ultimately hired fully
dedicated engineers to build our own internal tools. Quite instantly, more than 50+ Growth teams
from other startups came to us and asked us if they could use our internal tools for their own
projects. We knew we were onto something!

After Qonto, I freelanced to help a dozen startups build their own internal tools and teams to solve
this pain.

Still, we re-validated the need by formally interviewing another 100+ Growth leaders in Q4 2020,
before finally deciding to build Lago full-time.

#### What's new about what you're making? What substitutes do people resort to because it doesn't exist yet (or they don't know about it)?

Lago is no-code, laser-focused on B2B Growth teams' needs.

They want to take actions on data, and iterate fast on account-based marketing and product usage
campaigns.

People resort to the following substitutes:

- Zapier: 'Zaps' can send one data point from A to B, that's all. It does not store data, so can't reconcile it, and thus creates lots of errors and duplicates. Zapier is like McDonald's: quick gratification, but you regret it as soon as you've eaten it. Every team we interviewed that uses it, wants to get rid of it, but can't because of tech bottlenecks.

- Customer Data Platforms: we've tried and used many of them at Qonto (including Segment Personas). The implementation and day-to-day use were tech-intensive. we had built and had to maintain so much custom code, that Anh-Tho (who was VP Growth) would not use the CDP anymore without an engineer next to her, for fear of breaking a custom script or misunderstanding data.

- Data warehouse stack: it's the exact opposite of what Growth teams want: they want to be freed from depending on engineers, iterate fast on tests, get fresh data in real time. They don't want to hear about ETLs, reverse ETLs, ask data scientists to transform and unify data, beg engineers to build pipes to the new tools they are testing. It's not what Tech teams want either: 'plumbing' data all-day-long instead of focusing on building a product.

#### What do you understand about your business that other companies in it just don't get?

1/ Making Growth teams dependent on Engineers is a lose-lose setup

Growth teams need to act and iterate fast on data. However, since data and actions necessarily exist
across systems (e.g., Facebook ads, CRM, emailing, product) engineers currently have to build the
required pipes to bridge the silos between these systems.

As engineers prefer to focus on products rather than 'data plumbing' (using an ETL, data modeling in
a warehouse, and a reverse ETL), and Growth teams themselves don't want to depend on engineers, a
no-code data overlay such as Lago adds tremendous value.

It gives speed, control and autonomy to Growth teams, and frees the engineers to focus solely on
where they have the most impact.

2/ In order to take relevant actions on data, it needs to be refreshed in real-time. Yet data
warehouses stacks were not built for that.

Data warehouses have been implemented for reporting purposes (one refresh/day). While ETLs (e.g.,
Fivetran) and reverse ETLs (e.g., Census, Hightouch) can help to move data around, it's not useful
to Growth teams if they process already outdated data.

#### How do or will you make money? How much could you make? (We realize you can't know precisely, but give your best estimate.)

We'll charge on a usage-based model:

- Volume of data (e.g., number of users or accounts)

- Number of integrations (e.g., Salesforce, Hubspot, Intercom)

- Number of seats : after launch, when Lago to is the tool where Go-to-Market teams collaborate and create workflows -> land and expand strategy Our potential users currently spend around $1 200 - $15 000 / month for imperfect solutions.

- Low-end budget: $1200/month: Zapier subscriptions (Zapier for teams: $600/month), and a few hours of work from a BI analyst

- High-end budget: $15 000/month for a data warehouse-centric infrastructure: Fivetran ETL + Pop SQL + Reverse ETL (Census/Hightouch) + Data engineers & scientists (full-time) + Growth engineers (part time) We'll start by targeting the B2B SMBs as they are using more tools, have a higher need for centralization/unification and are more prone to be early adopters, but we're looking at the whole SMB market. Assuming:

- A $1 000/month average ARPU -> $12 000 average ARR

- Around 100K SMBs are using Hubspot CRM [1], which amounts to 29% of market share [2], so the total addressable market is 344K SMBs.

- We're looking at a current $4+ bn total addressable market

- In 5 years: a $18+ bn total addressable market. Indeed, the low-code development platform market is projected to grow at a 30% CAGR rate (for the 10 coming years) [3]. Sources: 1. https://www.hubspot.com/industry-data?category=total&topic=deal-pipelines&subTopic=deals-created&drilldown=null 2. https://www.datanyze.com/market-share/marketing-automation--3/hubspot-market-share 3. https://www.psmarketresearch.com/market-analysis/low-code-development-platform-market

#### How will you get users? If your idea is the type that faces a chicken-and-egg problem in the sense that it won't be attractive to users till it has a lot of users (e.g. a marketplace, a dating site, an ad network), how will you overcome that?

Our first users are companies we interviewed during our discovery phase, or who organically came to
us for advice about their Growth and data stack.

Lago's acquisition strategy will rely on bottoms-up, as it is a no-code, intuitive data tool any
Growth Marketer can use on her own. No engineers, or long onboarding process needed.

To build demand, we identified several levers:

- Educating growth teams about data: e.g., we've bootstrapped a course by email (600+ qualified leads) and will amplify our efforts when we launch.

- Community: we had built Qonto Startup Meetups community (4K+ French startups) at Qonto, and can adapt/replicate what we had done.

- Targeted SEO/paid campaigns on companies hiring their first growth/sales engineers or data engineers As we grow: even the best self-serve product-led approach can benefit from a human touch, so we will layer sales and customer-facing teams into our product-led growth model. These teams will focus more on implementation and usage expansion, than on outbound sales.

#### Is there anything else we should know about your company?

We've built Lago to be international from day 1, we keep all documentation in English, write our
content in English, make a point to document in writing: we're all in France today, but tomorrow,
our market and part of our team will be in the US, and working remotely.

### Others

#### If you had any other ideas you considered applying with, please list them. One may be something we've been waiting for. Often when we fund people it's to do something they list here and not in the main application.

A tool for Community Managers, as building communities will be a marketing discipline just as
performance marketing is: not sure if it would be a CRM, a data platform, but the space is huge!

#### Please tell us something surprising or amusing that one of you has discovered.(The answer need not be related to your project.)

Last year, when Raffi was preparing for their trip to the North Pole, he had to eat 6 000 calories a
day, i.e. 6 complete meals/a day, while exercising a lot, to be able to resist the very low
temperatures there. Eating that much was surprisingly the hardest part of the trip preparation.

He thought it would be a meal feast: eating their favorite food all the time, indulging in junk
food.

Actually, after only 3 days, he was totally disgusted by food.

They had to fight their reluctance to eat, and implemented a very strict system to overcome this:
structured meal plan, meal alarms 6 times a day, calories count etc: the initial feast became a
discipline challenge.

### Curious

#### What convinced you to apply to Y Combinator? Did someone encourage you to apply?

Several people encouraged us to apply: Lyle Fong (former visiting partner at YC), Arthur
Bonnecarrere (co-founder of Once.app, YC S20), Enzo Avigo (CEO of June, YC W21), Christophe Pasquier
(CEO of Slite, YC W18), David Rusenko (CEO of Weebly YC07), Hassan Bourgi (CEO of Djamo, YC W21)

#### How did you hear about YC?

Anh-Tho launched Weebly (YC07) in France, and hearing David Rusenko (CEO of Weebly) praise YC made
her want to join it ever since.
