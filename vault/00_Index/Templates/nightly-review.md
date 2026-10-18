---
job: nightly-review
cadence: daily 23:00
inputs: [04_Notes_Daily/today, 00_Index/Logs/agent/, MEMORY.md, hubs]
outputs: [refreshed hubs, memory updates, 00_Index/log.md entry, git commit]
---

# Nightly Review — Job Spec

**Purpose**: tidy + priority refresh + backup. Roll up the day into the chronological log.

## Steps for the agent

1. **Read state**: `CLAUDE.md`, `00_Index/index.md`, today's `00_Index/Logs/ingest/YYYY-MM-DD_*.md` if it exists.

2. **Process today's daily note** `04_Notes_Daily/YYYY-MM-DD.md`:
   - Decisions worth remembering across conversations → write to
     ```
     05_Resources/Claude Code/memory/   (one fact per file, then a pointer line in MEMORY.md)
     ```
     Otherwise → write to relevant project README.
   - Open questions → seed tomorrow's daily note skeleton (create `04_Notes_Daily/YYYY-MM-DD+1.md` with a "carried over" section).

3. **Refresh Hubs that drifted**:
   - `[[Projects]]`: scan `03_Projects/*/README.md` frontmatter. Anything `status: done`? Propose archive (don't auto-move). Anything new in `03_Projects/` not yet in the Hub? Add link.
   - `[[Areas]]`: pull latest non-stale notes per area into the Hub.
   - `[[Workflows]]`: update "Last run log" pointers.

4. **Index sync**: any new pages created today not yet in `00_Index/index.md`? Add them under the right category.

5. **Roll up agent session logs** from today (`00_Index/Logs/agent/YYYY-MM-DD_*.md`): one summary line per session in the nightly log.

6. **Write detailed log** to `00_Index/Logs/reviews/nightly/YYYY-MM-DD_nightly.md`:
   - Hubs refreshed
   - Promotions / archive proposals
   - Memory updates (which file, one-line summary)
   - Open questions surfaced for tomorrow
   - Index sync summary
   - Git commit hash (after step 7)

7. **Backup**:
   ```
   git add .
   git commit -m "nightly review YYYY-MM-DD"
   git push   # only if remote configured
   ```
   If working tree has unstaged user changes from before this job started, commit them separately first with message `wip: pre-nightly snapshot YYYY-MM-DD`.

8. **Append summary entry** to `00_Index/log.md`:
   ```
   ## [YYYY-MM-DD] nightly | <commit-hash-short>

   <one paragraph: what got refreshed, what was archived/proposed, memory updates, open questions for tomorrow>
   ```

## Rules

- Never push to git without a descriptive commit message.
- Never modify a project README without preserving its frontmatter.
- If memory write conflicts with existing memory → prefer existing, log the conflict.
- Don't auto-archive — propose only.

## Invocation

Cron: `daily 23:00` (Windows Task Scheduler `ObsidianLazy_NightlyReview` → `00_Index/Scripts/run-job.ps1 -Job nightly-review`).
