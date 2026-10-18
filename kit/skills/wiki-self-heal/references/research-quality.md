# Research Quality Gates

The single biggest failure mode of a self-heal skill is pulling low-quality content into the wiki. Every junk source you add to the wiki poisons every future query against it. These gates exist to prevent that.

**Guiding principle**: it is strictly better to skip a gap than to fill it with low-quality content. Never lower the bar.

## Question formulation

For each gap, write **1–3 specific research questions** before searching. Not "learn about X" — that produces vague searches and junk results. Instead:

- "When was X founded and by whom?"
- "What is the current industry adoption rate of X as of <recent period>?"
- "How does X differ from Y in <specific dimension>?"
- "What are the three primary criticisms of X and who made them?"

Specific questions → specific searches → high-quality sources. Write the questions down in your working notes before issuing any search.

## Source tier ranking

Prefer sources in this order. Always try to reach tier 1 or tier 2 before settling for lower.

**Tier 1 — Primary sources**:
- Original documents, official announcements, filings
- Peer-reviewed papers, preprints on arxiv.org / biorxiv.org
- Source code, specs, datasheets, regulatory filings (SEC, EMA, etc.)
- Official documentation from the vendor/project
- Government and standards-body publications

**Tier 2 — Reputable secondary**:
- Major outlets with editorial standards: Reuters, AP, NYT, FT, WSJ, The Economist, Nature News, Science Magazine
- Well-known domain publications: ArsTechnica, The Verge (for tech), BMJ, NEJM (for medicine)
- Wikipedia articles with strong citation density (and check the cited sources)

**Tier 3 — Acceptable with caution**:
- Official vendor blogs (acceptable for product facts, not for comparative claims)
- Well-maintained community wikis with citation requirements
- Stack Overflow accepted answers with source links
- Individual experts' personal blogs / Substacks **if** the author is verifiably credentialed in the topic

**Reject entirely**:
- SEO spam / "top 10" listicles without citations
- Content farms — domains that exist solely to rank in search. Recognizable patterns: `*/guides/*`, `*/tutorials/*` on hosting company domains, `*.io/blog/*` that mostly republishes competitor content, domains filled with AI-slop patterns
- AI-generated content without attribution or human review
- Opinion blogs cited as fact sources (use for opinions, not facts)
- Outdated content for time-sensitive claims — see recency gate below
- Single-source PR/press-release echoes across multiple outlets (counts as one source, not many)

## Two-source rule

**Every factual claim added to the wiki must have ≥ 2 independent qualifying sources.**

Independent = different publishers with independent editorial control. Five outlets republishing the same Reuters wire counts as **one** source, not five. Two academic papers from different research groups citing separate original data counts as two. One Tier-1 primary source (e.g. a company's own "Founded in 2019" statement) counts as definitive for that specific factual claim.

If only one qualifying source exists for a claim, you have three options:
1. Mark the claim in the page body as "single-source" with the caveat explicit
2. Skip the claim entirely
3. Skip the whole gap

**Never silently add a single-sourced factual claim to the wiki without the caveat.**

## Recency gate

For rapidly changing topics (AI, software, markets, policy, cybersecurity), reject sources older than **18 months** as primary evidence. If the gap is about current state and you can't find qualifying sources within the window → skip the gap.

For stable topics (history before recent decades, fundamental science, mathematics, geography), no recency cutoff applies.

For topics in between (business, politics, academia), prefer sources within 3 years but accept older sources if nothing newer exists and the claim is background rather than current-state.

## Citation format

Every new or updated page must record its sources in frontmatter:

```yaml
sources:
  - https://example.com/specific-article (accessed 2026-04-11)
  - https://another-source.org/paper (accessed 2026-04-11)
  - raw/local-source-file.md
```

Include the specific URL, not a homepage. Include the accessed date so future stale-claim scans work.

Inline citations in prose for specific claims: write `(<short-domain>, <year>)` at the end of the sentence making the claim.

Example:
```markdown
X was founded in 2019 (company.com, 2026) by two researchers from Stanford
(stanford.edu/news, 2019).
```

## When the gates fail

If no sources meet the quality bar for a gap:

1. **Skip the gap**. Do not lower the bar, do not fabricate.
2. **Record the skip** in the run summary: `skip: <gap-title> — reason: <specific reason>`. Example reasons:
   - `no qualifying sources within recency window`
   - `only single source found, claim too consequential to add with caveat`
   - `all found sources were content farms or SEO spam`
   - `search tool unavailable, fallback also failed`
3. **Suggest in the skip note** that the human find and add a primary source manually — give the specific research question the human would need to answer.

## Never

- **Never fabricate citations.** If a claim needs a source and none exists, skip the claim.
- **Never lower the quality bar** to "hit the target" of N gaps per run. It is correct to close a run with zero gaps addressed if quality gates fail on all prioritized gaps.
- **Never add AI-generated content from other agents** as a source (e.g. another LLM's answer to a question). Use only human-authored or primary-source material.
- **Never trust a domain you don't recognize** for factual claims without first verifying it against a Tier 1 or Tier 2 source on the same claim.
