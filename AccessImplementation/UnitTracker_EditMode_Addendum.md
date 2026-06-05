# UnitTracker Access Spec — Addendum: Edit Mode & Double-Click Editing

**April 2026**

---

## A.1 Overview

The Python app has an **Edit Mode** toggle (Advanced menu, Alt+E). When active, clicking a row in any of the three tab views selects it and allows editing or deletion. The Access reimplementation replicates this using a module-level boolean flag combined with the `DblClick` event on each subform's datasheet.

The design principle: **double-clicking a row always opens the relevant dialog in edit mode**, but only when Edit Mode is enabled. When Edit Mode is off, double-clicking does nothing.

---

## A.2 Global Edit Mode Flag

Add one variable to `modGlobals`:

```vba
Public bEditMode As Boolean  ' False by default
```

Update `InitGlobals()` to initialize it:

```vba
Public Sub InitGlobals()
    bWarningsEnabled = True
    bEditMode = False
End Sub
```

---

## A.3 Toggling Edit Mode from the Menu

The menu item is a checkable toggle (mirrors `actionEdit_Mode` in `main_window.py`). Wire its click handler on `frmMain`:

```vba
Public Sub ToggleEditMode()
    bEditMode = Not bEditMode
    ' Optionally update a menu checkmark or status label here
End Sub
```

If using a ribbon, the toggle button's `getPressed` and `onAction` callbacks read and write `bEditMode`. If using a plain command button or menu item, flip the flag and update a caption or indicator label on `frmMain` so the user can see the current state (e.g., a label reading "Edit Mode: ON" in a status bar area).

---

## A.4 Subform DblClick Events

Each subform is a datasheet bound to a read-only query. The `DblClick` event fires when the user double-clicks anywhere on a row. Place the following event procedures in each subform's code module.

### A.4.1 sfrmFunds — Double-Click Handler

The selected row's `ID` is read from the subform's current record and passed to `frmFundDialog`.

```vba
' In sfrmFunds code module
Private Sub Form_DblClick(Cancel As Integer)
    If Not bEditMode Then Exit Sub
    If Me.RecordsetClone.RecordCount = 0 Then Exit Sub

    ' Pass the selected Fund ID to the dialog via OpenArgs
    Dim fundID As Long
    fundID = Me!ID
    DoCmd.OpenForm "frmFundDialog", , , , acFormEdit, acDialog, CStr(fundID)
    Me.Requery
    Forms!frmMain.sfrmPurchases.Requery
    Forms!frmMain.sfrmAccountValues.Requery
End Sub
```

### A.4.2 sfrmPurchases — Double-Click Handler

```vba
' In sfrmPurchases code module
Private Sub Form_DblClick(Cancel As Integer)
    If Not bEditMode Then Exit Sub
    If Me.RecordsetClone.RecordCount = 0 Then Exit Sub

    ' The purchases query doesn't expose UnitPurchase.ID directly.
    ' Add ID to qryPurchasesByAccount so it is available here.
    Dim purchaseID As Long
    purchaseID = Me!ID
    DoCmd.OpenForm "frmPurchaseDialog", , , , acFormEdit, acDialog, CStr(purchaseID)
    Me.Requery
    Forms!frmMain.sfrmFunds.Requery
    Forms!frmMain.sfrmAccountValues.Requery
End Sub
```

> ⚠ **qryPurchasesByAccount must expose UnitPurchase.ID.** Add `up.ID` as the first column in that query so the subform can read it from `Me!ID`. The column can be hidden in the datasheet (column width = 0) so it doesn't appear to the user.

### A.4.3 sfrmAccountValues — Double-Click Handler

```vba
' In sfrmAccountValues code module
Private Sub Form_DblClick(Cancel As Integer)
    If Not bEditMode Then Exit Sub
    If Me.RecordsetClone.RecordCount = 0 Then Exit Sub

    Dim avID As Long
    avID = Me!ID
    DoCmd.OpenForm "frmAccountValueDialog", , , , acFormEdit, acDialog, CStr(avID)
    Me.Requery
    Forms!frmMain.sfrmFunds.Requery
    Forms!frmMain.sfrmPurchases.Requery
End Sub
```

---

## A.5 Receiving the Record ID in Each Dialog

Each dialog is opened with `OpenArgs` containing the record ID as a string. The dialog's `Form_Open` event reads it to load the correct record.

### A.5.1 frmFundDialog — On Open

```vba
Private Sub Form_Open(Cancel As Integer)
    If Not IsNull(Me.OpenArgs) And Len(Me.OpenArgs) > 0 Then
        ' Edit mode: load existing fund
        Dim fundID As Long
        fundID = CLng(Me.OpenArgs)
        Me.txtFundName     = DLookup("Name",         "Funds", "ID=" & fundID)
        Me.txtInitialUnits = DLookup("InitialUnits", "Funds", "ID=" & fundID)
        Me.Tag = CStr(fundID)   ' stash ID for use in the save handler
        Me.Caption = "Edit Fund"
        Me.chkDeleteFund.Visible = True
    Else
        ' Add mode
        Me.txtInitialUnits = 0
        Me.Caption = "New Fund"
        Me.chkDeleteFund.Visible = False
    End If
    Me.btnOK.Enabled = False
End Sub
```

The OK handler distinguishes add vs. edit by checking whether `Me.Tag` is set:

```vba
Private Sub btnOK_Click()
    If Len(Me.Tag) > 0 Then
        ' Edit or delete
        Dim fundID As Long : fundID = CLng(Me.Tag)
        If Me.chkDeleteFund Then
            CurrentDb.Execute "DELETE FROM Funds WHERE ID=" & fundID, dbFailOnError
        Else
            CurrentDb.Execute _
                "UPDATE Funds SET Name=""" & Me.txtFundName & """" & _
                ", InitialUnits=" & Me.txtInitialUnits & _
                " WHERE ID=" & fundID, dbFailOnError
        End If
    Else
        ' Insert new fund
        CurrentDb.Execute _
            "INSERT INTO Funds (Name, InitialUnits) VALUES (""" & _
            Me.txtFundName & """, " & Me.txtInitialUnits & ")", dbFailOnError
    End If
    Call ProcessPurchases()
    DoCmd.Close acForm, Me.Name
End Sub
```

### A.5.2 frmPurchaseDialog — On Open

```vba
Private Sub Form_Open(Cancel As Integer)
    If Not IsNull(Me.OpenArgs) And Len(Me.OpenArgs) > 0 Then
        ' Edit mode: load existing purchase
        Dim upID As Long : upID = CLng(Me.OpenArgs)
        Dim fundID As Long
        fundID        = DLookup("FundID", "UnitPurchase", "ID=" & upID)
        Dim avID As Long
        avID          = DLookup("DateID", "UnitPurchase", "ID=" & upID)

        Me.cboFund.Value     = fundID
        Me.cboFund.Locked    = True
        Me.txtPurchaseDate   = DLookup("ValueDate", "AccountValue", "ID=" & avID)
        Me.txtAccountValue   = DLookup("Value",     "AccountValue", "ID=" & avID)
        Me.txtAccountValue.Locked = True
        Me.txtPurchaseAmount = DLookup("Amount",    "UnitPurchase", "ID=" & upID)
        Me.Tag = CStr(upID)
        Me.Caption = "Edit Purchase"
        Me.chkDeletePurchase.Visible = True

        ' Store the known AccountValue ID so the date-lookup logic is pre-seeded
        lngKnownAccountValueID = avID
    Else
        ' Add mode (existing behaviour)
        Me.chkDeletePurchase.Visible = False
        Me.Caption = "New Purchase"
        lngKnownAccountValueID = 0
    End If
End Sub
```

The `btnOK_Click` handler already written in the main spec handles the insert path. Extend it with the edit/delete branch:

```vba
' At the top of btnOK_Click, before the existing insert logic:
If Len(Me.Tag) > 0 Then
    Dim upID As Long : upID = CLng(Me.Tag)
    If Me.chkDeletePurchase Then
        CurrentDb.Execute "DELETE FROM UnitPurchase WHERE ID=" & upID, dbFailOnError
        ' If that was the only purchase on its date, the AccountValue orphan
        ' remains — this is intentional; the user deletes it separately if desired.
    Else
        CurrentDb.Execute _
            "UPDATE UnitPurchase SET Amount=" & Me.txtPurchaseAmount & _
            " WHERE ID=" & upID, dbFailOnError
    End If
    Call ProcessPurchases()
    DoCmd.Close acForm, Me.Name
    Forms!frmMain.sfrmFunds.Requery
    Forms!frmMain.sfrmPurchases.Requery
    Forms!frmMain.sfrmAccountValues.Requery
    Exit Sub   ' skip the insert path below
End If
' ... existing insert logic follows unchanged
```

### A.5.3 frmAccountValueDialog — On Open

```vba
Private Sub Form_Open(Cancel As Integer)
    If Not IsNull(Me.OpenArgs) And Len(Me.OpenArgs) > 0 Then
        ' Edit mode
        Dim avID As Long : avID = CLng(Me.OpenArgs)
        Me.txtDate  = DLookup("ValueDate", "AccountValue", "ID=" & avID)
        Me.txtValue = DLookup("Value",     "AccountValue", "ID=" & avID)
        Me.Tag = CStr(avID)
        Me.Caption = "Edit Account Value"
        Me.chkDeleteValue.Visible = True
    Else
        ' Add mode
        Me.Caption = "Add Account Value"
        Me.chkDeleteValue.Visible = False
    End If
    Me.btnOK.Enabled = False
End Sub
```

Add a `chkDeleteValue` checkbox to `frmAccountValueDialog` (hidden by default, shown in edit mode). The OK handler:

```vba
Private Sub btnOK_Click()
    If Len(Me.Tag) > 0 Then
        Dim avID As Long : avID = CLng(Me.Tag)
        If Me.chkDeleteValue Then
            ' Cascade delete will remove any UnitPurchase records on this date
            CurrentDb.Execute "DELETE FROM AccountValue WHERE ID=" & avID, dbFailOnError
        Else
            CurrentDb.Execute _
                "UPDATE AccountValue SET ValueDate=#" & _
                Format(Me.txtDate, "mm/dd/yyyy") & "#" & _
                ", Value=" & Me.txtValue & _
                " WHERE ID=" & avID, dbFailOnError
        End If
    Else
        CurrentDb.Execute _
            "INSERT INTO AccountValue (ValueDate, Value) VALUES (#" & _
            Format(Me.txtDate, "mm/dd/yyyy") & "#, " & Me.txtValue & ")", dbFailOnError
    End If
    Call ProcessPurchases()
    DoCmd.Close acForm, Me.Name
    Forms!frmMain.sfrmFunds.Requery
    Forms!frmMain.sfrmPurchases.Requery
    Forms!frmMain.sfrmAccountValues.Requery
End Sub
```

---

## A.6 Visual Feedback for Edit Mode State

The user needs a clear indication that Edit Mode is active. Two approaches:

**Option A — Status label on frmMain (simplest):** Add a label `lblEditMode` near the bottom of the form. `ToggleEditMode()` updates its caption and color:

```vba
Public Sub ToggleEditMode()
    bEditMode = Not bEditMode
    With Forms!frmMain.lblEditMode
        If bEditMode Then
            .Caption   = "Edit Mode: ON"
            .ForeColor = RGB(180, 0, 0)
        Else
            .Caption   = "Edit Mode: OFF"
            .ForeColor = RGB(100, 100, 100)
        End If
    End With
End Sub
```

**Option B — Ribbon toggle button:** If using a custom ribbon, the toggle button's `getPressed` callback returns `bEditMode`, giving the button a pressed/depressed visual state automatically. Wire `onAction` to call `ToggleEditMode()` and `invalidate` the ribbon control to refresh its pressed state.

---

## A.7 Cursor Change on Hover (Optional Polish)

Access datasheets don't support per-row cursors, but you can set the subform's `MousePointer` property to indicate edit-readiness when Edit Mode is on:

```vba
' Call from ToggleEditMode() after flipping the flag
Private Sub UpdateSubformCursors()
    Dim mp As Integer
    mp = IIf(bEditMode, 1, 0)  ' 1 = arrow+hourglass (pointer), 0 = default
    Forms!frmMain.sfrmFunds.Form.MousePointer = mp
    Forms!frmMain.sfrmPurchases.Form.MousePointer = mp
    Forms!frmMain.sfrmAccountValues.Form.MousePointer = mp
End Sub
```

---

## A.8 Changes to Existing Queries

| Query | Change Required |
|---|---|
| `qryPurchasesByAccount` | Add `up.ID` as the first SELECT column. Hide this column in the sfrmPurchases datasheet (set column width to 0 in the subform's column layout). |
| `qryFundSummary` | `f.ID` is already the first column — no change needed. |
| `qryAccountValues` | `ID` is already the first column — no change needed. |

---

## A.9 Summary of New/Modified Elements

| Element | Change |
|---|---|
| `modGlobals` | Add `bEditMode As Boolean`; initialize in `InitGlobals()` |
| `frmMain` | Add `ToggleEditMode()` sub; add `lblEditMode` status label |
| `sfrmFunds` | Add `Form_DblClick` event |
| `sfrmPurchases` | Add `Form_DblClick` event |
| `sfrmAccountValues` | Add `Form_DblClick` event |
| `frmFundDialog` | Add `Form_Open` to read `OpenArgs`; extend `btnOK_Click` for edit/delete |
| `frmPurchaseDialog` | Add `Form_Open` to read `OpenArgs`; extend `btnOK_Click` for edit/delete |
| `frmAccountValueDialog` | Add `Form_Open` to read `OpenArgs`; add `chkDeleteValue`; extend `btnOK_Click` for edit/delete |
| `qryPurchasesByAccount` | Add `up.ID` to SELECT; hide column in sfrmPurchases |
