---
name: feedback-autonomous-run-cost-control
description: Long autonomous runs need a per-step token cap, a stop rule, and a judge that is not the author, written down before launch
metadata:
  type: feedback
---
Unbounded "iterate until perfect" loops burn the shared Claude usage window and any paid API budget.

**How to apply:** before a long or scheduled run, write into the project's CLAUDE.md or PLAN.md: per-step cap, max iterations, budget line for any paid service, and who grades the result (not the session that wrote it). Report spend vs plan in every status update. The `planner` skill and `plan-auditor` agent enforce this.
