# UnitTracker — Import Feature Specification

**April 2026**

---

## 1. Overview

Users migrating from prior solutions (spreadsheets, the Python app, etc.) need a way to bulk-load historical data into a fresh `.accdb`. This feature accepts a specifically formatted Excel workbook and imports it in a single operation, invoking `ProcessPurchases()` once at the end.

The import is **destructive and all-or-nothing**: it requires a database in which AccountInfo has not yet been populated (i.e., a fresh template). If AccountInfo already has a record, the import is blocked with an error message.

---

## 2. Excel Workbook Format

The workbook must be `.xlsx`. It supports two layout modes, selected by the user when they initiate the import (see Section 4).

### 2.1 Mode A — Separate Account Values Sheet (4 sheets)

| Sheet (tab name, exact) | Contents |
|---|---|
| `AccountInfo` | Account metadata (one data row) |
| `Funds` | Fund names and initial units |
| `Purchases` | Purchase transactions — date and amount only |
| `AccountValues` | Account total values by date |

### 2.2 Mode B — Account Value Per Purchase (3 sheets)

Same as Mode A but the `AccountValues` sheet is **omitted**. Instead, the `Purchases` sheet includes an `AccountValue` column. Each purchase row carries the total account value on that date. Where multiple purchases share a date, every row for that date must have the same `AccountValue`; the importer uses the first non-blank value found for that date and warns if they differ.

---

## 3. Sheet Definitions

Column headers must appear exactly as shown (case-insensitive). Column order does not matter. Extra columns are ignored.

### 3.1 AccountInfo Sheet

One header row, one data row.

| Column | Maps To | Required | Notes |
|---|---|---|---|
| `Name` | `AccountInfo.Name` | Yes | |
| `Brokerage` | `AccountInfo.Brokerage` | Yes | |
| `AccountNo` | `AccountInfo.AccountNo` | Yes | |

### 3.2 Funds Sheet

One header row, one row per fund.

| Column | Maps To | Required | Notes |
|---|---|---|---|
| `FundName` | `Funds.Name` | Yes | Must be unique within the sheet |
| `InitialUnits` | `Funds.InitialUnits` | Yes | Numeric ≥ 0; at least one fund must be > 0 |

Row order determines insertion order. Column order does not matter.

### 3.3 Purchases Sheet

One header row, one row per purchase.

| Column | Maps To | Required | Notes |
|---|---|---|---|
| `FundName` | Lookup → `Funds.ID` | Yes | Must match a name in the Funds sheet |
| `Date` | `UnitPurchase.DateID` via `AccountValue.ValueDate` | Yes | Any Excel date format acceptable |
| `Amount` | `UnitPurchase.Amount` | Yes | Currency > 0 |
| `AccountValue` | `AccountValue.TodaysValue` | Mode B only | Currency > 0; omit column in Mode A |

### 3.4 AccountValues Sheet (Mode A only)

One header row, one row per valuation date.

| Column | Maps To | Required | Notes |
|---|---|---|---|
| `Date` | `AccountValue.ValueDate` | Yes | Any Excel date format acceptable |
| `AccountValue` | `AccountValue.TodaysValue` | Yes | Currency > 0 |

Each date must be unique within this sheet. The importer merges this with dates implied by the Purchases sheet: if a purchase date has no corresponding row here, the import fails with a clear error listing the missing dates.

---

## 4. Menu Integration

Add one item to the **Accounts** menu:

| Item | Notes |
|---|---|
| Import from Excel… | Disabled until AccountInfo is unpopulated (fresh template only). Opens `frmImportDialog`. |

> If AccountInfo already has a record, the menu item is greyed out. Attempting to import into a populated database is not supported; users should start from a fresh template.

---

## 5. frmImportDialog

A simple modal dialog. No subforms or live previews — validation happens after the user clicks Import.

### 5.1 Controls

| Control | Type | Behavior |
|---|---|---|
| `txtFilePath` | Text box, read-only | Displays the chosen file path |
| `btnBrowse` | Button | Opens a `FileDialog` to select an `.xlsx` file; writes path to `txtFilePath` |
| `fraMode` | Option group | Two radio buttons: "Separate AccountValues sheet (4 sheets)" / "AccountValue column in Purchases (3 sheets)" |
| `btnImport` | Button | Disabled until `txtFilePath` is non-empty. Runs the import. |
| `btnCancel` | Button | Closes the dialog without action |
| `lblStatus` | Label | Displays progress messages and errors during/after import |

### 5.2 AfterUpdate / Change Events

- `txtFilePath` AfterUpdate: enable/disable `btnImport`.

---

## 6. VBA Implementation — modImport

All import logic lives in a new standard module `modImport`. The dialog's `btnImport_Click` calls `ImportFromExcel(filePath As String, mode As Integer)` where `mode` is 1 (Mode A) or 2 (Mode B).

### 6.1 High-Level Procedure

```vba
Public Sub ImportFromExcel(filePath As String, mode As Integer)
    ' 1. Open the workbook read-only via Excel automation
    ' 2. Validate all sheets and data (Section 6.2)
    '    — on any error: close workbook, report errors, Exit Sub
    ' 3. Begin import inside a transaction
    '    a. INSERT AccountInfo row
    '    b. INSERT Funds rows; capture Name→ID map
    '    c. INSERT AccountValue rows (Mode A: from AccountValues sheet;
    '       Mode B: one row per distinct date found in Purchases sheet)
    '       Capture Date→AccountValue.ID map
    '    d. INSERT UnitPurchase rows using the two maps
    ' 4. Commit transaction
    ' 5. Close workbook
    ' 6. Call ProcessPurchases()
    ' 7. Refresh all subforms and summary labels on frmMain
End Sub
```

Use `DBEngine.BeginTrans` / `DBEngine.CommitTrans` / `DBEngine.Rollback` so that a mid-import failure leaves the database empty.

### 6.2 Validation Pass (before any INSERTs)

Collect all errors into a string array; report them all at once rather than stopping at the first failure.

| Check | Error Message Pattern |
|---|---|
| Required sheets present | "Sheet 'AccountValues' not found" |
| Required columns present in each sheet | "Column 'InitialUnits' missing from Funds sheet" |
| AccountInfo has exactly one data row | "AccountInfo sheet must have exactly one data row" |
| No duplicate FundName within Funds sheet | "Duplicate fund name: 'Smith Fund'" |
| At least one fund has InitialUnits > 0 | "At least one fund must have InitialUnits > 0" |
| All FundName values in Purchases exist in Funds sheet | "Unknown fund name in Purchases row 5: 'Jones'" |
| All Amount values > 0 | "Amount must be > 0 in Purchases row 8" |
| All AccountValue values > 0 | "AccountValue must be > 0 in Purchases row 12" (Mode B) |
| Mode A: every purchase date has a matching AccountValues row | "No AccountValue found for date 2023/03/15 (referenced in Purchases rows 4, 7)" |
| Mode B: rows sharing a date have consistent AccountValue | "Inconsistent AccountValue for date 2023/03/15 in Purchases rows 4 and 7" |
| No duplicate dates in AccountValues sheet | "Duplicate date in AccountValues sheet: 2023/03/15" (Mode A) |

If any errors are found, display them in `lblStatus` (newline-separated) and abort.

### 6.3 Excel Automation Snippet (reference)

```vba
Dim xlApp As Object
Dim xlWb  As Object
Set xlApp = CreateObject("Excel.Application")
xlApp.Visible = False
Set xlWb = xlApp.Workbooks.Open(filePath, ReadOnly:=True)

' Access a sheet by name:
Dim ws As Object
Set ws = xlWb.Sheets("Funds")

' Read a cell value (row r, column c):
Dim v As Variant
v = ws.Cells(r, c).Value

' Always clean up:
xlWb.Close SaveChanges:=False
xlApp.Quit
Set xlWb = Nothing : Set xlApp = Nothing
```

Column positions should be determined dynamically by reading the header row and building a `colIndex(columnName)` lookup, so column order in the workbook does not matter.

---

## 7. Template Workbook

Distribute a file `UnitTracker_Import_Template.xlsx` alongside `UnitTracker.accdt`. It contains the four sheets with header rows only, sample rows in a light grey font, and a `Notes` column on each sheet (ignored by the importer) explaining each field. A fifth sheet named `Instructions` describes both modes and the rules from Section 3.

---

## 8. Error Reporting

- Validation errors (Section 6.2): displayed in `lblStatus` as a bulleted list. `btnImport` remains enabled so the user can fix the file and retry.
- Transaction/runtime errors: caught in an `On Error` handler; `DBEngine.Rollback` called; error description shown in `lblStatus`.
- Partial success is not possible: either all rows import or none do.

---

## 9. Build Checklist

| Step | Task |
|---|---|
| 1 | Create `UnitTracker_Import_Template.xlsx` with correct headers and Instructions sheet |
| 2 | Write `modImport`: column-header resolver, validation pass, transaction-wrapped insert logic |
| 3 | Build `frmImportDialog` with controls from Section 5 |
| 4 | Wire Accounts menu item; disable logic when AccountInfo is populated |
| 5 | Test Mode A with a complete 4-sheet workbook |
| 6 | Test Mode B with a 3-sheet workbook |
| 7 | Test all validation error cases from Section 6.2 |
| 8 | Test rollback: introduce a bad row mid-sheet; confirm database remains empty |
| 9 | Verify `ProcessPurchases()` produces correct UnitPrice and UnitsPurchased values after import |
