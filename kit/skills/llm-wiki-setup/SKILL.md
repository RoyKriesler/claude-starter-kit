---
name: llm-wiki-setup
description: Initialize a Karpathy-style LLM wiki (personal knowledge base / AI second brain) in a folder. Creates a CLAUDE.md schema with routing table and naming conventions, AGENTS.md mirror, raw/wiki directory structure, and index.md/log.md scaffolding — a complete working vault in one pass. Use when the user asks to "set up an LLM wiki", "create a second brain", "build a personal knowledge base", "install the Karpathy wiki pattern", "initialize a knowledge vault", or points at an empty folder and wants to turn it into an AI-maintained wiki.
---

# llm-wiki-setup

Install the Karpathy LLM wiki pattern into a folder. One pass, three questions, a working vault a beginner can use immediately.

## What gets created

```
<vault>/
├── CLAUDE.md              # the map — routing table, schema, workflows, guardrails
├── AGENTS.md              # minimal mirror for Codex and other non-Claude agents
├── .gitignore
├── raw/                   # immutable source documents (LLM reads, never writes)
│   └── .gitkeep
└── wiki/                  # LLM-owned markdown
    ├── index.md           # catalog of every page, organized by category
    └── log.md             # chronological operation log with grep-friendly prefix
```

Optional additions the user may request at setup time:

- `wiki/hot.md` — 500-char rolling buffer for fast recent-context lookup (executive-assistant use cases)
- Nested wiki subfolders: `wiki/entities/`, `wiki/concepts/`, `wiki/sources/`, `wiki/analyses/`

## Setup flow

Ask these three questions in a single message:

1. **Vault path?** Absolute path. Will be created if it doesn't exist.
2. **Flat or nested wiki?** Flat is the default (Karpathy's preference — cleaner, grep-friendly). Nested adds subfolders for larger or mixed-topic vaults.
3. **Include hot cache?** Optional `wiki/hot.md` rolling buffer. Default: no.

## Build procedure

1. **Safety check.** If `<vault>/CLAUDE.md` or `<vault>/wiki/` already exists, stop and ask the user — do not overwrite without explicit confirmation.
2. **Create directories.** `<vault>`, `<vault>/raw/`, `<vault>/wiki/`. For nested layout, also create `wiki/entities/`, `wiki/concepts/`, `wiki/sources/`, `wiki/analyses/`.
3. **Install the schema.** Copy `templates/CLAUDE.md` → `<vault>/CLAUDE.md`, replacing `{{LAYOUT}}` with `flat` or `nested`. Copy `templates/AGENTS.md` → `<vault>/AGENTS.md`.
4. **Scaffold the wiki.** Copy `templates/index.md` → `<vault>/wiki/index.md`. Copy `templates/log.md` → `<vault>/wiki/log.md`, replacing `{{DATE}}` with today's date (YYYY-MM-DD) and `{{LAYOUT}}` with the layout choice.
5. **Optional extras.** If hot cache was requested, create `<vault>/wiki/hot.md` with a header comment only. Create `<vault>/raw/.gitkeep`.
6. **Gitignore.** If `<vault>/.gitignore` does not exist, copy `templates/gitignore` → `<vault>/.gitignore`. If it already exists, append any missing lines from the template — do not overwrite.
7. **Git init.** If `<vault>` is not already a git repo: `git init && git add . && git commit -m "chore: initialize LLM wiki"`. If it is already a git repo with a clean working tree, stage the new files and commit them separately as `chore: add LLM wiki scaffold`. If the repo has uncommitted changes, stop and ask the user how to proceed.
8. **Verify.** Read `<vault>/CLAUDE.md` back and confirm the `{{LAYOUT}}` placeholder was replaced. If it wasn't, fix it and amend (or create a follow-up commit).

## Report to user

On completion, print exactly:

```
LLM wiki initialized at <vault>

Layout: <flat|nested>
Hot cache: <yes|no>

Next steps:
1. Drop a source into <vault>/raw/ (PDF, markdown, web clip, transcript)
2. Open Claude Code in the vault:  cd <vault> && claude
3. Say: "Ingest the new source I just added to raw/"

Claude will read it, extract entities and concepts, write wiki pages,
update wiki/index.md, and append to wiki/log.md. A substantive source
typically touches 10–15 pages — that is normal and the whole point.

For periodic gap-filling research, install and run the wiki-self-heal skill.
```

## Notes

- The `CLAUDE.md` template is the hero file. It encodes the three-layer architecture, the routing table, naming conventions, workflows, and guardrails. Beginners read it to understand the system — it's also documentation, not just instructions for the LLM. Keep it intact during the copy; only `{{LAYOUT}}` is substituted.
- The `AGENTS.md` template is a minimal mirror for OpenAI Codex and other non-Claude agents that don't read CLAUDE.md.
- Never overwrite existing files without explicit user confirmation (steps 1 and 6).
- The vault is just a git repo of markdown files. No database, no embeddings, no vector store. That is intentional — naming conventions and `wiki/index.md` replace RAG infrastructure at this scale.
