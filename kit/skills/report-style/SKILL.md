---
name: report-style
description: Styled HTML-to-PDF research and investment reports in house report design — Heebo font, brand blue 2c5282, 880px screen width, RTL, semantic finding boxes, no emoji, A4 mm page sizing, Edge headless PDF export. Triggers on "דוח", "report PDF", "כמו הדוח של לונדון", "finding box", "investment report", "research report", or any styled HTML/PDF investment or research report deliverable. This skill owns the CSS, page sizing, and Edge headless mechanics; the presentation rules — micro-first analysis, econometric register, the 8-component finding card, and the mandatory ticker/price/₪ recommendation — live in memory `reference_report_presentation_rules.md` and are not repeated here. Not for an English-language DOCX report — route to document-skills:docx. Not for a Hebrew DOCX or PPTX deliverable — route to hebrew-office.
---

# Report Style

Mechanics for building the user's styled HTML report and exporting it to PDF with Edge headless, in one standard house design. Content rules (recommendation first, finding cards, no emoji) live in memory `reference_report_presentation_rules.md` when present. This skill is the *how*: CSS, page sizing, break rules, the Edge command, and PDF verification.

## 1. CSS tokens — paste this block

Two width regimes exist and must not be mixed. `880px` is the **screen/webview** width the user asked for by name. A4 print content area is only ~178mm (≈673px), so 880px never fits inside `@page` sizing — the print block below deliberately does not inherit the screen width. Author reports with this full CSS block; do not improvise colors or box classes.

```css
/* ==== report-style tokens (house report design) ==== */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700&display=swap');

:root {
  --brand: #2c5282;   /* primary */
  --bad:   #c53030;   /* chart / box: negative */
  --good:  #2f855a;   /* chart / box: positive */
  --warn:  #d69e2e;   /* chart / box: caution */
  --muted: #718096;   /* chart / box: neutral */
}

/* ---- screen / webview ---- */
body {
  font-family: 'Heebo', 'DejaVu Sans', sans-serif;
  direction: rtl;
  max-width: 880px;
  margin: 0 auto;
  color: #1a202c;
  line-height: 1.6;
  padding: 24px;
}

h1, h2, h3 { break-after: avoid; page-break-after: avoid; }
h2 { border-right: 4px solid var(--brand); padding-right: 12px; }

table { border-collapse: collapse; width: 100%; }
th { background: var(--brand); color: #fff; padding: 8px 12px; }
td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }

/* 5-column stat grid, 2-column under 768px */
.stat-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
@media (max-width: 768px) { .stat-grid { grid-template-columns: repeat(2, 1fr); } }
.stat-card { border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; text-align: center; }

/* equation blocks: monospace, forced LTR inside RTL body */
.equation {
  font-family: 'Courier New', monospace;
  direction: ltr;
  text-align: left;
  background: #f7fafc;
  padding: 10px 14px;
  border-radius: 4px;
  margin: 12px 0;
}

/* semantic boxes */
.finding-box        { border-right: 4px solid var(--good);  background: #f0fff4; padding: 12px 16px; margin: 12px 0; }
.hypothesis-box      { border-right: 4px solid var(--brand); background: #ebf8ff; padding: 12px 16px; margin: 12px 0; }
.warning-box         { border-right: 4px solid var(--bad);   background: #fff5f5; padding: 12px 16px; margin: 12px 0; }
.caveat              { border-right: 4px solid var(--warn);  background: #fffaf0; padding: 12px 16px; margin: 12px 0; }
.glossary-box        { border-right: 4px solid #d69e2e;      background: #fffff0; padding: 12px 16px; margin: 12px 0; }
.abstract            { border-right: 4px solid var(--muted); background: #f7fafc; padding: 12px 16px; margin: 12px 0; }
.recommendation-box  { border: 2px solid var(--good); padding: 16px; margin: 16px 0; }

/* never split a box or card across a page break (see section 3) */
.finding-box, .hypothesis-box, .warning-box, .caveat, .glossary-box,
.abstract, .recommendation-box, .finding-card, .verdict, .fig, .stat-card {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* ---- print / PDF: mm units, A4, no inherited px width ---- */
@page { size: A4; margin: 0; }

@media print {
  body { max-width: none; margin: 0; padding: 0; }
  .page {
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    padding: 18mm 16mm;
    box-sizing: border-box;   /* without this the padding adds to 297mm and spills a blank page */
    overflow: hidden;
  }
  table { table-layout: fixed; }   /* width:100% alone does not cap intrinsic column width */
}
```

Chart palette (matplotlib / any chart lib, not just CSS): use the same four hex values above — `#2f855a` good, `#c53030` bad, `#d69e2e` warn, `#718096` muted — max 3 colours per chart. Chart *content* rules (Tufte spines, direct labels, annotation) are in `reference_report_presentation_rules.md`; this skill only fixes the palette.

No emoji anywhere in a report — body, boxes, chart labels, or prompts. Not `✓`, not `⚠️`. Use the semantic box color instead of an emoji to signal severity.

No Hebrew Markdown tables — Hebrew/English mixed table cells break RTL rendering the same way mixed-language prose does. Build tables as HTML (`<table>` with the CSS above), never as a Markdown pipe table, when any cell is Hebrew.

## 2. Page sizing

Default paper size in headless Chrome/Edge is **Letter** (816×1056px @96dpi), not A4. A layout authored at 880px screen width, or any layout missing an explicit `@page` rule, gets silently clipped on the trailing edge when printed — Edge does not scale, it clips. This bit the user on a team guide where `.page { width: 880px }` overflowed the Letter print viewport; caught only after a screenshot.

Rules, every time a report goes to PDF:
1. Set `@page { size: A4; margin: 0; }` in the stylesheet (A4 is the user's default; Letter only if he asks).
2. Give the print container mm units, not px: `.page { width: 210mm; min-height: 297mm; }` (see CSS block above).
3. A4 portrait content area after 16mm horizontal padding is ≈178mm ≈ 673px. Any table, wide badge row, or pill group must fit inside that — check widths before export, not after. A fixed px width on the table is not enough on its own: set `table-layout: fixed` (in the print block above) or the table keeps its intrinsic content width and clips the trailing column.
4. For dense content (wide tables, side-by-side charts) prefer `@page { size: A4 landscape; }` — content area ≈265mm ≈1000px — over shrinking fonts to fit portrait.

If the user reports clipped text from a screenshot, the cause is almost always a missing `@page` rule or a px width exceeding the print viewport. Check those two things first.

## 3. Layout — break rules and the Edge command

**Never let a heading land alone at the bottom of a page**, and never let a box or card split across a page boundary:

```css
h1, h2, h3 { break-after: avoid; page-break-after: avoid; }
.finding-card, .verdict, .fig,
.finding-box, .hypothesis-box, .warning-box, .caveat,
.glossary-box, .abstract, .recommendation-box, .stat-card {
  break-inside: avoid; page-break-inside: avoid;
}
```
(Already included in the CSS block in section 1 — this is the rule behind it.)

**Strip the browser's default header/footer.** Edge/Chrome headless prints the source URL and a page number onto every page unless told not to. the user sees this immediately on his Edge PDF viewer. Pass **both** flags — order matters and one alone is sometimes silently ignored:

```
--print-to-pdf-no-header
--no-pdf-header-footer
```

**Edge headless command template** (PowerShell):

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  --headless --disable-gpu `
  --print-to-pdf="C:\path\to\output.pdf" `
  --print-to-pdf-no-header `
  --no-pdf-header-footer `
  "file:///C:/path/to/report.html"
```

Both header-suppression flags are belt-and-suspenders; keep both even if one alone appears to work on a given Edge build.

## 4. Structure

- Cover page, then findings as cards, then the recommendation, then appendix. Card content structure (8 components: takeaway, question, method, chart, numbers, interpretation, caveats, next step) and the micro-first content rule are owned by `reference_report_presentation_rules.md` — read it before drafting card content, this skill does not restate it.
- The recommendation is mandatory and is its own `<h1>המלצת השקעה</h1>` section, injected before `מטריצת סיכונים` (risk matrix) near the end of the document — not left for the model to place ad hoc. If a draft is missing this section, add it before calling the report done; do not deliver a report without ticker, price target, and an ₪ entry/exit figure in that section. The ₪ requirement means the glyph itself; the Hebrew abbreviation ש"ח does not satisfy it.
- No emoji anywhere (section 1). No Hebrew Markdown tables (section 1) — HTML tables only when any cell is Hebrew.

## 5. Verification — render before calling it done

Never hand off a PDF unread. Render every page to an image and inspect for clipping (section 2), orphan headings (section 3), and stray footer text (section 3) before delivery:

```python
import fitz  # PyMuPDF

doc = fitz.open(r"C:\path\to\output.pdf")
print(f"pages: {doc.page_count}")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(f"page_{i + 1}.png")
    if not page.get_text().strip():
        print(f"WARNING: page {i + 1} has no extractable text (image-only or blank)")
# This script catches blank pages only. Clipping and orphan headings do NOT
# show up here (word bboxes stay in-bounds even when Edge clips them): open
# the PNGs and check by eye, every page.
doc.close()
```

Then open the PNGs (or the PDF itself) and check, page by page:
- No table or content block cut off at the trailing (right, for RTL) edge — the section 2 clipping failure mode.
- No section heading alone at the bottom of a page with its content pushed to the next — the section 3 break-after failure mode.
- No URL or page-number footer from the browser — the section 3 header-suppression failure mode.
- The `המלצת השקעה` section is present, before the risk matrix, with a ticker, a price target, and an ₪ figure.
- No emoji, no Hebrew Markdown table, anywhere in the rendered output.

Only report the deliverable done after this check passes.
