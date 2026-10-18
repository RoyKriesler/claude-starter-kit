---
name: feedback-modify-dont-create
description: "Fix / update / improve" means edit the existing file in place; never leave v2, _new, _final copies
metadata:
  type: feedback
---
When asked to fix or update a file, edit it in place. No `report_v2.pdf`, `Q_new.xlsx`, `guide_final_FINAL.docx`.

**Why:** version clutter makes it unclear which file is current.

**How to apply:** at most one `<name>.backup_<YYYYMMDD_HHMMSS>.<ext>` for risky operations (VBA rewrite, destructive SQL); offer to delete it after verifying. End multi-edit sessions with "current: <path>, backups to delete: <list or none>".
