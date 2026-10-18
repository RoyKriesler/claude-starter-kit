---
name: reference-docx-to-pdf-windows
description: Reliable DOCX to PDF on Windows when Word COM hangs - local temp copy, Start-Job with timeout, kill zombie WINWORD
metadata:
  type: reference
---
Word COM `ExportAsFixedFormat` can hang when called directly in PowerShell, and hangs harder on OneDrive paths.

1. Copy the .docx to a local temp path (`C:\Temp\...`), not OneDrive.
2. Run the COM export inside `Start-Job`, `Wait-Job -Timeout 75`, `Stop-Job` if it exceeds.
3. `Stop-Process -Name WINWORD -Force`; confirm `Get-Process WINWORD` is empty before any retry — a zombie makes the next export hang.
4. Copy the PDF back. Verify by rasterizing with PyMuPDF (`fitz`) and reading the PNGs.

Same pattern for PowerPoint (`POWERPNT`). Related: [[feedback-hebrew-docs]].
