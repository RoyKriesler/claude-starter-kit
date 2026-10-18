---
name: feedback-math-formula-formatting
description: Math goes in fenced code blocks as ASCII / unicode, never $$...$$ LaTeX; the terminal does not render LaTeX
metadata:
  type: feedback
---
The terminal shows LaTeX as raw source, unreadable.

**How to apply:** formulas in a fenced code block, e.g. `c0 = (a + y0 + y1/(1+r0)) / (1 + r)`. Greek letters as unicode (σ, ρ, β). Multi-line fractions are fine inside the block. Never inline math in a Hebrew sentence.
