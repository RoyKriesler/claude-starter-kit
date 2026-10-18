---
name: feedback-html-pdf-rules
description: HTML to PDF - explicit @page A4 + mm units, both no-header flags, no orphan headings, no emoji
metadata:
  type: feedback
---
Edge/Chrome headless defaults to Letter (816px wide); px layouts wider than that get clipped silently.

**How to apply on every HTML→PDF build:**
```css
@page { size: A4; margin: 0; }
.page { width: 210mm; min-height: 297mm; padding: 18mm 16mm; }
h1, h2, h3 { break-after: avoid; page-break-after: avoid; }
.card { break-inside: avoid; page-break-inside: avoid; }
```
Pass both `--print-to-pdf-no-header` and `--no-pdf-header-footer` or the URL and page number print on every page. A4 content width with 16mm padding is ~673px. No emoji in reports. Recommendation goes before the risk section. Clipped text in a screenshot = missing `@page` or px width too wide. Related: [[feedback-hebrew-docs]].
