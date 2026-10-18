# Vault — Obsidian Knowledge Stack

Local-first markdown second brain. Built on the **Lazy Obsidian Method**: Karpathy LLM-wiki + PARA + recurring agent jobs.

You are the LLM. The human curates sources and asks questions. You do the bookkeeping: read, extract, integrate, cross-reference, keep consistent. Never complain about the grunt work — it is the whole point.

## The map (read this first, every time)

This file is the floor plan. Read it before doing anything in the vault.

## Layout (PARA over numbered scheme)

| Folder | Layer | Notes |
|--------|-------|-------|
| `00_Raw/` | Raw source-of-truth, **read-only** | `inbox/`, `clips/`, `voice/`, `ideas/`. Triage daily. |
| `00_Index/` | MOC + ops | `Hubs/`, `Templates/`, `Logs/`, `audits/`, `Scripts/`, master `index.md` and `log.md`. |
| `01_Areas/` | Areas | Ongoing responsibilities with no end date (studies, health, finances). One subfolder per area. |
| `02_Work/` | Areas | Day job. Keep employer-confidential data OUT of the vault. |
| `03_Projects/` | Projects | Defined outcome + deadline. One subfolder or note per project. |
| `04_Notes_Daily/` | Daily | Per-day journal, `YYYY-MM-DD.md`. |
| `05_Resources/` | Resources | Reusable reference: `reading/`, `refs/`, `snippets/`, and `Claude Code/memory/` (Claude's auto-memory). |
| `99_Archive/` | Archive | Done / cold. |

## Routing table

For each task, read these files first. Skip the rest.

| Task | Read first | Then |
|------|-----------|------|
| Ingest a new source | `CLAUDE.md`, `00_Index/index.md` | the source in `00_Raw/`, plus `00_Index/Templates/daily-ingest.md` |
| Answer a query | `CLAUDE.md`, `00_Index/index.md`, relevant Hub in `00_Index/Hubs/` | specific notes by wikilink |
| Lint / self-heal | `CLAUDE.md`, `00_Index/index.md`, last 10 of `00_Index/log.md` | `00_Index/Templates/weekly-vault.md` + `wiki-self-heal` skill |
| Add a cross-reference | `00_Index/index.md` | the two pages being linked |
| Check the timeline | last entries of `00_Index/log.md` | — |
| Promote raw → project/area | `00_Raw/<item>`, target Hub | matching `01_`–`05_` folder |

## The three layers

1. **`00_Raw/`** — immutable source documents. Read, **never modify**. If you would change anything there, stop and ask.
2. **`00_Index/`, `01_`–`05_`, `04_Notes_Daily/`** — LLM-owned markdown. Create, update, maintain.
3. **`CLAUDE.md` + `AGENTS.md`** — the schema. Update only when the owner asks.

## Naming conventions

- Notes: `Title Case.md`; templates and ops files: `kebab-case.md`. Title matches filename.
- Raw sources: `YYYY-MM-DD-source-title.<ext>`.
- Audits: `00_Index/audits/audit-YYYY-MM-DD.md`.

## Page format

Every Project + Area note starts with:

```yaml
---
title: <page title>
status: <active|paused|done>
tags: [tag1, tag2]
sources:
  - 00_Raw/source-file.md
  - https://external-url (accessed YYYY-MM-DD)
related: [[other-page]]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
owner: me
---
```

- `[[wikilinks]]` for internal links, never markdown links.
- One concept per page.
- `sources:` must not be empty for ingested content. No source, no page.

## `00_Index/index.md` and `00_Index/log.md`

- `index.md` is the master catalog, one line per page: `- [[page]] — summary`. Read it first on any query; update it on every new page. A page missing from the index is invisible.
- `log.md` is append-only: `## [YYYY-MM-DD] <op> | <title>`. Ops: `ingest`, `query`, `lint`, `update`, `init`, `daily`, `nightly`, `weekly`, `heal`, `promote`, `archive`.

## Workflow: Ingest

1. Read the source completely.
2. Pick the destination by PARA (deadline → Project, ongoing → Area, reusable → Resource).
3. Write or update the page with frontmatter and `sources:`.
4. Link it from the closest Hub. Never promote an orphan.
5. Update `index.md`, append to `log.md`.

## Workflow: Lint (weekly, `wiki-self-heal` skill, audit-only by default)

Scan for contradictions, stale claims, orphan pages, missing pages (concept referenced 2+ times with no page), missing cross-refs. Output severity-ranked with a fix proposal each.

## Session save

At the end of any substantive Claude session (a project step, a solved problem, a decision), write a short note in the matching folder or in today's `04_Notes_Daily/YYYY-MM-DD.md`, and append one `log.md` line. Trigger phrases from the owner: "save to obsidian", "תשמור באובסידיאן".

## Recurring jobs (optional, Windows Task Scheduler → claude CLI)

| Job | Cadence | Spec |
|-----|---------|------|
| Daily ingest | 09:00 | `00_Index/Templates/daily-ingest.md` |
| Nightly review | 23:00 | `00_Index/Templates/nightly-review.md` |
| Weekly vault | Sunday 20:00 | `00_Index/Templates/weekly-vault.md` |

Runner: `00_Index/Scripts/run-job.ps1 -Job <name>`. Each run uses the owner's Claude usage (`--max-budget-usd 2` cap). Keep every `.ps1` ASCII or UTF-8 with BOM: PowerShell 5.1 misreads a BOM-less UTF-8 file with an em-dash and fails before logging.

## Guardrails

**CAN**: create and update pages in `00_Index/`, `01_`–`05_`, `04_Notes_Daily/`; update `index.md`; append `log.md`; write audits; promote from `00_Raw/` with a Hub link.

**CANNOT**:
- Modify or delete anything in `00_Raw/`.
- Delete pages without explicit owner confirmation — flag orphans, do not remove.
- Add factual claims without `sources:`; fabricate citations; silently resolve contradictions (note both sides).
- Auto-archive without proposing first.
- Write Latin characters inside Hebrew sentences.
- Fabricate facts in personal or CV-style notes.

**Simplicity criterion**: all else equal, fewer new pages wins. Update an existing page before creating a new one.
