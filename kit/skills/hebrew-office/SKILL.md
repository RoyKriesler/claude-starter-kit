---
name: hebrew-office
description: Hebrew or RTL DOCX and PPTX generation with python-docx and python-pptx, plus DOCX to PDF conversion on the Windows machine. Use whenever the user asks for a Hebrew Word document, a Hebrew PowerPoint, or a DOCX turned into a PDF. Triggers on "מסמך וורד", "קובץ וורד בעברית", "מצגת בעברית", "Hebrew docx", "RTL pptx", "convert to PDF", "Word hangs", and any Hebrew document deliverable. Not for English-language documents or decks — route those to document-skills:docx or minimax-skills:pptx-generator. Not for styled HTML-to-PDF investment or research reports — route those to report-style.
---

# Hebrew Office Documents

Generate correct Hebrew/RTL Word and PowerPoint files, and convert DOCX to PDF reliably on the Windows machine. Three failure modes drive every rule here: Word silently falls back to LTR when bidi is missing at any one of five levels, PowerPoint scrambles Hebrew punctuation unless `lang="he-IL"` is set on every run, and Word's COM automation hangs — especially on OneDrive paths.

## Scope check first

- English-language DOCX or PPTX → decline, route to `document-skills:docx` or `minimax-skills:pptx-generator`.
- A styled HTML → PDF investment/research report (Heebo, `#2c5282`, finding cards) → decline, route to `report-style`.
- Otherwise: any Hebrew DOCX, Hebrew PPTX, or DOCX→PDF conversion on this machine is in scope.

## 1. DOCX bidi — five levels, plus tables

`WD_ALIGN_PARAGRAPH.RIGHT` is **necessary but not sufficient**. Word renders Hebrew correctly only when BiDi is set at every level below. Miss one and Word silently falls back to LTR for some paragraphs (headings and defaults are the usual casualties). Every paragraph in a Hebrew DOCX must end up right-aligned, no exceptions.

Mandatory checklist for every Hebrew DOCX:

1. **Section** — add `<w:bidi/>` to `sectPr`.
2. **docDefaults `<w:rPrDefault><w:rPr>`** — add `<w:rtl/>` and `<w:lang w:val="he-IL" w:bidi="he-IL"/>`. Without this, unstyled runs fall back to LTR even when the paragraph has `<w:bidi/>`.
3. **docDefaults `<w:pPrDefault><w:pPr>`** — add `<w:bidi/>`. Without this, paragraphs that don't override the default behave LTR.
4. **Normal style** — `<w:pPr>` gets `<w:bidi/>`; `<w:rPr>` gets `<w:rtl/>`.
5. **Every paragraph `<w:pPr>`** — add `<w:bidi/>` and emit **no** `<w:jc>` element at all. Verified empirically via Word COM:

   | XML state | `Format.Alignment` reports | Ribbon shows |
   |---|---|---|
   | `<w:jc w:val="right"/>` + bidi | `0` (wdAlignParagraphLeft) | Align Left |
   | `<w:jc w:val="end"/>` + bidi | `0` (wdAlignParagraphLeft) | Align Left |
   | no `<w:jc>` + bidi | `2` (wdAlignParagraphRight) | Align Right ✓ |

   For RTL paragraphs, the *absence* of `<w:jc>` is what Word treats as natural Hebrew right-alignment, both visually and in the ribbon. Any explicit `<w:jc>` value misleads the ribbon. `python-docx`'s `WD_ALIGN_PARAGRAPH.RIGHT` emits `<w:jc w:val="right"/>` — do not rely on it. Either skip setting alignment entirely, or strip every `<w:jc .../>` from paragraph properties before delivery.
6. **Every run `<w:rPr>`** — add `<w:rtl/>`.
7. **Tables** — add `<w:bidiVisual/>` to `tblPr`. Apply paragraph + run RTL inside every cell.
8. **Mixed Hebrew + English tokens** — keep English in its own run without `<w:rtl/>`; the surrounding Hebrew runs keep `<w:rtl/>`.

Boilerplate (use as-is or adapt, keep the full checklist):

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

def _add(el, tag):
    el.append(OxmlElement(f'w:{tag}'))

def set_rtl_section(section):
    _add(section._sectPr, 'bidi')

def set_rtl_defaults(doc):
    styles = doc.styles.element
    dd = styles.find(qn('w:docDefaults'))
    rPr = dd.find(qn('w:rPrDefault')).find(qn('w:rPr')) or OxmlElement('w:rPr')
    _add(rPr, 'rtl')
    lang = OxmlElement('w:lang'); lang.set(qn('w:val'), 'he-IL'); lang.set(qn('w:bidi'), 'he-IL')
    rPr.append(lang)
    pPr = dd.find(qn('w:pPrDefault')).find(qn('w:pPr')) or OxmlElement('w:pPr')
    _add(pPr, 'bidi')
    for st in styles.findall(qn('w:style')):
        if st.get(qn('w:styleId')) == 'Normal':
            spPr = st.find(qn('w:pPr')) or OxmlElement('w:pPr'); _add(spPr, 'bidi'); st.insert(0, spPr)
            srPr = st.find(qn('w:rPr')) or OxmlElement('w:rPr'); _add(srPr, 'rtl'); st.append(srPr)

def set_rtl_para(p):
    pPr = p._p.get_or_add_pPr()
    _add(pPr, 'bidi')
    # Strip ANY w:jc — Word treats the absence as natural Hebrew right-alignment
    # both visually and in the ribbon (Format.Alignment == 2 = Right).
    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)

def set_rtl_run(r):
    _add(r._element.get_or_add_rPr(), 'rtl')

def set_rtl_table(t):
    _add(t._element.tblPr, 'bidiVisual')
```

### Verification before delivery — always

- Count `<w:jc` elements in `word/document.xml` — must equal **0** for RTL paragraphs.
- Count `<w:bidi/>` in `pPr` — must equal total paragraph count.
- Open the doc via Word COM and confirm `Format.Alignment == 2` for every paragraph. If any return `0`, strip the offending `<w:jc>` and re-verify.
- Word COM `Document.Paragraphs` over a table injects phantom end-of-row entries that report `Alignment=0` and have no `<w:p>` behind them. A naive count false-positives. Compare against the raw `<w:p>` count from `document.xml`, and check cell paragraphs via `Tables(i).Range.Cells` instead.
- Render to PDF via Word COM `SaveAs FileFormat=17` and visually inspect at least 2 pages.
- `Range.ParagraphFormat.ReadingOrder` over Word COM uses `wdReadingOrderRtl = 0`, `wdReadingOrderLtr = 1` — confusingly inverted. Never trust this property alone; always pair it with the XML count and the PDF visual.

## 2. PPTX — Hebrew RTL with python-pptx

Proven on a production Hebrew deck.

1. **`rtl="1"` on `a:pPr` alone is NOT enough.** Punctuation, parens, and em-dashes scramble until `lang="he-IL"` is ALSO set on every `a:rPr`. That attribute drives PowerPoint's bidi resolution. Also set the `a:cs` (complex script) typeface alongside `a:latin`.
2. **Chart category labels with `(Latin)` inside Hebrew render broken** — e.g. `קאלם ((Calm`. RLM, RLE/PDF control chars, and axis `c:txPr` rtl all fail to fix it. The original PowerPoint-authored deck has the same artifact — this is a renderer quirk, not a bug in the generator. **Avoid parentheses in chart text entirely**; don't try to fix the rendering.
3. **Charts**:
   - Delete the value axis via `c:delete val="1"` XML when data labels are shown.
   - `dl.number_format = '0"%"'` with `number_format_is_linked = False` for percent labels.
   - Per-series label color needs manual `c:dLbls` XML injection — python-pptx has no series-level `data_labels` API. The injected element must precede `c:cat`.
4. **Visual QA loop** — PowerPoint COM `Presentation.Export(dir, "PNG", 1280, 720)` inside `Start-Job` with `Wait-Job -Timeout`. Copy the pptx to local temp first — OneDrive paths hang COM (same failure as DOCX→PDF, §3). Then `Read` the PNGs and use PIL crop-zoom for detail checks. Afterwards `Stop-Process -Name POWERPNT -Force` and confirm `Get-Process POWERPNT` is empty; one call is sometimes not enough in the same script, so kill, check, kill again.
5. **Fonts** — Heebo and Assistant may be missing on the machine; check installed fonts. Segoe UI family is the safe modern Hebrew font for PPTX.
Minimal RTL text-box setup:

```python
from pptx.oxml.ns import qn
from pptx.enum.text import PP_ALIGN

def set_rtl_paragraph(paragraph, text, font_size=18):
    paragraph.alignment = PP_ALIGN.RIGHT
    pPr = paragraph._pPr if paragraph._pPr is not None else paragraph.get_or_add_pPr()
    pPr.set('rtl', '1')
    run = paragraph.add_run()
    run.text = text
    run.font.size = font_size
    rPr = run._r.get_or_add_rPr()
    rPr.set('lang', 'he-IL')          # the critical fix — without this, punctuation scrambles
    cs = rPr.find(qn('a:cs'))
    if cs is None:
        cs = rPr.makeelement(qn('a:cs'), {})
        rPr.append(cs)
    cs.set('typeface', 'Segoe UI')
    run.font.name = 'Segoe UI'        # a:latin
```

Example series-label XML injection (must precede `c:cat` inside `c:ser`):

```python
from pptx.oxml.ns import qn
from lxml import etree

dLbls_xml = f'''<c:dLbls xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart">
  <c:spPr/>
  <c:txPr><a:bodyPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>
    <a:lstStyle xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>
    <a:p xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:pPr><a:defRPr solidFill="{{color}}"/></a:pPr>
    </a:p>
  </c:txPr>
  <c:showLegendKey val="0"/><c:showVal val="1"/>
</c:dLbls>'''
ser_element.insert(list(ser_element).index(ser_element.find(qn('c:cat'))), etree.fromstring(dLbls_xml))
```

## 3. DOCX → PDF on Windows

Word COM `ExportAsFixedFormat` **hangs** when called directly in a PowerShell session, and hangs harder on OneDrive paths. Check first whether `docx2pdf`, LibreOffice or `pdftoppm` exist; do not assume.

Working recipe:

1. Copy the `.docx` to a LOCAL temp path (`C:\Temp\...`), not OneDrive.
2. Run the Word COM export inside `Start-Job` with `Wait-Job -Timeout 75`; `Stop-Job` if it exceeds.
3. After the job, `Stop-Process -Name WINWORD -Force` to clear any zombie instance, then copy the PDF back to OneDrive.
4. Verify the result by rasterizing pages with PyMuPDF (`fitz`, installed) and reading the PNGs — `Read` on the PDF fails without `pdftoppm`.

Never embed a Hebrew filename as a string literal in a `.ps1` file: PowerShell 5.1 reads a non-BOM script through the system codepage and silently corrupts it. Either save the script as UTF-8 with BOM, copy the file to an ASCII temp name first, or locate it with `Get-ChildItem -Filter` and pass the resulting object.

Killing Word mid-run leaves a zombie COM server that makes the NEXT export hang too — always confirm `Get-Process WINWORD` count is 0 before retrying.

```powershell
# sketch — adapt paths per task
Copy-Item $oneDrivePath 'C:\Temp\draft.docx' -Force
$job = Start-Job -ScriptBlock {
    $word = New-Object -ComObject Word.Application
    $doc = $word.Documents.Open('C:\Temp\draft.docx')
    $doc.SaveAs([ref]'C:\Temp\draft.pdf', [ref]17)
    $doc.Close(); $word.Quit()
}
Wait-Job $job -Timeout 75
if ($job.State -ne 'Completed') { Stop-Job $job }
Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue
Get-Process WINWORD -ErrorAction SilentlyContinue   # must return nothing before next attempt
Copy-Item 'C:\Temp\draft.pdf' $oneDriveTargetPath -Force
```

```python
# verify page count + text, since Read can't open PDF without pdftoppm
import fitz
doc = fitz.open(r"C:\Temp\draft.pdf")
print(len(doc), "pages")
for page in doc:
    pix = page.get_pixmap(dpi=150)
    pix.save(f"C:\\Temp\\page_{page.number}.png")
    print(page.get_text()[:200])
```

## 4. Delivery checklist

- Modify the existing file in place; at most one timestamped backup, only for risky rewrites — see the modify-don't-create rule (`feedback_modify_dont_create.md`).
- Run the actual generation/conversion end to end and inspect the result yourself before saying "done" — never push verification onto the user — see the test-before-delivery rule (`feedback_test_before_delivery.md`).
- For DOCX: run the §1 verification block (XML counts, Word COM `Format.Alignment`, PDF page render).
- For PPTX: run the §2 visual QA loop (COM PNG export, inspect every slide, especially chart titles for stray parens).
- For DOCX→PDF: confirm page count and extracted text via PyMuPDF, and confirm `Get-Process WINWORD` is clean.
- Never claim a fix without having re-run the verification that would have caught the original failure.
