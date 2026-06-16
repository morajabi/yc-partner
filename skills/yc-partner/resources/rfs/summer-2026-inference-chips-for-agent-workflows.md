# Inference Chips for Agent Workflows

- Type: YC Requests for Startups section
- Status: Official YC source
- URL: https://www.ycombinator.com/rfs#inference-chips-for-agent-workflows
- Author: Diana Hu (https://www.ycombinator.com/people/diana-hu)
- Published: Unknown
- Captured: 2026-06-16
- Caveat: references/caveats/yc-rfs-source.md

## Summary

- Full captured content preserved below

## Content

Most AI chips are designed for a world where inference means "prompt in, response out." Agents don't work that way. They loop: calling tools, branching, backtracking, holding context across dozens of steps. That's a completely different hardware problem.

Current GPUs hit 30 to 40 percent of peak utilization on these workloads because the work is bursty, bouncing between memory-bound model calls, I/O-bound tool use, and CPU-bound orchestration. That gap is where purpose-built silicon wins.

NVIDIA bought Groq for $20 billion because it saw this coming. Google built TPU v7 for inference specifically. But nobody's designing for the agent loop itself: fast context switching between models, native speculative decoding, memory built for KV caches that persist across an entire execution graph.

Groq's real insight wasn't the chip. It was the compiler that made the chip work. We think that'll be true for whoever builds this next. If you understand both chip architecture and how agents actually execute, this is a rare moment where both halves of that experience matter.

If you're building inference silicon for agentic AI, we'd love to hear from you.
