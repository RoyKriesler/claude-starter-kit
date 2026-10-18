# Full Loop Procedure

The complete numbered procedure for a `wiki-self-heal` run. SKILL.md has the summary; this file has the details, edge cases, and exact commands.

## Setup phase

1. **Verify preconditions**:
   - `raw/` exists (directory)
   - `wiki/` exists (directory)
   - `CLAUDE.md` exists at vault root
   - `wiki/index.md` exists
   - `wiki/log.md` exists
   - If any missing → stop. Tell the user: "This vault is missing the Karpathy wiki structure. Run the `llm-wiki-setup` skill first."

2. **Verify git state**:
   - `git rev-parse --is-inside-work-tree` → must succeed. If not, `git init && git add . && git commit -m "chore: pre-heal snapshot"`.
   - `git status --porcelain` → must be empty. If dirty, stop and ask user to commit or stash.

3. **Ask about MCPs** (once per session):
   > I'll default to WebSearch + WebFetch for research. If you have any of these MCPs installed for higher-quality sources, let me know which and I'll prefer them: Apify, Firecrawl, Exa.

   Remember the answer for this run. Default: WebSearch + WebFetch only. Never block the loop on this — if the user is unresponsive, proceed with the default.

4. **Determine mode**: full (default) or audit-only. Audit-only runs when the user said "dry run", "just audit", "audit only", "don't make changes", or "show me the gaps first". If unsure, ask once before creating the branch.

4. **Create branch**:
   ```bash
   tag=$(date +%Y-%m-%d)
   # Append -2, -3, etc. if the branch already exists
   n=1
   while git show-ref --verify --quiet "refs/heads/wiki-heal/$tag$([ $n -gt 1 ] && echo -$n)"; do
     n=$((n+1))
   done
   suffix=$([ $n -gt 1 ] && echo -$n)
   git checkout -b "wiki-heal/$tag$suffix"
   ```

## Audit phase

5. **Read state**:
   - Read `CLAUDE.md` (the schema — tells you what this wiki is for)
   - Read `wiki/index.md` (the catalog — tells you what's in it)
   - Read last 10 entries of `wiki/log.md`: `grep "^## \[" wiki/log.md | tail -10`

6. **Run the audit** per the procedures in [audit.md](audit.md). Scan for all 6 gap types.

7. **Write findings** to `wiki/audits/audit-<date>.md`. Create the `wiki/audits/` directory if it doesn't exist.

   Format:
   ```markdown
   # Audit — YYYY-MM-DD

   ## HIGH (N)
   - [type] <title> — <details> — proposed: <fix>

   ## MEDIUM (N)
   - [type] <title> — <details> — proposed: <fix>

   ## LOW (N)
   - [type] <title> — <details> — proposed: <fix>
   ```

## Prioritization phase

8. **Pick top N gaps** (default N=3):
   - All HIGH before any MEDIUM before any LOW
   - Skip gaps that need human judgment (see "skip conditions" below)
   - Ties broken by: (1) gaps central to the vault's topic, inferred from `wiki/index.md` categories, (2) gaps addressable with WebSearch-quality sources

   **Skip conditions** (log and continue):
   - Contradictions between two authoritative primary sources — flag for human
   - Gaps requiring paywalled sources with no free equivalent
   - Gaps on topics where the wiki author has expressed opinion in CLAUDE.md notes
   - Any gap where the research questions would require private or hard-to-verify information

## Research phase

9. **For each prioritized gap**, per [research-quality.md](research-quality.md):
   a. Formulate 1–3 specific research questions.
   b. Run research tool (MCP if available in priority order: Exa → Firecrawl → Apify → WebSearch/WebFetch).
   c. Apply quality gates: ≥ 2 independent qualifying sources per claim, recency rules, source tier ranking.
   d. If gates pass → draft the new content with inline citations and frontmatter `sources:`.
   e. If gates fail → skip the gap, record the reason, move to the next gap.

## Apply phase

10. **Write or update pages**:
    - For new pages: create `wiki/<page-name>.md` with the full frontmatter and content
    - For updated pages: edit in place, preserve existing frontmatter, bump `last_updated`, append new sources to `sources:` list, do not silently overwrite contradictory claims — note disagreements explicitly
    - Add bidirectional `[[wikilinks]]` — if page A now references page B, ensure page B also has a link back (either in prose or in `related:` frontmatter)

11. **Update `wiki/index.md`**:
    - Add entries for new pages under the correct category
    - Update one-line summaries for pages that changed significantly
    - Do not reorder existing entries unless correcting a miscategorization

## Log + commit phase

12. **Append one consolidated entry** to `wiki/log.md` per [log-format.md](log-format.md). One entry per run, not one per gap.

13. **Commit**:
    ```bash
    git add wiki/
    git commit -m "heal: <n> gaps addressed, <s> skipped"
    ```
    Use the exact message format — the `heal:` prefix makes heal commits greppable.

14. **Do not merge. Do not push.** Leave the branch checked out. The human reviews with `git diff main..wiki-heal/<tag>` and merges if satisfied.

## Report phase

15. Print the final report in the format specified in SKILL.md. No additional commentary.

## Edge cases

- **Branch for today already exists**: append `-2`, `-3`, etc. as shown in step 4.
- **All gaps are human-review-only**: commit the audit report only (just `wiki/audits/audit-<date>.md`), append a log entry marking zero fixes, report to user, exit.
- **Audit finds zero gaps**: wiki is clean. Append a one-line log entry `## [YYYY-MM-DD] lint | self-heal — no gaps found`, commit, report "wiki is clean", exit.
- **Research tool crashes**: fall back to the next tool in priority order. If all fail, skip the gap, log the skip with reason `all research tools unavailable`, continue.
- **Git dirty state discovered mid-run**: stop immediately. Do not attempt to commit over the user's uncommitted work. Report and exit.
- **Branch drift > 50 commits from main**: stop immediately and report. This means previous heal branches weren't merged and something is wrong with the user's workflow.
- **Run interrupted**: the branch preserves partial progress. Re-running picks up where it left off (new audit, new branch if a new day).
- **Large vault (>500 pages)**: audit phase may take significant time. Budget: full audit should complete in < 10 minutes of LLM work. If it would take longer, scope the audit to categories mentioned in the last 30 days of log entries and note the scoping in the audit report.

## What NOT to do

- Do not merge the heal branch automatically.
- Do not modify files in `raw/`.
- Do not delete wiki pages — always flag instead.
- Do not add claims without ≥ 2 qualifying sources.
- Do not pause mid-loop to ask the human "should I continue?" (autonomy directive).
- Do not silently resolve contradictions — note them in both affected pages and let the human decide.
- Do not create stub pages (< 150 words) just to address a phantom-link gap — either research real content or flag the gap for later.
