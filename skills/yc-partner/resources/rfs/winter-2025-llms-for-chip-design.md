# LLMs for Chip Design

- Type: YC Requests for Startups section
- Status: Official YC source
- URL: https://www.ycombinator.com/rfs#llms-for-chip-design
- Author: Garry Tan (https://www.ycombinator.com/people/garry-tan)
- Published: Unknown
- Captured: 2026-06-16
- Caveat: references/caveats/yc-rfs-source.md

## Summary

- Full captured content preserved below

## Content

Each breakthrough in AI creates demand for more powerful chips to train larger models. No country wants to fall behind in this arms race. Domestic chip design and manufacture is not just about economics anymore, it's about survival in a post AI world. OpenAI O1 showed us that LLMs with reasoning can power breakthroughs in science and engineering and we're interested in talking to anyone using LLMs to improve chip design.

We are especially interested in anyone focusing on designing ASICs and FPGAs. Design of customized digital systems whether through FPGAs (field programmable gate arrays) or ASICs (application-specific integrated circuits) has typically been costly because of the amount of custom design, development and testing necessary to bring such a system online. With the advent of large language models, these costs are coming down significantly, such that ever more specialized types of computation could be done.

Our normal computing environment assumes Von Neumann architecture using CPUs that we are familiar with: single shared memory for programs and data, arithmetic unit and a program control unit, operating through fetching and execution cycles serially. Most computers and computation use this because it's very easy to reprogram such systems.

We know there is a clear engineering trade-off: it is possible to optimize especially specialized algorithms or calculations such as cryptocurrency mining, data compression, or special-purpose encryption tasks such that the same computation would happen faster (5x to 100x), and using less energy (10x to 100x). This is a diagram (credit: Taner Sadikoglu) showing the differences in how data flows an optimized FPGA system versus a normal CPU.

Given the order of magnitude improvements possible with specialized FPGAs and ASICs, use of LLMs to optimize this process is likely to produce extremely useful results and great opportunities for startups.
