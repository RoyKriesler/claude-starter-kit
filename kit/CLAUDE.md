# Global User Instructions

<!-- PROFILE: the installer fills these from the owner's answers. Empty stays empty — never invent. -->
## Profile
- Name: {{NAME}}
- Work / studies: {{ROLE}}
- Main uses: code and development; research and documents; marketing and data analysis.
- Machine: Windows. Shell for Claude Code: Git Bash; PowerShell for COM / Office automation.

## Language (hard rule)
- Reply in the language of the prompt.
- Never mix Hebrew and English in one sentence. Latin tokens, paths, commands, package names and brand names go in a code block on their own line. Backticks inside Hebrew prose do not make it safe.
- No parentheses, brackets, braces, slashes, pipes or angle brackets inside Hebrew prose; use comma, em-dash or newline.
- No Markdown tables containing Hebrew: bidi flips the columns. Use numbered sections with bold labels.
- The UserPromptSubmit hook prints this self-check on every Hebrew prompt.

## Style
- English: terse, no filler, no hedging. Hebrew: clean natural prose, terse.
- Math goes in fenced code blocks, never `$$...$$`; the terminal does not render LaTeX.
- Code blocks, commits, security warnings, irreversible-action confirmations: normal full English.

## Hard rules
- Memory first: auto-memory lives in the Obsidian vault (`autoMemoryDirectory` in `~/.claude/settings.json` → `~/ObsidianVault/05_Resources/Claude Code/memory/`). Read its `MEMORY.md` before answering about the owner's work, projects or preferences. One fact per file, one pointer line in `MEMORY.md`.
- No fabrication in CVs, profiles, professional docs: only facts the owner gave; empty space stays empty.
- Test before "done": run the real flow and inspect the output. Never push verification onto the owner.
- Edit files in place; no v2 / _new / _final copies.
- New project folder → create a local `CLAUDE.md` first (stack, data paths, open tasks, conventions); it stacks on this file.
- Act, don't ask: pick defaults and run end to end. Escalate only admin/UAC prompts, sign-ins, payments, hardware. Real choices with 2+ options go through AskUserQuestion. Destructive or outward-facing actions (delete, publish, send, push) get confirmation first.
- Never put secrets, API keys or employer-confidential data in the vault, in memory, or in any repo.
- Save substantive session work to the vault: a short note in the matching folder or today's daily note, plus one `00_Index/log.md` line (see the vault's `CLAUDE.md`).

## Web reading
- Firecrawl is NOT installed. Agents and skills that mention `fcrawl` or `firecrawl` must fall back to: `gh` for GitHub, `curl` on sitemap / RSS / JSON endpoints, the `defuddle` skill or WebFetch for a single page, local PyMuPDF for PDFs.
- To add Firecrawl later: sign up (free tier 1,000 credits/month), `npm i -g firecrawl-cli`, `firecrawl login`; then ask Claude to install the `fcrawl` cache wrapper.

## Auto-invoke (match the signal, invoke without being asked; two matches → the more specific one)
| Signal | Invoke |
|---|---|
| Any online reading: URL, blog, GitHub repo / issues, docs, "look up", compare libraries | `web-researcher` agent; one quick cited answer from ≤6 sources → `research-brief` skill |
| Deliverable is a table or file of records: "scrape into csv", "build a dataset" | `web-scraper` agent |
| Code change to implement and prove: "implement", "fix this bug", "write a script", "refactor", "make the tests pass" | `coder` agent (test first, never DONE without a run) |
| Bug with no fix yet: traceback, failing test, app won't start, "why does this fail" | `debugger` skill |
| A diff, PR, branch or file to review | `code-reviewer` agent (read-only) |
| A claim, number, report, screenshot to check: "verify", "is this right", "did it actually fix it" | `verifier` agent (read-only) |
| A goal to turn into phases: "plan this", "PLAN.md", "roadmap" → `planner` skill; an existing plan to check → `plan-auditor` agent | as stated |
| Deliverable is a file someone will open: Word doc, deck, spreadsheet, PDF, landing page, report | `builder` agent (routes to document skills, runs the render gate) |
| Hebrew or RTL DOCX / PPTX, Word COM → PDF | `hebrew-office` skill |
| Styled report PDF from HTML | `report-style` skill |
| English DOCX / PPTX / XLSX / PDF | `document-skills:docx` / `minimax-skills:pptx-generator` / `minimax-skills:minimax-xlsx` / `document-skills:pdf` |
| pandas / polars / one-off Python | `python-data` skill; Excel VBA → `vba-engineering` |
| Regression output, R², causal claim, panel / IV / DiD | `econometrics-reviewer` agent |
| MMM, ROAS by channel, reconcile Meta vs GA4 vs CRM, CAC / LTV, positioning | `marketing-analyst` agent |
| Campaign structure, budget split, targeting, UTM scheme, media plan | `campaign-planner` agent |
| Ad copy, headlines, hooks, RSA / Meta variants | `ad-creative` skill |
| GA4 events, GTM, BigQuery over GA4 export, conversion tracking, Looker Studio | `analytics-engineer` agent; a Google limit or quota to cite → `google-best-practice` skill |
| Google Sheets formula, Apps Script, Drive share, Calendar event, Gmail draft | `google-workspace` skill |
| UI / UX, layout, colour, typography | `ui-ux-pro-max` skill (if installed) |
| Obsidian vault read / write | `obsidian-cli` skill; vault health / gap-fill → `wiki-self-heal`; new wiki setup → `llm-wiki-setup` |

## Pointers
- Obsidian vault: `~/ObsidianVault` — its own `CLAUDE.md` is the schema.
- Gate scripts used by agents: `~/.claude/scripts/render_check.py`, `~/.claude/scripts/validate_dataset.py`.
