# Claude Starter Kit

A ready-made Claude Code setup for Windows: 11 agents, 14 skills, a Hebrew language hook, starter memory, and an Obsidian vault built on the Lazy Obsidian Method (Karpathy LLM-wiki + PARA).

## Install — paste this into Claude Code

```
Install my Claude starter kit. Clone https://github.com/RoyKriesler/claude-starter-kit and follow INSTALL.md in it exactly, end to end, without asking me to do steps you can do yourself.
```

That's it. Claude installs the prerequisites, agents, skills, settings, memory and the Obsidian vault, verifies everything, and reports back.

## What's inside

| Path | What |
|---|---|
| `kit/agents/` | coder, code-reviewer, verifier, plan-auditor, web-researcher, web-scraper, builder, analytics-engineer, campaign-planner, marketing-analyst, econometrics-reviewer |
| `kit/skills/` | debugger, planner, research-brief, report-style, hebrew-office, python-data, vba-engineering, google-workspace, google-best-practice, ad-creative, llm-wiki-setup, wiki-self-heal, obsidian-cli, defuddle |
| `kit/memory/` | 15 starter memories: working rules learned the hard way (test before done, Hebrew documents, PDF sizing, SQL delivery…) |
| `kit/CLAUDE.md` | global instructions template with an auto-invoke routing table |
| `kit/hooks/` | Hebrew bidi self-check on every Hebrew prompt |
| `kit/scripts/` | `render_check.py` and `validate_dataset.py`, the gates the builder and scraper agents run |
| `vault/` | Obsidian vault skeleton: schema `CLAUDE.md`, index, log, hubs, job templates |
| `INSTALL.md` | the step-by-step the installing Claude follows |
