---
job: weekly-vault
cadence: Sunday 20:00
inputs: [memory, all hubs, full vault for health check]
outputs: [weekly review note, audit report in 00_Index/audits/, gaps list, next-week focus, graphify + qmd refresh, 00_Index/log.md entry]
---

# Weekly Vault — Job Spec

**Purpose**: set focus areas for the coming week. Find gaps. Health check the vault. Run the self-heal loop in audit-only mode (default).

`graphify` and `qmd` steps are optional: skip them silently when the tool is not installed.

## Steps for the agent

1. **Read state**: `CLAUDE.md`, `00_Index/index.md`, last 10 entries of `00_Index/log.md`.

2. **Self-heal audit** — invoke the `wiki-self-heal` skill in **audit-only mode** (default for first runs to avoid dumping pages without review):

   > Run `wiki-self-heal` in audit-only mode on this vault. Use the `wiki/` junction (which resolves to `00_Index/`) and `raw/` junction (which resolves to `00_Raw/`). Write the audit report to `00_Index/audits/audit-YYYY-MM-DD.md`. Add an entry to `00_Index/index.md` under the Audits section.

   Audit-only means: scan and report, do not research or write new pages this run. the owner reads the audit and decides which gaps to fill in next session.

3. **PARA health check** (in addition to the wiki-self-heal audit):
   - Stale raw: items in `00_Raw/` older than 30 days → propose archive list (don't auto-archive)
   - Projects without frontmatter → list
   - Hubs vs reality: any project in `03_Projects/` not in `[[Projects]]` Hub? Vice versa?
   - Areas with no activity in 14+ days → flag

4. **Gaps proposal**:
   - Topics referenced 3+ times across the vault but no resource note → propose `05_Resources/` candidates
   - Concepts mentioned but lacking depth → research candidates (input for next manual self-heal full mode)

5. **Focus for the coming week**:
   - Active projects with deadline within 14 days
   - Areas with neglected threads
   - Top 3 things the owner should work on, with reasoning tied to deadlines or area standards. **No vibes.**

6. **Refresh tooling outputs**:
   - **graphify**: `graphify update "$HOME/ObsidianVault"` → updates `graphify-out/graph.json` + `graph.html` (no LLM needed for code-only changes; for doc changes the runner will note this)
   - **qmd**: `qmd update` → re-indexes the `vault` collection. Optional: `qmd embed` to refresh vector embeddings (heavy — only if the owner budget-approved)

7. **Write detailed weekly log** to `00_Index/Logs/reviews/weekly/YYYY-MM-DD_weekly.md`:
   - Self-heal audit summary (severity counts by gap type)
   - PARA health check results
   - Gaps proposed (top 10)
   - Top-3 focus items with reasoning
   - Tooling refresh status (graphify run? qmd reindex?)
   - Pointer to `00_Index/audits/audit-YYYY-MM-DD.md` for the full report

8. **Append summary entry** to `00_Index/log.md`:
   ```
   ## [YYYY-MM-DD] weekly | audit found <N> gaps; top focus: <one-liner>

   <one paragraph: highlights from health check, top 3 focus items for the week, anything urgent>
   ```

## Rules

- Default to audit-only mode for `wiki-self-heal`. Switch to full mode only if the owner explicitly says so in the runner prompt.
- Don't auto-archive. Propose, let the owner approve in next session.
- Don't auto-write resource notes. Propose topics + sources.
- Top-3 focus must be tied to deadlines or explicit area standards.
- `qmd embed` only if explicitly authorized — it costs LLM tokens.

## Invocation

Cron: `Sunday 20:00` (Windows Task Scheduler `ObsidianLazy_WeeklyVault` → `00_Index/Scripts/run-job.ps1 -Job weekly-vault`).
