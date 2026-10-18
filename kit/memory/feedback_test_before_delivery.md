---
name: feedback-test-before-delivery
description: Run the real flow and inspect the output before saying "done" on any file, macro, script or pipeline; never push verification onto the user
metadata:
  type: feedback
---
Before declaring any deliverable done, execute it end to end and inspect the result: run the macro via COM and dump the cells, reopen the generated file and check its contents, open each variant and confirm the difference is visible.

**Why:** "Done, run it to check" followed by a silently empty output wastes the user's time and breaks trust.

**How to apply:** Excel COM needs `Application.AutomationSecurity = 1` or macros silently do not run. Check output values, not only "no error thrown". If a check is impossible, say so explicitly. For parameter-driven macros, test several input scenarios (narrow, wide, empty) — the current data is one slice. Related: [[feedback-verify-before-claiming-fixed]].
