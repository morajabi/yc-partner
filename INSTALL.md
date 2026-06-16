# Installation

This page has the manual install paths for YC Partner. If you are already using Codex or Claude Code, the simplest option is still to paste this prompt into the agent:

```text
Install YC Partner globally as an agent skill from https://github.com/morajabi/yc-partner.git.

Clone or update the repo in a stable local folder, install `skills/yc-partner` into the global skills directory for the agent I am using, and tell me how to invoke it when finished.
```

## Clone

```sh
git clone https://github.com/morajabi/yc-partner.git
cd yc-partner
```

If you already cloned it, pull the latest version:

```sh
git pull
```

## Codex

Install it as a personal Codex skill:

```sh
mkdir -p ~/.agents/skills
ln -s "$PWD/skills/yc-partner" ~/.agents/skills/yc-partner
```

Restart Codex if it was already open. Then ask:

```text
Use YC Partner to review my YC application
```

You can also explicitly mention the skill with `$yc-partner`.

## Claude Code

Install it as a personal Claude Code skill:

```sh
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/yc-partner" ~/.claude/skills/yc-partner
```

Restart Claude Code if it was already open. Then invoke it directly:

```text
/yc-partner review my YC application
```

or ask Claude to use YC Partner in plain English.

## Claude.ai

Create a skill zip with `SKILL.md` at the top level:

```sh
cd skills/yc-partner
zip -r ../../yc-partner-skill.zip .
cd ../..
```

Then upload `yc-partner-skill.zip` as a custom Skill from Claude settings. Use this only if your Claude plan has custom Skills enabled.

## Updating

From the cloned repo:

```sh
git pull
```

If you installed with a symlink, that is enough. If you copied the skill folder instead, copy the updated `skills/yc-partner` folder into your global skills directory again.
