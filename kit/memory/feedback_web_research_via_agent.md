---
name: feedback-web-research-via-agent
description: Online reading (URLs, repos, docs, "look up X") goes to the web-researcher agent by default; datasets go to web-scraper
metadata:
  type: feedback
---
Route every online research task to the `web-researcher` agent without being asked; a table or file of records goes to `web-scraper`. A single quick cited answer can use the `research-brief` skill in-session.

**Why:** raw pages stay out of the main context, and routing lessons accumulate in one agent file.

**How to apply:** pasted URL, "what does this repo do", "summarize", "compare X and Y", "find articles" → spawn the agent; several sources → several agents in parallel. Exception: the user says "do it directly".
