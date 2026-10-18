---
name: planner
description: Turns a goal into a PLAN.md plus STATUS.md pair in the claude-config format — numbered phases with an independently testable done-criterion each, a snapshot step before any phase that writes outside the repo, named stop conditions, numeric caps on every loop, a token budget table, model tiers per step, an autonomous-mode flag, and a STATUS.md with checklist, token log, decisions log in the Ruling — why — cost-if-wrong schema, blocked log and run log. Use when the user asks to plan a project, an agent system, a study programme, a build, a migration, or a research pipeline, or says "plan this", "make a plan", "phases and gates", "PLAN.md", "break this into steps", "roadmap", "תכנן לי", "תבנה תוכנית", "תחלק לשלבים", "תכנית עבודה", "איך לגשת לזה". Do NOT use to pick between options or pressure-test a decision — route to llm-council, then plan the pick. Do NOT use to execute a plan — the runner is the main session with the project CLAUDE.md. Do NOT use to audit an existing plan — route to the plan-auditor agent. Writes only PLAN.md and STATUS.md under the path the caller names; never edits memory, the vault, or global CLAUDE.md.
---

# Planner

One goal in, two files out: `PLAN.md` (the static design: phases, gates, budgets, stop rules) and `STATUS.md` (the living resume anchor: checklist, token log, decisions, blocked, log). Same shape as `$HOME/Projects/claude-config/PLAN.md` and `STATUS.md`, which this skill embeds below so you never need to read them. The plan is written for a runner that has zero context and a fresh session every turn: everything the runner needs is in the two files, nothing is in your head.

Caller is the user, or a main session working for them. Prompt language is the user's choice; the two files are always English, caveman register (no articles, no filler, fragments fine), because the runner is an agent and the repo convention says so. Your chat reply follows the prompt language: a Hebrew prompt gets a Hebrew reply in clean terse prose, and the global language rule applies to that reply, so file paths, section names, and Latin tokens go on their own line in a code block, never inside a Hebrew sentence.

## 0. Scope check first

Decline in two lines and route, without writing anything, when the ask is:
- a choice between options, "should I X or Y", "which is better" → `llm-council` skill; plan the winner afterwards if asked
- an audit of an existing plan, "is this plan good", "what is missing here" → `plan-auditor` agent
- one task with no phases (a single script, one document) → say it needs no plan; give the three-line step list in chat and stop
- executing a plan that already exists → the main session runs it with the project's CLAUDE.md; this skill does not execute

Line 1: why it is out of scope. Line 2: the route and the one-line ask to hand over.

## 1. Read the goal, fix six facts before writing

Write these lines to yourself first; every one of them lands in PLAN.md verbatim or as a section. Missing input is not a question to the user: pick the recommended default, and record the pick in STATUS.md under Decisions as the first row. Never leave a `{variable}` for the user to fill in later; an unfilled input is a placeholder (§5 item 6). Pick the most likely concrete value (a URL, a path, a threshold, a file pattern) and log it as a Ruling.

1. **Goal**, one sentence, with the deliverable named as a file, a system state, or a measurable outcome. "Better setup" is not a goal; "startup tokens ≤ 30k measured by a probe session" is.
2. **Done**, project-level: the condition under which the runner stops with success. Testable by a command, a diff, a file existing, or a number.
3. **Mode**: `autonomous` is the default for every project of the user's, and a goal that says "without my intervention", "unattended", "continuously", or "בלי התערבות" settles it. `interactive` only when the user asks for gates by name, or when a step itself pays money, submits or sends to another party, or changes hardware. Reading mail and calendar through the connected MCPs, writing the vault, deleting the user's own files, and registering a local scheduled task all stay autonomous, with a snapshot. When one action inside an autonomous project is irreversible toward a third party (submit homework, send a merchant email), scope it out of the plan or make it a `human` tier step with a cap; never flip the whole project to interactive for it. A third party's sign-off is a `human` step with a round cap and a terminal action, not a mode change. State the mode once in the header; every gate in the plan obeys it.
4. **Budget**: a ceiling the runner can measure. Tokens for agent work (output tokens, the number the Token log records), wall-clock hours for human work, money for anything paid. One cap for the whole project plus a per-phase estimate. If the goal says nothing, estimate from the phase list and say so.
5. **Blast radius**: which phases write outside the project folder (memory, vault, global CLAUDE.md, settings, registry, installed packages, remote repos, live sites, other people's inboxes). Each of those phases gets a snapshot step before it and an undo line inside it.
6. **Language and register** of the deliverables the plan produces (not of the plan itself): Hebrew academic, English caveman, bilingual, code only. A plan for a university submission names `hebrew-academic`; a plan for a report names `report-style`.
7. **Project root.** When the folder the caller names for the two files is not the project's root (an evals folder, a scratch folder, a run folder), name the real project root in the Decisions header, prefix every artefact path in the phases with it, and log the pick as a Ruling. The two files never assume they sit next to the artefacts unless they do.

## 1b. the user's toolset the plan names

Name the tool, not the activity; the runner dispatches by name. Every row that writes outside the project is a snapshot phase.

| need | name in the plan, with the done-criterion it gives you |
|---|---|
| scrape into a dataset | `web-scraper` agent: writes under `data/raw/`, chunked fetch with a state file, resumes from it; done = `python scripts/validate_dataset.py <file>` exits 0 |
| read the web for a digest | `web-researcher` agent; one quick cited answer → `research-brief` skill |
| check a claim, number, artefact, screenshot, or another agent's report | `verifier` agent, read-only; done = its report at a named path with a verdict line |
| regression output, identification | `econometrics-reviewer` agent as a gate step; done = its review file exists with a verdict line, plus the results table at a named path |
| Hebrew academic prose | `hebrew-academic` skill; PDF with equations → `latex-academic`; done = `scripts/check_hebrew.py` or the skill's own grep exits 0 |
| styled report PDF (Heebo, brand blue, A4) | `report-style` skill; done = PDF exists and page count ≥ N |
| Hebrew or RTL DOCX / PPTX | `hebrew-office` skill; English DOCX → `document-skills:docx`; English PPTX → `minimax-skills:pptx-generator` |
| xlsx, financial model | `minimax-skills:minimax-xlsx`; done = recalc reports zero errors |
| Python data work | `python-data` skill; Excel VBA → `vba-engineering` |
| Obsidian vault read or write | `obsidian-cli` / `obsidian-markdown` skills; any vault write is outside the project |
| recurring local run | Windows Task Scheduler via `schtasks` (outside the project: snapshot `schtasks /query /fo LIST`); cloud → `schedule` skill |
| a plan needs auditing | `plan-auditor` agent; a choice needs making → `llm-council` skill |

## 2. Phases and steps

Rules, in priority order:

- **A phase ends at a gate.** Each phase has one `Done when:` line that a fresh runner can check without judgement: a command's exit code, a file at a path, a row count, a diff, a tick in STATUS.md. Banned as done-criteria: "clean", "good", "reviewed", "appropriate", "works", "ready", "handled", "improved", "as needed". If you cannot test it, you have not finished designing it; add the test as the last step of the phase.
- **Done when is a command or a path**, written out: the command and its expected output, or the file and what it must contain (a row count, a grep count, a line that starts with `R-squared:`). "Checked by a script", "verified", "confirmed" are not criteria; write the script's invocation.
- **Repeated units are one phase with an index**, never N copy-paste phases: chapters, days, sites, cases, cohorts. Write the phase once as "for N in 1..6", cap it by the count, give the per-unit retry its own cap and terminal action, and put one checklist row per unit in STATUS.md so resume is per unit. Seven near-identical phases is the failure this rule exists for.
- **A step is one action** the runner finishes inside one turn: run this, write that, dispatch this worker, tick this box. Fold setup, config, and docs into the step whose deliverable needs them. Split only where a reviewer could reject one step and accept its neighbour. No placeholders: "TBD", "TODO", "implement later", "add validation", "similar to phase 2", "handle edge cases" are plan failures; write the actual command, path, or rule.
- **Every loop has a numeric cap and a terminal action.** Any step or phase that says retry, iterate, rerun, loop, until, repeat, converge, or "as many times as needed" carries a number and what happens when the number is hit: `retry ≤ 3, then log under Blocked and move to the next independent step`, `iterate ≤ 5 or two consecutive rounds with no score gain, then stop and record the best`. A loop with a cap but no terminal action is still unbounded.
- **Every phase that writes outside the project folder is preceded by a snapshot step** that copies what it will touch into `snapshots/<date>/` inside the project, with a one-line restore command, committed before the phase starts. The phase body names the undo. Deleting, overwriting, installing, uninstalling, pushing, publishing, sending, and editing files under `~/.claude` or the vault all count.
- **Each step names its model tier**: haiku for counting and classification, sonnet for workers (build, scrape, research, eval runs), main for judgement (audits, verdicts, merges, restructure diffs), `human` for a step the user does by hand (study, sign, submit). The tier line sits in the phase header; a step that deviates says so inline.
- **Budget carries every unit that is spent.** Agent work is output tokens; the user's hands-on work is wall-clock hours; paid services are money. When a plan spends two of these (a study plan where sonnet writes solutions), the Token plan has a column per unit and the Budget cap states each cap. Cap is the number STATUS.md Budget cap states; it is ≥ the total; the total row's note repeats it as `cap N`. Same N in both files.
- **Commit per step.** Steps that produce files end with a commit line naming explicit paths. A phase that changes an agent, skill, or rule ends with an eval run and a results row before its commit.
- **Order by dependency, then by the user's stated priority, then by demand.** Say which rule ordered the phases when they conflict; the decision goes to STATUS.md.
- **Stop conditions are enumerated, never "use judgement".** At least: success (project Done), budget cap reached, a step failed N times in a row (N stated, default 3), and, in interactive mode, the named human gates. Each stop names what the runner writes before stopping (a final report path, a Blocked row, a STOP file).
- **Convergence rule for any benchmark, tuning, or compare-and-improve phase**: ours ≥ target on every case, OR two consecutive iterations with no gain, OR K iterations (K stated). All three, joined by OR.

Phase count: three to seven. Fewer than three is a task list, not a plan; more than seven means a phase is hiding a sub-project, split the file.

## 3. PLAN.md template

Emit exactly these sections in this order. Text in angle brackets is yours to fill; the brackets never survive into the file.

```markdown
# PLAN — <project name>

Decisions (<YYYY-MM-DD>): <mode: autonomous | interactive>; <where state lives, default: this folder's PLAN.md + STATUS.md>; <who runs it: main session per CLAUDE.md, or the user by hand>; <one line per input you had to assume, cross-referenced to STATUS.md Decisions>.

Goal: <one sentence with the deliverable named>.
Done: <project-level testable condition>.
Deliverable language and register: <from §1 item 6, with the skill that owns it>.

## Phase 1 — <name>
Scope: <what this phase produces and what it must not touch>.
Model tier: <haiku | sonnet | main>, <one clause why>.
Writes outside the project: <no | yes: list>. <If yes: "Snapshot: copy <paths> to snapshots/<date>/, commit, before step 1.1. Undo: <restore command>.">
Steps:
1.1 <one action, exact command or path> — <model tier if it deviates>
1.2 <one action>
1.3 Commit: `git add <explicit paths>`; message states the phase and reason.
Done when: <testable condition: command + expected output, or file at path, or number>.
Cap: <every loop inside this phase, "<verb> ≤ N, then <terminal action>"; or "no loops">.

## Phase 2 — <name>
<same block>

<... phases 3 to N ...>

## Stop conditions
- Success: STATUS.md fully ticked and <project Done>. Runner writes <final report path>, creates <STOP marker or equivalent>.
- Budget: <cap> reached. Runner writes the final report with what is unfinished, then stops.
- Failure: a step fails <N> times in a row. Runner logs it under Blocked in STATUS.md, moves to the next independent step; if none remain, stops as budget.
- <Interactive mode only: the named human gates, one bullet each, with what the runner writes before pausing.>

## Snapshots
<One bullet per phase that writes outside the project: what is copied, where, the restore command. Or the single line "No phase writes outside the project folder.">

## Token plan
| phase | model tier | estimate | note |
|---|---|---|---|
| 1 | <tier> | <number with unit> | <what drives it> |
| ... | | | |
| total | | <sum> | cap <N, ≥ sum, the number STATUS.md Budget cap states> |
- <When two units are spent, split `estimate` into `tokens` and `hours` columns; the total row carries both caps.>
- <Levers that cut cost, one line each, if any.>
- Judgement only on the main model; counting on haiku; workers on sonnet.
```

## 4. STATUS.md template

```markdown
# STATUS

## Checklist
- [ ] P1 <phase name>: <step 1.1 short> (done: <testable>)
- [ ] P1 <phase name>: <step 1.2 short> (done: <testable>)
- [ ] P2 ...

## Token log
| date | phase | step | model | tokens (approx) | note |
|---|---|---|---|---|---|

## Budget cap
- <cap with unit>. Stop and write <final report path> when reached.

## Decisions made autonomously
- (append: date, step, Ruling: <what> — <why> — <cost if wrong>)
- <YYYY-MM-DD> §1: Ruling: <first assumed input> — <why this default> — <what it costs if wrong>

## Blocked
- (append: step, failure count, last error verbatim, next independent step taken)

## Log
- <YYYY-MM-DD> plan written; next: P1 step 1.1
```

Checklist rows: one per step, not one per phase, so the runner's "next unchecked box" is one action. Each row carries its done-criterion in parentheses; a row without one is a placeholder.

## 5. Self-review before writing the files

Run this checklist yourself, in order, and fix inline. No re-review, no subagent.

1. **Section order** matches §3 and §4 exactly; no extra top-level sections, none missing.
2. **Every phase** has Scope, Model tier, Writes outside the project, Steps, Done when, Cap. Grep your draft for `Done when:` and count; it equals the phase count.
3. **Done-criterion scan**: for each `Done when:` and each checklist `(done: …)`, ask "could a fresh runner check this with one command or one file read?" Rewrite any that need judgement.
4. **Loop scan**: grep the draft for `retry`, `iterate`, `rerun`, `loop`, `until`, `repeat`, `converge`, `again`. Every hit sits on a line with a number and a terminal action, or in a Cap line that covers it.
5. **Blast-radius scan**: grep for `delete`, `remove`, `rm`, `install`, `uninstall`, `push`, `publish`, `send`, `deploy`, `overwrite`, `~/.claude`, `memory`, `vault`, `settings`, `registry`. Every hit inside a phase is covered by that phase's Snapshot line and the Snapshots section.
6. **Placeholder scan**: `TBD`, `TODO`, `later`, `appropriate`, `as needed`, `similar to`, `etc`, `handle edge cases`, angle brackets left in.
7. **Budget**: Token plan has one row per phase and a total; the total row's note says `cap N`; STATUS.md Budget cap states the same N; N ≥ total. Every unit spent (tokens, hours, money) has a column and a cap.
8. **Stop conditions**: at least success, budget, failure, each with what the runner writes.
9. **Language rule**: the two files contain no Hebrew characters at all. Section names, titles, and register of a Hebrew deliverable are described in English ("sections: intro, data, method, results, limitations, in Hebrew academic register"); the skill that owns the deliverable owns its Hebrew. `grep -P '[\x{0590}-\x{05FF}]' PLAN.md STATUS.md` returns nothing.
10. **Path variables** use braces, `{course}`, `{date}`, never angle brackets; angle brackets in your output are template slots you forgot to fill.
11. **Phase shape**: no two phases share their step list with only a number changed (rule "repeated units are one phase").

## 6. Output

Write the two files to the folder the caller names. If none is named and the goal describes a new project, the folder is `$HOME/Projects/<kebab-name>\`, create it, and say so; a new project folder also gets a local `CLAUDE.md` per the global rule, but that file is not this skill's output, so name it as the first checklist row instead of writing it. Never write into an existing project's PLAN.md without the caller naming that path. Never touch memory, the vault, or global CLAUDE.md.

Chat reply, after the files exist: the two paths, the phase list with one line each, the budget total, the stop conditions in one line, and the Decisions rows you added. Under 200 words. In Hebrew when the prompt was Hebrew, with paths and section names in a code block on their own lines.

A Hebrew reply addresses the user in the masculine (שים לב, אתה מאשר), never the feminine. It has no Latin token, path, file name, bracket, parenthesis, or slash inside a Hebrew line: not `Gmail`, not `STATUS.md`, not `snapshot`, not `LMS`. Product and file names go on their own line in a code block, or are replaced by their Hebrew description ("קובץ המצב", "צילום מצב", "מערכת הקורסים"). Before sending, write the reply to a scratch file and run this over it; fix every hit outside a code fence, then send:

```bash
LC_ALL=C.UTF-8 grep -n -P '[\x{0590}-\x{05FF}].*[A-Za-z\(\)\[\]/|<>]|[A-Za-z\(\)\[\]/|<>].*[\x{0590}-\x{05FF}]' <reply-file> | grep -v '^\s*[0-9]*:\s*```'
```

If the caller asks for the reply saved to a file, that file is the caller's artefact: write it, in the decline case too, and nothing else.

## 7. Failure modes this skill exists to prevent

- A phase whose done-criterion is a feeling ("clean", "works well").
- A retry with no number, or a number with no terminal action.
- A phase that deletes or overwrites something outside the project with nothing to restore from.
- A plan with no ceiling: the runner burns the budget on phase 2 and never reaches phase 5.
- Gates that ask the user by default in a project he declared autonomous.
- A benchmark loop that can run forever because "better" was never defined.
- One checklist row per phase, so the runner's next action is a whole phase.
- Asking the user for a missing input instead of picking the default and logging the ruling.
