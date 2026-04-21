# UnitTracker — MS Access Reimplementation Specification

**April 2026**

---

## 1. Overview

UnitTracker tracks unit ownership in a commingled endowment fund. Multiple sub-accounts ("funds") pool assets into a single account. Each fund receives units when money is contributed. A unit price is derived from the total account value divided by total outstanding units at each valuation date. This document is a complete specification for reimplementing the application in Microsoft Access with VBA.

### 1.1 Core Concept

When a contribution ("purchase") is made to a fund on a given date, the units credited equal the contribution amount divided by the unit price on that date. The unit price on any date equals the total account value divided by the total units entering that date. Unit prices must be recomputed sequentially whenever any historical data changes.

### 1.2 Design Change: Single-Account / Template Model

The Access reimplementation departs from the Python app in one significant architectural decision: each .accdb file holds exactly one endowment. To manage multiple endowments, users create a new database from the Access template for each one.

Consequences of this design throughout the spec:

- The Accounts table is eliminated. Account metadata is stored in a single-row configuration table called AccountInfo.
- All foreign keys previously pointing to Accounts.ID are removed. Funds and AccountValue records implicitly belong to the one account in the file.
- The Open Account / Select Account dialog is eliminated entirely.
- New Account and Delete Account menu items are replaced by a single Edit Account Info action that edits the AccountInfo record.
- The `lngActiveAccountID` global variable is eliminated. VBA uses a helper function `GetAccountID()` that returns the single ID from AccountInfo.
- The Access file itself is the unit of account management. Users open different endowments by opening different .accdb files.

> ⚠ The Access template (.accdt) is a pre-built .accdb saved in template format. It contains all tables, queries, forms, reports, and VBA but no data rows. Users create a new endowment database via File > New, locate UnitTracker.accdt, and save it with the endowment name (e.g., SmithFoundation.accdb).

### 1.3 Technology Stack

| Component | Choice |
|---|---|
| Database engine | Microsoft Access (.accdb) |
| Distribution format | Access Template (.accdt) — one file per endowment |
| Business logic | VBA (Visual Basic for Applications) |
| UI | Access Forms and Subforms |
| Reporting | Access Reports + optional VBA Excel export |
| Backup | VBA FileCopy on application open |

---

## 2. Database Schema

Three tables replace the original four. The Accounts table is eliminated; its data moves to the single-row AccountInfo table. The two remaining foreign-key relationships should be enforced with Referential Integrity and Cascade Delete.

### 2.1 AccountInfo (replaces Accounts)

A single-row configuration table. Always contains exactly one record, created when the user first sets up a new database from the template.

| Field | Access Type | Constraints | Notes |
|---|---|---|---|
| ID | AutoNumber | PK | Always 1 in practice |
| Name | Short Text (100) | Required | Endowment or account name |
| Brokerage | Short Text (100) | Required | |
| AccountNo | Short Text (50) | Required | |

### 2.2 Funds

No AccountID column. All funds in the file belong to the single implicit account.

| Field | Access Type | Constraints | Notes |
|---|---|---|---|
| ID | AutoNumber | PK | |
| Name | Short Text (100) | Required | Must be unique within this file |
| InitialUnits | Number (Double) | Required, >= 0 | First fund added must be > 0 |

### 2.3 AccountValue

No AccountID column. All valuation records belong to the single implicit account.

| Field | Access Type | Constraints | Notes |
|---|---|---|---|
| ID | AutoNumber | PK | |
| ValueDate | Date/Time | Required | Original app stored dates as text yyyy/mm/dd; use proper Date/Time here |
| TodaysValue | Currency | Required, > 0 | Total account value on this date |
| UnitPrice | Number (Double) | Computed by VBA | Written by ProcessPurchases(); not user-editable |

> ⚠ UnitPrice is new in the Access version. The Python app recomputed it on every load; storing it makes queries and reports practical.

### 2.4 UnitPurchase

| Field | Access Type | Constraints | Notes |
|---|---|---|---|
| ID | AutoNumber | PK | |
| FundID | Number (Long) | FK -> Funds | Cascade delete; fund cannot be changed after creation |
| Amount | Currency | Required, > 0 | Dollar amount contributed |
| DateID | Number (Long) | FK -> AccountValue | Cascade delete |
| UnitsPurchased | Number (Double) | Computed by VBA | Written by ProcessPurchases(); not user-editable |

> ⚠ UnitsPurchased is new in the Access version. The Python app computed this on the fly; storing it allows straightforward queries and reports.

### 2.5 Relationships

Set these two relationships in the Access Relationships window, both with Referential Integrity enforced and Cascade Delete enabled:

| Relationship | Cascade Delete Effect |
|---|---|
| Funds (ID) -> UnitPurchase (FundID) | Deleting a fund deletes all its purchases |
| AccountValue (ID) -> UnitPurchase (DateID) | Deleting an account value deletes purchases on that date |

---

## 3. Global VBA State

Place the following in a standard module named `modGlobals`. `lngActiveAccountID` is eliminated; `GetAccountID()` reads from AccountInfo instead.

```vba
' modGlobals

Public bWarningsEnabled As Boolean  ' True by default

Public Sub InitGlobals()
    bWarningsEnabled = True
End Sub

' Returns the ID of the single account in this file.
' Returns 0 if AccountInfo has not been populated yet.
Public Function GetAccountID() As Long
    Dim v As Variant
    v = DLookup("ID", "AccountInfo")
    GetAccountID = IIf(IsNull(v), 0, CLng(v))
End Function
```

---

## 4. Core Calculation — modCalc

`ProcessPurchases()` replicates the Python `processPurchases()` method. Because there is exactly one account per file, the function takes no argument. It must be called after every data mutation: adding/editing/deleting a fund, account value, or purchase.

### 4.1 Algorithm

Walk AccountValue records in ascending ValueDate order. At each date:

- Compute `unit_price = account_value / total_units_entering_this_date`
- For each UnitPurchase on this date: `units_purchased = amount / unit_price`
- Add `units_purchased` to the running fund total
- Write `UnitPrice` back to AccountValue and `UnitsPurchased` back to UnitPurchase

The calculation only runs if the sum of `InitialUnits` across all funds is greater than zero.

### 4.2 VBA Implementation

```vba
' modCalc

Public Sub ProcessPurchases()

    Dim db As DAO.Database
    Dim rsAV As DAO.Recordset
    Dim rsUP As DAO.Recordset
    Dim rsFunds As DAO.Recordset
    Dim totalInitial As Double
    Dim unitTotals() As Double
    Dim fundIDs() As Long
    Dim fundCount As Integer
    Dim i As Integer
    Dim totalUnits As Double
    Dim unitPrice As Double

    Set db = CurrentDb()

    ' 1. Load all funds and initial units
    Set rsFunds = db.OpenRecordset("SELECT ID, InitialUnits FROM Funds ORDER BY ID")
    fundCount = 0 : totalInitial = 0
    Do While Not rsFunds.EOF
        fundCount = fundCount + 1
        ReDim Preserve fundIDs(fundCount - 1)
        ReDim Preserve unitTotals(fundCount - 1)
        fundIDs(fundCount - 1) = rsFunds!ID
        unitTotals(fundCount - 1) = rsFunds!InitialUnits
        totalInitial = totalInitial + rsFunds!InitialUnits
        rsFunds.MoveNext
    Loop
    rsFunds.Close

    ' 2. Guard: nothing to compute if all initial units are zero
    If totalInitial = 0 Or fundCount = 0 Then Exit Sub

    ' 3. Walk AccountValue rows in ascending date order
    Set rsAV = db.OpenRecordset("SELECT ID, TodaysValue FROM AccountValue ORDER BY ValueDate")
    Do While Not rsAV.EOF
        totalUnits = 0
        For i = 0 To fundCount - 1 : totalUnits = totalUnits + unitTotals(i) : Next i
        unitPrice = rsAV!TodaysValue / totalUnits

        db.Execute "UPDATE AccountValue SET UnitPrice=" & unitPrice & " WHERE ID=" & rsAV!ID, dbFailOnError

        Set rsUP = db.OpenRecordset("SELECT ID, FundID, Amount FROM UnitPurchase WHERE DateID=" & rsAV!ID)
        Do While Not rsUP.EOF
            Dim unitsBought As Double
            unitsBought = rsUP!Amount / unitPrice
            db.Execute "UPDATE UnitPurchase SET UnitsPurchased=" & unitsBought & " WHERE ID=" & rsUP!ID, dbFailOnError
            For i = 0 To fundCount - 1
                If fundIDs(i) = rsUP!FundID Then unitTotals(i) = unitTotals(i) + unitsBought : Exit For
            Next i
            rsUP.MoveNext
        Loop
        rsUP.Close

        rsAV.MoveNext
    Loop
    rsAV.Close

End Sub
```

> ⚠ Call `ProcessPurchases()` from the AfterUpdate/AfterInsert/AfterDelete events of the fund, account value, and purchase forms whenever any data changes.

---

## 5. Saved Queries

Because there is one account per file, no `WHERE AccountID = ?` filter is needed in any query.

### 5.1 qryFundSummary

Used by the Funds subform. Returns one row per fund with ending units and percentage of total.

```sql
SELECT
    f.ID,
    f.Name,
    f.InitialUnits,
    f.InitialUnits + Nz(SUM(up.UnitsPurchased), 0)  AS EndUnits,
    (f.InitialUnits + Nz(SUM(up.UnitsPurchased), 0))
        / (SELECT SUM(f2.InitialUnits) + Nz(SUM(up2.UnitsPurchased), 0)
           FROM Funds f2 LEFT JOIN UnitPurchase up2 ON up2.FundID = f2.ID)
        * 100  AS PctOfTotal
FROM Funds f
LEFT JOIN UnitPurchase up ON up.FundID = f.ID
GROUP BY f.ID, f.Name, f.InitialUnits
```

### 5.2 qryPurchasesByAccount

Used by the Purchases subform.

```sql
SELECT
    av.ValueDate,
    f.Name    AS FundName,
    up.Amount,
    up.UnitsPurchased
FROM UnitPurchase up
INNER JOIN AccountValue av ON av.ID = up.DateID
INNER JOIN Funds f        ON f.ID  = up.FundID
ORDER BY av.ValueDate, f.Name
```

### 5.3 qryAccountValues

Used by the Account Values subform.

```sql
SELECT ID, ValueDate, TodaysValue, UnitPrice
FROM AccountValue
ORDER BY ValueDate
```

---

## 6. Menu Structure

The Python app (main_window.py) uses a menu bar with three menus: Accounts, Funds, and Advanced. The Access version replicates this structure using a custom ribbon or Access menu bar. The items below are derived directly from main_window.py, with modifications for the single-account design.

### 6.1 Accounts Menu

| Item | Notes |
|---|---|
| Edit Account Info | Opens frmAccountInfoDialog to edit the single AccountInfo record. Replaces New Account, Open Account, and Delete Account from the Python app. |
| Export to Excel | Calls `modExport.ExportToExcel()`. Disabled until AccountInfo has a record (mirrors Python: disabled until account is loaded). |

### 6.2 Funds Menu

| Item | Notes |
|---|---|
| New Fund | Opens frmFundDialog in add mode. Disabled until AccountInfo is set up. |
| Purchase Fund | Opens frmPurchaseDialog in add mode. |
| Hide Empty (checkable toggle) | Filters sfrmFunds to EndUnits > 0 when checked. Mirrors Python actionHide_Empty. |

### 6.3 Advanced Menu

| Item | Notes |
|---|---|
| Edit Mode (Alt+E, checkable toggle) | Enables row selection in the three subforms for editing/deleting. Mirrors Python actionEdit_Mode. |
| No Warnings (Alt+W, checkable toggle) | Sets `bWarningsEnabled = False`. Suppresses date and InitialUnits warnings. Mirrors Python actionNo_Warnings. |
| Add Account Value (Alt+V) | Opens frmAccountValueDialog to add a standalone valuation. Mirrors Python actionAdd_Account_Value. |
| Backup Now (Alt+B) | Calls `modBackup.BackupDB()` immediately. Mirrors Python actionBackup_Now. |

---

## 7. Forms

### 7.1 frmMain

The main application window. Opens automatically on startup via an AutoExec macro. Layout mirrors the Python main_window.ui: an account summary panel on the left (~25% width) and a tab control on the right (~75% width).

#### Layout (from main_window.py)

The Python window uses a framed panel on the left containing a bold "Account Description" label followed by account name, brokerage, and account number in a vertical stack. Replicate this in Access using a Rectangle control with raised or sunken appearance containing four Label controls. The Tab Control occupies the remainder of the form with three pages: Funds, Purchases, Account Values.

#### Controls

| Control Name | Type / Purpose |
|---|---|
| lblAccountDescription | Label, bold, centered — static caption "Account Description" |
| lblAccountName | Label — displays Name from AccountInfo |
| lblBrokerage | Label — displays Brokerage from AccountInfo |
| lblAccountNo | Label — displays AccountNo from AccountInfo |
| tabMain | Tab Control with 3 pages: Funds │ Purchases │ Account Values |
| sfrmFunds | Subform on Funds tab, datasheet view, bound to qryFundSummary |
| sfrmPurchases | Subform on Purchases tab, datasheet view, bound to qryPurchasesByAccount |
| sfrmAccountValues | Subform on Account Values tab, datasheet view, bound to qryAccountValues |

#### On Open Event

Runs backup, initializes globals, and checks whether AccountInfo is populated. If not (fresh template), forces the user to enter account info before proceeding.

```vba
Private Sub Form_Open(Cancel As Integer)
    Call modBackup.BackupDB()
    Call InitGlobals()
    If GetAccountID() = 0 Then
        MsgBox "Welcome! Please enter your account information to get started.", _
               vbInformation, "UnitTracker"
        DoCmd.OpenForm "frmAccountInfoDialog", , , , acFormAdd, acDialog
        If GetAccountID() = 0 Then   ' user cancelled without saving
            Cancel = True : Exit Sub
        End If
    End If
    Call RefreshSummary()
    Me.sfrmFunds.Requery
    Me.sfrmPurchases.Requery
    Me.sfrmAccountValues.Requery
End Sub

Public Sub RefreshSummary()
    Me.lblAccountName.Caption = Nz(DLookup("Name",      "AccountInfo"), "")
    Me.lblBrokerage.Caption   = Nz(DLookup("Brokerage", "AccountInfo"), "")
    Me.lblAccountNo.Caption   = Nz(DLookup("AccountNo", "AccountInfo"), "")
End Sub
```

### 7.2 frmAccountInfoDialog (replaces frmAccountDialog)

Edits the single AccountInfo record. Opened on first launch (add mode) and via Accounts > Edit Account Info (edit mode). No duplicate-name check is needed since only one record exists per file.

| Control | Behavior |
|---|---|
| txtName | Required. OnChange: enable/disable Save button. |
| txtBrokerage | Required. OnChange: enable/disable Save button. |
| txtAccountNo | Required. OnChange: enable/disable Save button. |
| btnSave | Disabled until all three fields are non-empty. On click: INSERT or UPDATE AccountInfo; call `RefreshSummary()` on frmMain. |

### 7.3 frmFundDialog

Add or Edit a fund. Most of the application's validation lives here.

#### Controls

| Control | Behavior |
|---|---|
| txtFundName | Required. OnChange: duplicate check, show/hide warning label, enable/disable OK. |
| txtInitialUnits | Numeric >= 0, 3 decimal places. OnChange: enable/disable OK. |
| lblDuplicateFundWarning | Visible when a fund with this name already exists. |
| chkDeleteFund | Visible in edit mode only. When checked, disables other fields. |
| btnOK | Disabled until name is filled, unique, and InitialUnits has a value. |

#### Validation Rules (OK Handler)

- First fund in the file: InitialUnits must be > 0. Check `DCount("*","Funds") = 0`.
- Changing InitialUnits when purchases exist (edit mode): show warning — proceeding will recalculate all historical unit prices.
- Adding a fund with InitialUnits > 0 when purchases already exist: same warning.
- Duplicate fund name: block save with DCount check on Funds.Name.

#### Warning Text

Edit mode: "You have changed the initial units value in an existing fund. If you proceed, unit values for all funds will change starting with the initial purchases."

Add mode with existing purchases: "You have entered an initial units value in an account that has existing fund purchases. If you proceed, unit values for all funds will change starting with the initial purchases."

#### On Save

INSERT or UPDATE Funds, call `ProcessPurchases()`, requery all three subforms on frmMain.

### 7.4 frmPurchaseDialog

The most complex dialog. Handles adding or editing a UnitPurchase, and conditionally creates a new AccountValue record when the chosen date has no existing valuation.

#### Controls

| Control | Behavior |
|---|---|
| cboFund | Combo box populated from Funds table. Locked in edit mode. |
| txtPurchaseDate | Date picker. AfterUpdate triggers date-lookup logic. |
| txtAccountValue | Currency > 0. Locked and auto-filled when the date already has an AccountValue record; editable otherwise. |
| txtPurchaseAmount | Currency > 0. Required. |
| chkDeletePurchase | Visible in edit mode only. |
| btnOK | Disabled until txtPurchaseAmount > 0 AND (txtAccountValue > 0 OR a known AccountValue exists for the date). |

#### Date Lookup Logic (txtPurchaseDate AfterUpdate)

```vba
Private lngKnownAccountValueID As Long  ' 0 = new date, non-zero = existing record

Private Sub txtPurchaseDate_AfterUpdate()
    Dim dateVal As Date : dateVal = Me.txtPurchaseDate

    ' Warn if date is older than the latest existing AccountValue
    If bWarningsEnabled Then
        Dim latestDate As Variant : latestDate = DMax("ValueDate", "AccountValue")
        If Not IsNull(latestDate) And dateVal < CDate(latestDate) Then
            Dim resp As Integer
            resp = MsgBox("The selected date is older than the latest existing date (" & _
                   Format(latestDate, "yyyy/mm/dd") & _
                   "). This may affect account history. Continue?", _
                   vbYesNo + vbDefaultButton2, "Date Warning")
            If resp = vbNo Then Me.txtPurchaseDate = Date : Exit Sub
        End If
    End If

    ' Check for an existing AccountValue on this date
    Dim avID As Variant
    avID = DLookup("ID", "AccountValue", _
           "ValueDate=#" & Format(dateVal, "mm/dd/yyyy") & "#")

    If Not IsNull(avID) Then
        lngKnownAccountValueID = CLng(avID)
        Me.txtAccountValue = DLookup("TodaysValue", "AccountValue", "ID=" & avID)
        Me.txtAccountValue.Locked = True
    Else
        lngKnownAccountValueID = 0
        Me.txtAccountValue = Null
        Me.txtAccountValue.Locked = False
    End If

    Call ValidateForm()
End Sub
```

#### Save Logic (btnOK Click)

- Known date (`lngKnownAccountValueID > 0`): insert UnitPurchase with `DateID = lngKnownAccountValueID`.
- New date (`lngKnownAccountValueID = 0`): insert AccountValue first, capture its new ID, then insert UnitPurchase using that ID.

After saving, call `ProcessPurchases()` and requery all three subforms.

```vba
Private Sub btnOK_Click()
    Dim db As DAO.Database : Set db = CurrentDb()
    Dim dateID As Long

    If lngKnownAccountValueID = 0 Then
        db.Execute _
            "INSERT INTO AccountValue (ValueDate, TodaysValue) VALUES (" & _
            "#" & Format(Me.txtPurchaseDate, "mm/dd/yyyy") & "#, " & _
            Me.txtAccountValue & ")", dbFailOnError
        dateID = db.OpenRecordset("SELECT @@IDENTITY")(0)
    Else
        dateID = lngKnownAccountValueID
    End If

    db.Execute _
        "INSERT INTO UnitPurchase (FundID, Amount, DateID) VALUES (" & _
        Me.cboFund & ", " & Me.txtPurchaseAmount & ", " & dateID & ")", dbFailOnError

    Call ProcessPurchases()
    DoCmd.Close acForm, Me.Name
    Forms!frmMain.sfrmFunds.Requery
    Forms!frmMain.sfrmPurchases.Requery
    Forms!frmMain.sfrmAccountValues.Requery
End Sub
```

### 7.5 frmAccountValueDialog

Simple dialog to add or edit a standalone AccountValue record without an associated purchase. Accessed via Advanced > Add Account Value (Alt+V).

| Control | Behavior |
|---|---|
| txtDate | Date picker. Required. |
| txtValue | Currency > 0. Required. |
| btnOK | Disabled until both fields valid. On click: INSERT or UPDATE AccountValue, call `ProcessPurchases()`, requery subforms. |

---

## 8. VBA Modules

### 8.1 modBackup

Called automatically on frmMain Open and by Advanced > Backup Now (Alt+B). Copies the current .accdb to a /backup subfolder with a timestamp, mirroring the Python `backupDB()` method.

```vba
' modBackup

Public Sub BackupDB()
    Dim dbPath As String : dbPath = CurrentDb().Name
    Dim backupDir As String
    backupDir = Left(dbPath, InStrRev(dbPath, "\")) & "backup"
    If Dir(backupDir, vbDirectory) = "" Then MkDir backupDir

    Dim baseName As String
    baseName = Mid(dbPath, InStrRev(dbPath, "\") + 1)
    baseName = Left(baseName, Len(baseName) - 6)  ' strip .accdb

    Dim backupFile As String
    backupFile = backupDir & "\" & baseName & "_" & Format(Now(), "yyyy-mm-dd-hh-nn") & ".accdb"

    On Error Resume Next
    FileCopy dbPath, backupFile
    If Err.Number <> 0 Then MsgBox "Backup failed: " & Err.Description, vbExclamation, "Backup"
    On Error GoTo 0
End Sub
```

### 8.2 modExport

Exports data to an Excel workbook with three sheets, replicating the Python `exportXLSX()` method. Requires a reference to the Microsoft Excel Object Library (Tools > References in the VBA editor).

| Sheet | Contents |
|---|---|
| Funds | Fund name, Initial Units, Ending Units, % of Total. Bold totals row at bottom. |
| Purchases | ValueDate, Fund Name, Amount, UnitsPurchased — from qryPurchasesByAccount. |
| Account Values | ValueDate, TodaysValue — from qryAccountValues. |

The save routine must handle the case where the target file is already open in Excel, prompting the user to close it and retry or choose a new filename. This mirrors the Python `save_workbook_with_retry()` method.

### 8.3 modValidation

Helper functions used across forms:

```vba
' modValidation

Public Function FundNameExists(name As String, excludeID As Long) As Boolean
    FundNameExists = DCount("*", "Funds", _
        "Name=""" & name & """ AND ID<>" & excludeID) > 0
End Function

Public Function HasPurchases() As Boolean
    HasPurchases = DCount("*", "UnitPurchase") > 0
End Function

Public Function IsFirstFund() As Boolean
    IsFirstFund = DCount("*", "Funds") = 0
End Function
```

---

## 9. Validation Rules Summary

All rules are enforced in VBA, not at the table level:

| Rule | Where Enforced | Mirrors Python |
|---|---|---|
| All AccountInfo fields required | frmAccountInfoDialog btnSave | AddAccountDialog.onTextChanged |
| Fund name must be unique within file | frmFundDialog OnChange + OKHandler | AddFundDialog.fundNameExists |
| First fund must have InitialUnits > 0 | frmFundDialog OKHandler | AddFundDialog.OKHandler first_fund check |
| Changing InitialUnits with existing purchases: warn | frmFundDialog OKHandler | AddFundDialog.OKHandler |
| Purchase date older than latest: warn if bWarningsEnabled | frmPurchaseDialog AfterUpdate | UnitPurchaseDialog.checkDate |
| Purchase amount must be > 0 | frmPurchaseDialog ValidateForm | UnitPurchaseDialog.validateForm |
| Account value must be > 0 | frmPurchaseDialog ValidateForm | UnitPurchaseDialog.validateForm |
| ProcessPurchases not run if all InitialUnits = 0 | modCalc guard | Account.initialUnitValuesIsZero |

---

## 10. Creating the Access Template

Once the .accdb is fully built and tested with sample data, produce the distributable template:

1. Delete all data rows from AccountInfo, Funds, AccountValue, and UnitPurchase.
2. Compact and Repair the database (Database Tools > Compact and Repair).
3. File > Save As > Access Template (.accdt). Name it `UnitTracker.accdt`.
4. Distribute `UnitTracker.accdt` to users. They create a new endowment database via File > New, locate the template, and save it under the endowment name (e.g., SmithFoundation.accdb).

> ⚠ Do not save any runtime VBA state as part of the template. All state is initialized in frmMain On Open via `InitGlobals()`. The AutoExec macro should do nothing more than open frmMain.

---

## 11. Recommended Build Order

| Step | Task |
|---|---|
| 1 | Create four tables (AccountInfo, Funds, AccountValue, UnitPurchase) with correct field types and indexes |
| 2 | Set up two Relationships with Referential Integrity and Cascade Delete |
| 3 | Write modGlobals (with `GetAccountID()`) and modCalc; test `ProcessPurchases()` with sample data in the VBA Immediate Window |
| 4 | Write modValidation helper functions |
| 5 | Build frmAccountInfoDialog (simplest form; no duplicate check needed) |
| 6 | Build frmMain shell with summary labels and empty tab control; wire On Open event |
| 7 | Build the three subforms (sfrmFunds, sfrmPurchases, sfrmAccountValues) as datasheets bound to saved queries |
| 8 | Wire subforms into frmMain tab control; verify data displays correctly |
| 9 | Build frmFundDialog (introduces InitialUnits warning pattern) |
| 10 | Build frmAccountValueDialog |
| 11 | Build frmPurchaseDialog (most complex — two-table conditional save + date lookup) |
| 12 | Write modBackup; hook into frmMain On Open and Backup Now menu item |
| 13 | Write modExport; hook into Export to Excel menu item |
| 14 | Add custom ribbon XML with Accounts / Funds / Advanced menu structure and keyboard shortcuts |
| 15 | End-to-end test with sample data (see Section 12) |
| 16 | Delete sample data, compact, and save as .accdt template |

---

## 12. Testing Checklist

**First-launch experience:**
- Open fresh template — frmAccountInfoDialog appears automatically
- Cancel without saving — application does not open
- Save account info — summary labels on frmMain populate correctly

**Fund management:**
- Add first fund with InitialUnits = 0 — rejected with message
- Add first fund with InitialUnits > 0 — accepted
- Add second fund with InitialUnits = 0 — allowed
- Add fund with duplicate name — rejected with inline warning label
- Edit fund InitialUnits when purchases exist — warning dialog; confirming triggers full recalculation of all UnitPrice and UnitsPurchased values
- Delete fund — all its UnitPurchase records deleted (cascade)

**Purchases and account values:**
- Add purchase on a new date — account value field is editable; new AccountValue record created on save
- Add purchase on an existing date — account value field auto-fills and locks
- Verify UnitPrice in AccountValue after purchase is added
- Verify UnitsPurchased in UnitPurchase after purchase is added
- Add purchase with date older than latest — warning appears when `bWarningsEnabled = True`
- Add purchase with date older than latest when No Warnings is checked — warning suppressed
- Add standalone account value via Advanced > Add Account Value

**Display and export:**
- Hide Empty toggle — funds with EndUnits = 0 disappear from Funds tab
- Export to Excel — three sheets with correct data and column widths
- Export with target file open in Excel — retry/save-as dialog appears
- Backup Now — timestamped .accdb appears in /backup subfolder
- Backup on open — same, triggered automatically on frmMain load
- Edit Mode toggle — subform rows become selectable for editing/deleting
