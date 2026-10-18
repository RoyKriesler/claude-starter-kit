---
name: feedback-no-hebrew-tables
description: No Markdown tables with Hebrew content; use numbered sections with bold labels
metadata:
  type: feedback
---
Markdown tables with Hebrew cells render broken: bidi flips column order and pipes misalign.

**How to apply:** use `### 1. <title>` then `- **<field>:** <value>` lines. Tables are fine when every cell is English, numbers or code. A grid that must exist goes as ASCII inside a code block. Related: [[feedback-no-language-mixing]].
