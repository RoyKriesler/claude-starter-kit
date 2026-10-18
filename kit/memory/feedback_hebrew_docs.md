---
name: feedback-hebrew-docs
description: Hebrew DOCX, PPTX and PDF recipes - bidi at every level in Word, lang he-IL in PowerPoint, HTML + Chromium (never ReportLab) for PDF
metadata:
  type: feedback
---
**DOCX (python-docx):** set bidi at every level or Word silently falls back to LTR: `<w:bidi/>` in sectPr, docDefaults rPr `<w:rtl/>` + `<w:lang w:val="he-IL" w:bidi="he-IL"/>`, docDefaults pPr `<w:bidi/>`, Normal style pPr bidi + rPr rtl, every paragraph pPr `<w:bidi/>`, every run `<w:rtl/>`, tables `<w:bidiVisual/>`. Emit NO `<w:jc>` on RTL paragraphs: absence is what Word treats as right-aligned; `WD_ALIGN_PARAGRAPH.RIGHT` misleads the ribbon. Verify: count `<w:jc` = 0, render to PDF, look at 2 pages.

**PPTX (python-pptx):** `rtl="1"` on `a:pPr` is not enough; set `lang="he-IL"` on every `a:rPr` and an `a:cs` font. Segoe UI is a safe Hebrew font if Heebo is missing. `(Latin)` inside Hebrew chart labels renders broken — a PowerPoint quirk, accept it.

**PDF:** build HTML with `<html lang="he" dir="rtl">`, render with Playwright/Chromium or Edge headless. Never ReportLab + python-bidi: it reverses line order after wrapping. The `minimax-pdf` skill is Latin-only.

**Why:** each of these failed silently at least once and was caught only by rendering. Related: [[feedback-html-pdf-rules]], [[reference-docx-to-pdf-windows]].
