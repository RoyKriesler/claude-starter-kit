---
name: vba-engineering
description: Build, debug, and refactor Excel VBA macros to house style. Use whenever the user asks for a macro, a Summary sheet builder, a fraud-review categorizer, SLA highlighting, conditional formatting via code, or any Workbook/Worksheet automation. Enforces silent execution (no flicker), robust error handling, Range vs Cells discipline, dynamic last-row detection, and `Option Explicit` everywhere. Triggers on "VBA", "macro", "xlsm", "Sub ", "Workbook_Open", "Excel macro", "automate this sheet", "Summary sheet", "fraud categorizer".
---

# VBA Engineering

House-style VBA for the user's Excel work — fraud-review categorizers, Summary sheets, SLA highlighting, and other workbook automation.

## Non-negotiables

Every macro the user ships must follow these. If asked to write VBA, apply them by default — do not ask permission.

### 1. `Option Explicit` at top of every module

```vba
Option Explicit
```

Forces variable declaration. Catches typos at compile time.

### 2. Silent execution wrapper

Wrap every long-running macro so the screen does not flicker and Excel does not recalc mid-run.

```vba
Public Sub MyMacro()
    Dim prevCalc As XlCalculation
    Dim prevScreen As Boolean
    Dim prevEvents As Boolean

    prevScreen = Application.ScreenUpdating
    prevEvents = Application.EnableEvents
    prevCalc = Application.Calculation

    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.Calculation = xlCalculationManual

    On Error GoTo Cleanup

    ' --- body of macro ---

Cleanup:
    Application.ScreenUpdating = prevScreen
    Application.EnableEvents = prevEvents
    Application.Calculation = prevCalc
    If Err.Number <> 0 Then
        MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
    End If
End Sub
```

Restore previous state in `Cleanup:`, not hardcode to `True` / `xlCalculationAutomatic`. User may have disabled events deliberately.

### 3. `Range` over `Cells` for readable addresses

- `ws.Range("B2:F100")` for fixed ranges.
- `ws.Cells(r, c)` only inside loops where `r` or `c` is a variable.
- Never mix `.Range("B" & i)` when `ws.Cells(i, "B")` is clearer in a loop.

Pick one style per Sub. Do not flip mid-function.

### 4. Dynamic last-row detection

Never hardcode the last row. Excel sheets grow.

```vba
Dim lastRow As Long
lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
```

For tables (ListObject), use the table's range:

```vba
Dim tbl As ListObject
Set tbl = ws.ListObjects("tblOrders")
Dim lastRow As Long
lastRow = tbl.ListRows.Count
```

For sheets where column A may be sparse, anchor on a column known to be fully populated. Document the choice in a comment.

### 5. Qualify every Range and Cells

Never `Range("A1")` bare — always `ws.Range("A1")`. The active sheet changes; the qualified reference does not.

```vba
' Bad
Range("A1").Value = "Date"

' Good
ws.Range("A1").Value = "Date"
```

### 6. Use array reads for >1000 rows

Looping `For i = 2 To lastRow ... ws.Cells(i, 5).Value` is slow. Read once, work in memory, write once.

```vba
Dim arr As Variant
arr = ws.Range("A2:E" & lastRow).Value  ' one trip to Excel

Dim i As Long
For i = 1 To UBound(arr, 1)
    ' arr(i, 1) ... arr(i, 5)
Next i

ws.Range("A2:E" & lastRow).Value = arr   ' one trip back
```

10–100× faster on large fraud-review sheets.

### 7. Error handling, not error suppression

`On Error Resume Next` is allowed only:
- For a single expected-failure line, followed immediately by `On Error GoTo 0`.
- Around a `Set` lookup that may legitimately return Nothing.

Never blanket `On Error Resume Next` at the top of a Sub.

### 8. Module organization

```
Module: modConfig       — constants, named ranges, SLA thresholds
Module: modCore         — main entry points (RebuildSummary, CategorizeReviews)
Module: modHelpers      — small utility Subs/Functions
Module: modSheetEvents  — bridges Workbook_Open to modCore
ThisWorkbook            — Workbook_Open, Workbook_BeforeClose only
Sheet objects           — Worksheet_Change, Worksheet_SelectionChange only
```

Sheet event handlers stay thin — call into `modCore`, don't put logic inline.

## Patterns the user uses repeatedly

### Build a Summary sheet from a transactional sheet

```vba
Public Sub RebuildSummary()
    ' Silent wrapper omitted for brevity — always include it
    Dim wbk As Workbook: Set wbk = ThisWorkbook
    Dim src As Worksheet: Set src = wbk.Worksheets("Reviews")
    Dim dst As Worksheet

    On Error Resume Next
    Set dst = wbk.Worksheets("Summary")
    On Error GoTo 0
    If dst Is Nothing Then
        Set dst = wbk.Worksheets.Add(After:=wbk.Worksheets(wbk.Worksheets.Count))
        dst.Name = "Summary"
    Else
        dst.Cells.Clear
    End If

    ' write headers, then pivot or aggregate from src
End Sub
```

### SLA highlighting

Conditional formatting is preferred over VBA loops where possible — it survives data changes without re-running. Use VBA only when the rule is too complex for CF (e.g., depends on another sheet), or when the rule is time-based and the sheet sits open unattended: a CF formula built on `NOW()` re-evaluates only on recalculation, so an idle sheet shows stale colours until something triggers a recalc.

```vba
' Within the silent wrapper:
Dim cell As Range
For Each cell In ws.Range("F2:F" & lastRow).Cells
    Select Case (Now - cell.Value) * 24    ' hours elapsed
        Case Is > 24:  cell.Interior.Color = RGB(255, 99, 99)
        Case Is > 8:   cell.Interior.Color = RGB(255, 204, 102)
        Case Else:     cell.Interior.Color = xlNone
    End Select
Next cell
```

### Fraud-review categorizer

Use a lookup table (named range or sheet) rather than hardcoding categories in code. Code reads the table; analysts edit the table.

## Anti-patterns

- `Select` / `Activate` — never. Operate on objects directly.
- `Sheet1.Range(...)` using the codename when the user may rename sheets — use `Worksheets("Sheet Name")` and document the dependency.
- Hardcoded sheet/column letters scattered across modules — centralize in `modConfig`.
- `MsgBox` debug prints left in production — use `Debug.Print` for dev, remove before ship.
- Storing secrets/API keys in VBA constants — never. Use environment variables via Shell, or prompt at runtime.

## Testing

Excel has no real unit-test framework. Approximate it, then test across scenarios — a single pass is not enough to ship.

### Unit-test approximation

1. Keep a `TestData` sheet with known inputs.
2. Write a `Public Sub Test_X()` that runs the macro on `TestData` and `Debug.Assert`s a few key cells.
3. Run all `Test_*` Subs from a `RunAllTests` Sub before shipping changes.

### Testing across scenarios

`TestData` covers one fixed input. Any macro driven by user-chosen parameters — time windows, filters, dropdowns — needs scenario coverage on top of that, because the data on screen right now is one slice, not the space of real usage. A clean run against today's snapshot proves nothing about tomorrow's filter; the bug that matters is the one that only shows up on an empty result set or an unusual combination of categories.

General matrix for any parameter-driven macro, whatever the workbook: a narrow window or filter with few rows, a wide one with many, and an empty one with zero matches that must reach an explicit no-data branch. Add one scenario per branch in the code.

For a reset or teardown macro that returns a workbook to a blank starting state: clear data rows below the header on data sheets, delete generated output tabs so they rebuild, and leave parameter cells and lookup lists alone unless told which ones to reset. Test the clear-and-rebuild cycle at least twice in a row.

## References

- Microsoft VBA reference: `docs.microsoft.com/en-us/office/vba/api/overview/excel`
- Chip Pearson's site (still authoritative on advanced patterns): `www.cpearson.com`
- Rubberduck VBA add-in for static analysis: `rubberduckvba.com`
