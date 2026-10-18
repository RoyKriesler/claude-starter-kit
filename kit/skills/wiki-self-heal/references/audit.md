# Audit Procedures

Six gap types. For each: scan method, severity rule, and fix template.

Table of contents:
1. [Orphan pages](#1-orphan-pages)
2. [Missing pages (phantom links)](#2-missing-pages-phantom-links)
3. [Contradictions](#3-contradictions)
4. [Stale claims](#4-stale-claims)
5. [Missing cross-references](#5-missing-cross-references)
6. [Data gaps (research candidates)](#6-data-gaps-research-candidates)

Severity rubric at the bottom.

---

## 1. Orphan pages

Pages in `wiki/` with zero inbound `[[wikilinks]]`.

**Scan**:
```bash
for f in wiki/*.md; do
  [ "$(basename "$f")" = "index.md" ] && continue
  [ "$(basename "$f")" = "log.md" ] && continue
  name=$(basename "$f" .md)
  count=$(grep -rl "\[\[$name\]\]" wiki/ --exclude="$(basename "$f")" 2>/dev/null | wc -l)
  [ "$count" -eq 0 ] && echo "ORPHAN: $name"
done
```

(Adapt for nested layout: use `wiki/**/*.md` glob or `find wiki -name "*.md"`.)

**Severity**:
- HIGH — if the page covers a major entity or concept central to the vault
- MEDIUM — if the page has substantial content (> 300 words) but nothing links to it
- LOW — otherwise

**Fix**: find pages that should reference this concept and add `[[wikilinks]]`. Never delete — flag for human if the page looks stale or off-topic.

---

## 2. Missing pages (phantom links)

`[[page-name]]` links that don't resolve to an existing file.

**Scan**:
```bash
grep -rhoE '\[\[[^]]+\]\]' wiki/ | sort -u | while read link; do
  name=$(echo "$link" | sed 's/\[\[//; s/\]\]//')
  [ ! -f "wiki/$name.md" ] && [ ! -f "wiki/entities/$name.md" ] && [ ! -f "wiki/concepts/$name.md" ] && echo "MISSING: $name (referenced)"
done
```

**Severity**:
- HIGH — referenced ≥ 3 times
- MEDIUM — referenced 2 times
- LOW — referenced 1 time

**Fix**: create the page. If the concept exists in `raw/`, extract content from there. Otherwise → research phase.

---

## 3. Contradictions

Two pages making mutually exclusive factual claims about the same subject.

**Scan**: this is LLM-driven, not grep-driven. Read pages in small batches (5–10 at a time). Look for:
- Conflicting dates ("founded in 2019" vs "founded in 2020")
- Conflicting numbers (market size, population, metric values)
- Conflicting causal claims (A caused B vs B caused A)
- Conflicting definitions (X means P vs X means Q)

Focus batches on pages that share tags or cross-reference the same entities — that's where contradictions actually live.

**Severity**: **always HIGH**. Contradictions erode trust in the whole wiki.

**Fix**:
- If one source is clearly authoritative and recent → update the outdated page, note the correction in both `sources:` frontmatters
- If sources conflict and both are authoritative → **flag for human**. Do not silently pick one. Add a note to both affected pages acknowledging the disagreement.

---

## 4. Stale claims

Time-sensitive claims that may have been superseded.

**Scan**: grep for time-sensitive language across pages with old `last_updated` frontmatter:

```bash
# Pages not updated in > 12 months
find wiki -name "*.md" -mtime +365

# Time-sensitive language inside those
grep -rhnE "(as of [0-9]{4}|currently|right now|latest|most recent|recently)" wiki/
```

**Severity**:
- HIGH — fast-moving topics (AI, software, policy, markets) with `last_updated` > 6 months
- MEDIUM — fast-moving topics with `last_updated` > 12 months, or stable topics > 24 months
- LOW — stable topics (history, chemistry, established science) regardless of age

**Fix**: research current state, update the claim, bump `last_updated`, append the new source.

---

## 5. Missing cross-references

Pages that mention another page's title without using `[[wikilinks]]`.

**Scan**: for each existing wiki page `X.md`, grep for its title (case-insensitive) across other pages. Where found without wrapping `[[...]]`, propose adding a link.

```bash
for f in wiki/*.md; do
  [ "$(basename "$f")" = "index.md" ] && continue
  name=$(basename "$f" .md)
  # Match the name as a word, not already inside [[...]]
  grep -rlE "\b$name\b" wiki/ --exclude="$(basename "$f")" | while read other; do
    if ! grep -q "\[\[$name\]\]" "$other"; then
      echo "MISSING_XREF: $other → $name"
    fi
  done
done
```

**Severity**: **always LOW** — cosmetic, but compounds over time. Do these in batches during low-budget runs.

**Fix**: add `[[wikilinks]]` in-place. Bidirectional — if A now references B, verify B's `related:` frontmatter includes A.

---

## 6. Data gaps (research candidates)

The main auto-learn engine. Concepts mentioned multiple times without dedicated coverage, or thin stubs on important topics.

**Scan**: two subtypes.

**6a. Referenced concepts without pages** — terms that appear frequently across wiki pages but have no dedicated page. Different from phantom links (#2): these aren't wrapped in `[[...]]` yet, but they probably should be. Use a simple frequency count on proper-noun-ish tokens (capitalized multi-word phrases).

**6b. Stub pages on important topics** — pages shorter than 200 words whose `tags:` or position in `index.md` suggests the topic is central to the vault.

```bash
# Stubs
for f in wiki/*.md; do
  wc=$(wc -w < "$f")
  [ "$wc" -lt 200 ] && echo "STUB: $(basename "$f" .md) ($wc words)"
done
```

**Severity**:
- HIGH — concepts that appear in `wiki/index.md` categories explicitly (central to the vault) — these are the primary research targets
- MEDIUM — concepts mentioned ≥ 3 times across different pages
- LOW — everything else

**Fix**: research + create new page OR expand existing stub. This is where the research quality gates matter most — see [research-quality.md](research-quality.md).

---

## Severity rubric (summary)

- **HIGH** — affects factual trust, or central to the vault's topic. Fix this run.
- **MEDIUM** — improves coverage or recency. Fix if budget allows.
- **LOW** — cosmetic / cleanup. Skip unless specifically requested or on a cleanup-focused run.

## Audit output format

Write the audit to `wiki/audits/audit-<YYYY-MM-DD>.md`:

```markdown
# Audit — YYYY-MM-DD

Scanned N pages. Found X gaps.

## HIGH (N)
- [orphan] <title> — <details> — proposed: <fix>
- [missing] <title> — referenced <k> times — proposed: research + create
- [contradiction] <pageA> vs <pageB> on <claim> — proposed: <fix or flag>

## MEDIUM (N)
- [stale] <title> — last_updated <date>, time-sensitive language found — proposed: research + update
- [data-gap] <title> — <k>-word stub — proposed: research + expand

## LOW (N)
- [xref] <pageA> → <pageB> — proposed: add [[wikilink]]
```
