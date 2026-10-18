---
name: feedback-sql-delivery-rules
description: SQL - always the complete runnable query, never guess a column, one change at a time
metadata:
  type: feedback
---
1. Always give the complete query ready to paste and run, never a snippet or "change line 42".
2. Never guess a column, table or type. Ship a discovery query (`INFORMATION_SCHEMA.COLUMNS`, `sys.columns`) first.
3. One change at a time; keep the rest byte-identical.
4. Answer first, then the query; caveats after the code. State any change in what a column means.

**Why:** a guessed column name or type costs a failed run against real data.
