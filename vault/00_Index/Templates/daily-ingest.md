---
job: daily-ingest
cadence: daily 09:00
inputs: [00_Raw/, 04_Notes_Daily/]
outputs: [00_Index/Logs/ingest/, 00_Index/log.md entry, promoted notes, index update]
---

# Daily Ingest — Job Spec

**Purpose**: get messy inputs in, don't overthink. Triage + light promotion. Karpathy-style ingest, PARA-aware promotion.

## Steps for the agent

1. **Read state**: `CLAUDE.md`, `00_Index/index.md`, last 5 lines of `00_Index/log.md`.

2. **Scan raw**: list items in `00_Raw/inbox/`, `00_Raw/clips/`, `00_Raw/voice/`, `00_Raw/ideas/`. Count by folder.

3. **Triage each item** — three signals:
   - **Trash** (duplicate, irrelevant, no value): delete. Note count + reason in log.
   - **Quick promote** (clear destination): apply the promotion procedure below.
   - **Defer**: leave in raw. If older than 30 days unpromoted → flag for next weekly run (don't auto-archive).

4. **Promotion procedure** for each promote-candidate:
   - Identify destination by PARA: Project (deadline) → `03_Projects/` ; Area (ongoing) → `01_Areas/` or `02_Work/` ; Resource (reusable) → `05_Resources/`.
   - Move file to destination with a clean filename (Title Case if a note, kebab-case if a template/ops file).
   - Add frontmatter:
     ```yaml
     ---
     title: <page title>
     status: active
     tags: [tag1, tag2]
     sources: [00_Raw/inbox/<original-filename>]
     related: [[parent-hub-or-page]]
     created: YYYY-MM-DD
     last_updated: YYYY-MM-DD
     owner: me
     ---
     ```
   - Add a wikilink from the closest Hub or related note. **Never promote without an inbound link** — orphans defeat the purpose.
   - Update `00_Index/index.md` with the new page under the right category.

5. **Process today's daily note** `04_Notes_Daily/YYYY-MM-DD.md` if it exists:
   - Action items → matching project README in `03_Projects/<name>/`
   - References → `05_Resources/refs/` or `05_Resources/reading/`
   - Cross-cutting lessons → `00_Index/Hubs/OS.md`

6. **Write detailed log** to `00_Index/Logs/ingest/YYYY-MM-DD_daily-ingest.md` with:
   - Item counts by folder (before / after)
   - Promotions: `raw path → destination` for each
   - Trashed: count + reason
   - Deferred items >30 days (flagged)
   - Index update summary

7. **Append summary entry** to `00_Index/log.md`:
   ```
   ## [YYYY-MM-DD] daily | <N> ingested, <M> promoted, <K> deferred

   <one paragraph: what came in, where it landed, anything notable>
   ```

## Rules

- Don't over-process. If unclear → leave in raw.
- Never delete a daily note. They are the journal.
- Never promote without adding a wikilink from a hub or related note.
- Frontmatter on promotion is mandatory — non-negotiable.
- Never modify files in `00_Raw/` after promotion. Move, don't edit.

## Invocation

Cron: `daily 09:00` (Windows Task Scheduler `ObsidianLazy_DailyIngest` → `00_Index/Scripts/run-job.ps1 -Job daily-ingest`).
