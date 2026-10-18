# Log Entry Format

Every `wiki/log.md` entry starts with the grep-friendly prefix format (same convention as CLAUDE.md):

```
## [YYYY-MM-DD] <op> | <title>
```

Operations: `ingest`, `query`, `lint`, `update`, `init`.

For `wiki-self-heal`, the op is always `lint` and the title is always `self-heal pass`.

## Full template

Append exactly **one** entry per run, not one per gap. Consolidate.

```markdown
## [YYYY-MM-DD] lint | self-heal pass

**Branch**: wiki-heal/<tag>
**Audit**: <N> gaps found (HIGH: <h>, MEDIUM: <m>, LOW: <l>)
**Addressed**: <n>
**Skipped**: <s>

### New pages
- [[page-name]] — <one-line summary> — sources: <k>

### Updated pages
- [[page-name]] — <what changed, one line>

### Skipped gaps
- [<type>] <title> — reason: <short reason>

### Research tools used
<Exa / Firecrawl / Apify / WebSearch+WebFetch>

**Status**: keep
```

## Real example

```markdown
## [2026-04-11] lint | self-heal pass

**Branch**: wiki-heal/2026-04-11
**Audit**: 12 gaps found (HIGH: 4, MEDIUM: 5, LOW: 3)
**Addressed**: 3
**Skipped**: 9

### New pages
- [[progressive-overload]] — training principle of incrementally increasing stimulus — sources: 3
- [[mechanical-tension]] — primary driver of hypertrophy per 2025 consensus — sources: 4

### Updated pages
- [[hypertrophy-mechanisms]] — added "mechanical tension" section with [[mechanical-tension]] link

### Skipped gaps
- [contradiction] deload frequency — sources disagree (2-week vs 4-week), both authoritative — flagged for human
- [missing] [[bulgarian-training]] — only 1 qualifying source found — suggest user add primary source

### Research tools used
WebSearch + WebFetch

**Status**: keep
```

## Empty-run format

If the audit found zero gaps:

```markdown
## [YYYY-MM-DD] lint | self-heal — no gaps found

Scanned <N> pages. Wiki is clean. No action taken.
```

## Why the format matters

```bash
# Last 5 entries of any type
grep "^## \[" wiki/log.md | tail -5

# Last self-heal pass
grep "^## \[.*lint" wiki/log.md | tail -1

# All heal passes in 2026
awk '/^## \[2026-/,0' wiki/log.md | grep "lint | self-heal"

# Count heal passes in the last 90 days (rough)
grep "^## \[" wiki/log.md | grep "lint | self-heal" | tail -90 | wc -l
```

Consistent format = a queryable timeline of the wiki's evolution.

## Status values

- `keep` — changes committed, branch ready for review
- `skip` — no changes made (clean wiki or all gaps skipped)
- `flag` — human review needed before the branch should be merged (used when contradictions were found between authoritative sources)

Use `flag` instead of `keep` when the user should not merge the branch without reading the audit report first.
