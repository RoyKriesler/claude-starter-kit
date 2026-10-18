---
name: feedback-no-language-mixing
description: Hebrew sentences contain only Hebrew; English tokens, paths, commands and bidi-breaking punctuation go on their own line
metadata:
  type: feedback
---
Never put English words, even short ones like SQL, API, PDF, GitHub, inside a Hebrew sentence. Never put parentheses, brackets, braces, slashes, pipes or angle brackets inside Hebrew prose.

**Why:** Hebrew is RTL, English is LTR. Mixing them, or using LTR-strong punctuation, scrambles the visual order of the whole line in the terminal.

**How to apply:** English terms go in a code block on their own line, or translate them. Replace `(...)` with a comma, an em-dash or a new line. Each bullet is fully Hebrew or fully English. Backticks do not make English safe inside Hebrew. Related: [[feedback-no-hebrew-tables]].
