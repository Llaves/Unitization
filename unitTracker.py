# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#


import sys
import os
import shutil
import datetime as date
from PyQt5 import QtCore, QtGui, QtWidgets
from main_window import Ui_MainWindow
from AddAccountDialog import AddAccountDialog
from SelectAccountDialog import SelectAccountDialog
from AddFundDialog import AddFundDialog
from UnitPurchaseDialog import UnitPurchaseDialog
from AccountValueDialog import AccountValueDialog
from database import connectDB, fetchAccounts
from db_objects import Fund, AccountValue, UnitPurchase
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class FundTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, fund):
    QtWidgets.QTableWidgetItem.__init__(self, fund.name)
    self.fund = fund

class AccountValuesTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, account_value):
    QtWidgets.QTableWidgetItem.__init__(self, account_value.date)
    self.account_value = account_value

class PurchasesTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, date, purchase):
    QtWidgets.QTableWidgetItem.__init__(self, date)
    self.purchase = purchase

class FloatTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, format_string, num):
    self.num = num
    QtWidgets.QTableWidgetItem.__init__(self, format_string % num)
    self.setTextAlignment(int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
  def __lt__(self, other):
    return self.num < other.num

def get_application_path():
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # Running as normal Python script
        return os.path.dirname(os.path.abspath(__file__))


#%%


class UnitTracker(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self, accounts_file, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    # set the working directory to the application path so that relative paths work
    self.app_path = get_application_path()
   
    self.setupUi(self)

    # Set the application icon
    self.setApplicationIcon()

    self.setStyleSheet("""
            QWidget {
                font-size: 12pt;
            }""")
            
    # set up the funds, purchases tables
    self.funds_table.setHorizontalHeaderLabels(["Name", "Initial Units", "End Units", "% of Total"])
    self.purchases_table.setHorizontalHeaderLabels(["Date", "Fund Name", "Amount", "Units Purchased"])
    self.account_values_table.setHorizontalHeaderLabels(["Date", "Account Value"])
    # windows fix for missing rule beneath header
    self.tableHeaderFix(self.funds_table)
    self.tableHeaderFix(self.purchases_table)
    self.tableHeaderFix(self.account_values_table)
    # hide the tab view until we have an active account
    self.tabWidget.setVisible(False)
    # disable edit for tables
    self.disableEditAllTables()
    self.funds_table.setColumnWidth(0, 300)
    self.purchases_table.setColumnWidth(1, 300)
    self.funds_table.setMaximumWidth(self.tableTotalWidth(self.funds_table) + 2)
    self.purchases_table.setMaximumWidth(self.tableTotalWidth(self.purchases_table) + 2)
    self.account_values_table.setMaximumWidth(self.tableTotalWidth(self.account_values_table) + 2)
    #enable sort in funds table
    self.funds_table.setSortingEnabled(False)             # disable built-in sort
    hh = self.funds_table.horizontalHeader()
    hh.setSortIndicatorShown(True)
    hh.sectionClicked.connect(self.onFundsHeaderClicked)
    self._funds_sort_col = 0
    self._funds_sort_order = QtCore.Qt.AscendingOrder




    #  disable menu items until account is loaded
    self.menuFunds.setEnabled(False)



    #  database variables
    self.db_filename = accounts_file
    self.con = connectDB(self.db_filename)  # connection to sqlite
    if (not self.con):
      print ("Database not found")
    else:
      self.backupDB()
    
    # fetch the accounts from the database
    self.accounts = fetchAccounts(self.con)
    self.active_account = None


    # UI Controls

    #  connect the menu items to methods
    self.actionNew_Account.triggered.connect(self.newAccount)
    self.actionOpen_Account.triggered.connect(self.openAccount)
    self.actionEdit_Account.triggered.connect(self.editAccount)
    self.actionDelete_Account.triggered.connect(self.deleteAccount)
    self.actionExport_to_Excel.triggered.connect(self.exportToExcel)
    self.actionNew_Fund.triggered.connect(self.newFund)
    self.actionPurchase_Fund.triggered.connect(self.purchaseFund)
    self.actionHide_Empty.toggled.connect(self.hideEmptyFunds)
    self.actionEdit_Mode.triggered.connect(self.editMode)
    self.actionNo_Warnings.triggered.connect(self.noWarnings)
    self.actionAdd_Account_Value.triggered.connect(self.addAccountValue)
    self.actionBackup_Now.triggered.connect(self.backupDB)


    # advanced mode options
    self.warnings_enabled = True

  def setApplicationIcon(self):
    """Set the application icon for the window and taskbar"""
    icon_path = os.path.join(get_application_path(), "icon.ico")
    if os.path.isfile(icon_path):
      try:
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
          print(f"Failed to load image from {icon_path}")
          return

        # Create icon from pixmap
        icon = QIcon(pixmap)

        # Set the window icon
        self.setWindowIcon(icon)

        # For better taskbar support, set multiple icon sizes
        # This helps with taskbar display on Windows/Linux
        icon.addPixmap(pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.addPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.addPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.addPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.addPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Set for both window and application
        self.setWindowIcon(icon)
        QtWidgets.QApplication.instance().setWindowIcon(icon)

      except Exception as e:
        print(f"Failed to load icon from {icon_path}: {e}")
    else:
      print("No icon file found.")
		


  # capture the close event so that we can properly close the database connection
  def closeEvent(self, event):
    if hasattr(self, 'con') and self.con:
        self.con.close()
    super().closeEvent(event)  # Always call parent


  def fillAccountSummaryBox(self):
      # set the account summary box
      self.account_name.setText(self.active_account.name)
      self.brokerage.setText(self.active_account.brokerage)
      self.account_number.setText(self.active_account.account_no)

###############################
##
##  Warnings
##
###############################

  def noWarnings(self):
    self.warnings_enabled = not self.actionNo_Warnings.isChecked()

  def noInitialUnitsWarning(self):
    self.showWarningDialog(
        "UnitTracker Warning",
        "You must have at least one fund with non-zero initial units in order "
        "for entries to show in the purchases tab"
    )

  def dangerousEditWarning(self):
      if not self.warnings_enabled:
          return True
      
      return self.showYesCancelDialog(
          "UnitTracker Warning",
          "Warning: The edit you are about to perform cannot be undone",
          "This edit may result in recomputation of all fund units dating back "
          "to the start of this account\n"
          "Click Yes to continue with this edit, otherwise click Cancel"
      )

###############################
##
##  Accounts Menu
##
###############################

  def newAccount(self):
    dialog = AddAccountDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      dialog.account.insertIntoDB(self.con)
      self.con.commit()
      self.accounts += [dialog.account]
      self.setActiveAccount(dialog.account)
      self.noInitialUnitsWarning()

  def openAccount(self):
    dialog = SelectAccountDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      self.setActiveAccount(dialog.selectedAccount())
      if (self.active_account.initialUnitValuesIsZero()):
        self.noInitialUnitsWarning()

  #edit account applies to the active account only. To edit other accounts, you must make them active
  def editAccount(self):
    if (self.dangerousEditWarning()):
      dialog = AddAccountDialog(self, True, self.active_account)
      if (dialog.exec() == QtWidgets.QDialog.Accepted):
        self.active_account.copy(dialog.account)
        self.active_account.updateToDB(self.con)
        self.fillAccountSummaryBox()

  def deleteAccount(self):
    if not self.dangerousEditWarning():
        return
    dialog = SelectAccountDialog(self)
    dialog.setWindowTitle("Select Account to Delete")
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        if dialog.selectedAccount() == self.active_account:
            self.showWarningDialog(
                "UnitTracker Warning",
                "You cannot delete the currently active account",
                "Open a different account and try again"
            )
        else:
            acct = dialog.selectedAccount()
            acct.deleteAccount(self.con)
            self.accounts.remove(acct)

  def setActiveAccount(self, account):
      self.active_account = account
      self.setWindowTitle("unitTracker - %s" % account.name)
      self.active_account.initialize(self.con)
      # populate the funds table in the funds tab
      self.populateFundsTable()
      # populate the purchases table in the purchases tab
      self.populatePurchasesTable()
      # populate the accounts values table in the account values tab
      self.populateAccountValuesTable()

      self.fillAccountSummaryBox()
      # show the tab view
      self.tabWidget.setVisible(True)
      # enable menu items now that we have an account
      self.menuFunds.setEnabled(True)
      self.actionAdd_Account_Value.setEnabled(True)
      #enable the edit account menu item only if advanced edit is enabled
      if (self.actionEdit_Mode.isChecked()):
        self.actionEdit_Account.setEnabled(True)
      else:
        self.actionEdit_Account.setEnabled(False)
      self.actionExport_to_Excel.setEnabled(True)

  def exportToExcel(self):
    (file_name, filter) = QtWidgets.QFileDialog.getSaveFileName(self, "Excel File Name",
                                                                directory = self.active_account.name + ".xlsx",
                                                                filter = ("Excel Files (*.xlsx) ;; All Files (*.*)"))
    if (file_name != ''):
      self.active_account.exportXLSX(file_name)


###############################
##
## Funds Menu
##
###############################


  def newFund(self):
    dialog = AddFundDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      new_fund = dialog.fund
      new_fund.insertIntoDB(self.con)
      self.active_account.addFund(new_fund,self.con)
      self.populateFundsTable()


  def purchaseFund(self):
    dialog = UnitPurchaseDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      # get existing AccountValue obj or create a new one
      if (dialog.knownAccountValueObj()):
       av = dialog.knownAccountValueObj()
      else:
        # create a new AccountValue object
        av = AccountValue(0, dialog.date(), dialog.accountValueDollars(), self.active_account.id)
        av.insertIntoDB(self.con)
        # update the account_values list in active account and update display
        self.active_account.addValue(av)
        self.populateAccountValuesTable()
      # create the unit purchase object
      up = UnitPurchase(0, dialog.fund().id, dialog.dollarsPurchased(), av.id)
      up.insertIntoDB(self.con)
      self.active_account.processPurchases(self.con)
      self.populatePurchasesTable()
      self.populateFundsTable()

  def hideEmptyFunds(self):
      self.populateFundsTable()
      self.populatePurchasesTable()


###############################
##
##  Advanced Menu
##
###############################



  def editMode(self):
    if self.actionEdit_Mode.isChecked():
        if self.active_account is not None:
            self.actionEdit_Account.setEnabled(True)     
        self.actionDelete_Account.setEnabled(True)
        self.funds_table.cellDoubleClicked.connect(self.fundTableEdit)
        self.purchases_table.cellDoubleClicked.connect(self.purchasesTableEdit)
        self.account_values_table.cellDoubleClicked.connect(self.accountValuesTableEdit)
        self.enableEditAllTables()

        if self.warnings_enabled:
            self.showWarningDialog(
                "UnitTracker Warning",
                "You have enabled potentially dangerous edits that cannot be undone.\n"
                "Proceed with care"
            )
    else:
        self.actionEdit_Account.setEnabled(False)
        self.actionDelete_Account.setEnabled(False)
        try:
            self.funds_table.cellDoubleClicked.disconnect(self.fundTableEdit)
        except TypeError:
            pass  # Already disconnected
        try:
            self.purchases_table.cellDoubleClicked.disconnect(self.purchasesTableEdit)
        except TypeError:
            pass  # Already disconnected
        try:
            self.account_values_table.cellDoubleClicked.disconnect(self.accountValuesTableEdit)
        except TypeError:
            pass  # Already disconnected      
        self.disableEditAllTables()
 
  def addAccountValue(self):
    dialog = AccountValueDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      # create a new AccountValue object
      av = AccountValue(0, dialog.date(), dialog.accountValueDollars(), self.active_account.id)
      av.insertIntoDB(self.con)
      # update the account_values list in active account and update display
      self.active_account.addValue(av)
      self.populateAccountValuesTable()




###############################
##
##  Table Edits
##
###############################



  def fundTableEdit(self, row, col):
    if row == self.funds_table.rowCount() - 1:
        self.funds_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 2), False)
        return
    fund = self.funds_table.item(row, 0).fund
    self.funds_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 2), True)
    dialog = AddFundDialog(self, True, fund)
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        if dialog.delete():
            should_delete = True
            if self.warnings_enabled:
                should_delete = self.showYesCancelDialog(
                    "UnitTracker Warning",
                    "Deleting a fund cannot be undone. You should only delete a fund if it was "
                    "created in error. If you're just trying to hide the fund because it has "
                    "been zeroed out, use Hide Empty on the Funds menu\n"
                    "Click Yes to continue with delete, otherwise click Cancel"
                )
            
            if should_delete:
                self.active_account.deleteFund(fund, self.con)
        else:
            fund.copy(dialog.fund)
            fund.updateToDB(self.con)
            if dialog.initialUnitsChanged():
                self.active_account.fundChanged(self.con)
            self.active_account.fund_names[fund.id] = fund.name
        self.populateFundsTable()
        self.populatePurchasesTable()
    self.funds_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 2), False)



  def purchasesTableEdit(self, row, col):
    purchase = self.purchases_table.item(row, 0).purchase
    self.purchases_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 3), True)
    dialog = UnitPurchaseDialog(self, True, purchase)
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        if dialog.delete():
            should_delete = True
            if self.warnings_enabled:
                should_delete = self.showYesCancelDialog(
                    "UnitTracker Warning",
                    "Deleting a purchase cannot be undone. You should only delete a purchase if it was "
                    "created in error. If you're just trying to hide a purchase because the fund because it has "
                    "been zeroed out, use Hide Empty on the Funds menu\n"
                    "Click Yes to continue with delete, otherwise click Cancel"
                )
            
            if should_delete:
                purchase.deleteFromDB(self.con)
        else:
            # get existing AccountValue obj or create a new one
            if dialog.knownAccountValueObj():
                av = dialog.knownAccountValueObj()
            else:
                # create a new AccountValue object
                av = AccountValue(0, dialog.date(), dialog.accountValueDollars(), self.active_account.id)
                av.insertIntoDB(self.con)
                # update the account_values list in active account and update display
                self.active_account.addValue(av)
                self.populateAccountValuesTable()
            # update the unit purchase object
            purchase.date_id = av.id
            purchase.amount = dialog.dollarsPurchased()
            purchase.updateToDB(self.con)
        self.active_account.processPurchases(self.con)
        self.populatePurchasesTable()
        self.populateFundsTable()
    self.purchases_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 3), False)

  def accountValuesTableEdit(self, row, col):
    av = self.account_values_table.item(row, 0).account_value
    self.account_values_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 1), True)
    dialog = AccountValueDialog(self, True, av)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      av.value = dialog.accountValueDollars()
      av.updateToDB(self.con)
      self.active_account.processPurchases(self.con)
      self.populateFundsTable()
      self.populatePurchasesTable()
      self.populateAccountValuesTable()
    self.account_values_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 1), False)




###############################
##
##  Table Helper methods
##
###############################


  def populateFundsTable(self):
    was_sorting = self.funds_table.isSortingEnabled()
    self.funds_table.setSortingEnabled(False)
    self.funds_table.setUpdatesEnabled(False)
    try:
        table = self.funds_table
        table.clearContents()

        # First pass: count visible rows
        visible_funds = []
        for f in self.active_account.funds:
            if not (self.actionHide_Empty.isChecked() and self.active_account.end_units[f.id] == 0):
                visible_funds.append(f)

        # Size to visible rows + 1 for totals
        table.setRowCount(len(visible_funds) + 1)

        # Fill visible rows
        row = 0
        for f in visible_funds:
            if (table.columnSpan(row, 0) != 1):
                table.setSpan(row, 0, 1, 1)  # undo any leftover spans
            table.setItem(row, 0, FundTableItem(f))
            table.setItem(row, 1, FloatTableItem("%.3f", f.initial_units))
            end_units = self.active_account.end_units[f.id]
            table.setItem(row, 2, FloatTableItem("%.3f", end_units))
            percentage = end_units / self.active_account.total_units if self.active_account.total_units > 0 else 0
            table.setItem(row, 3, FloatTableItem("%.4f%%", percentage * 100))
            row += 1

        # Totals row goes at the real last index
        totals_row = row
        table.setSpan(totals_row, 0, 1, 2)
        total_label = QtWidgets.QTableWidgetItem("Total Units")
        total_label.setTextAlignment(int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
        table.setItem(totals_row, 0, total_label)
        table.setItem(totals_row, 2, FloatTableItem("%.3f", self.active_account.total_units))
        self.styleTotalsRow(totals_row)
    finally:
        self.funds_table.setUpdatesEnabled(True)
        self.funds_table.setSortingEnabled(was_sorting)

  def onFundsHeaderClicked(self, col):
    # toggle order if same column, otherwise reset to ascending
    if col == self._funds_sort_col:
        self._funds_sort_order = (
            QtCore.Qt.DescendingOrder
            if self._funds_sort_order == QtCore.Qt.AscendingOrder
            else QtCore.Qt.AscendingOrder
        )
    else:
        self._funds_sort_col = col
        self._funds_sort_order = QtCore.Qt.AscendingOrder

    # show the correct arrow
    self.funds_table.horizontalHeader().setSortIndicator(
        self._funds_sort_col, self._funds_sort_order
    )

    self.sortFundsPreservingTotals(self._funds_sort_col, self._funds_sort_order)

  def sortFundsPreservingTotals(self, column, order):
    """
    Sort the funds table while keeping the totals row fixed at the bottom.
    Since Qt's sortItems() would move the totals row, we temporarily remove it,
    sort, then reinsert it.
    """
    table = self.funds_table

    # ensure totals row is physically last (see your populate fix)
    totals_row_idx = table.rowCount() - 1
    if totals_row_idx < 0:
        return

    # Take totals row out, so it never gets sorted
    totals_items = [table.takeItem(totals_row_idx, c) for c in range(table.columnCount())]
    table.removeRow(totals_row_idx)

    # Let Qt sort rows (works even with setSortingEnabled(False))
    table.sortItems(column, order)

    # Put totals row back at the end (and restore any spans/format)
    new_totals_row = table.rowCount()
    table.insertRow(new_totals_row)
    for c, it in enumerate(totals_items):
        if it is not None:
            table.setItem(new_totals_row, c, it)
    # If you had a span on the totals label cell:
    try:
        table.setSpan(new_totals_row, 0, 1, 2)
    except Exception:
        pass
    self.styleTotalsRow(new_totals_row)


  def styleTotalsRow(self, row):
      """Apply bold + shaded style to the totals row."""
      table = self.funds_table
      for col in range(table.columnCount()):
          item = table.item(row, col)
          if item is not None:
              # Bold font
              font = item.font()
              font.setBold(True)
              item.setFont(font)

              # Light gray background
              item.setBackground(QtGui.QColor("#f0f0f0"))

              # Darker text
              item.setForeground(QtGui.QBrush(QtGui.QColor("#202020")))

  def populatePurchasesTable(self):
    # Guard: disable sorting & repaints while filling
    was_sorting = self.purchases_table.isSortingEnabled()
    self.purchases_table.setSortingEnabled(False)
    self.purchases_table.setUpdatesEnabled(False)
    try:
        row = 0
        self.purchases_table.clearContents()

        # Build the rows we actually want to show
        filtered = []
        for p in self.active_account.purchases:
            if not (self.actionHide_Empty.isChecked() and self.active_account.end_units[p.fund_id] == 0):
                filtered.append(p)

        # Size exactly once
        self.purchases_table.setRowCount(len(filtered))

        # Fill
        for row, p in enumerate(filtered):
            self.purchases_table.setItem(
                row, 0,
                PurchasesTableItem(self.active_account.account_values_by_id[p.date_id].date, p)
            )
            self.purchases_table.setItem(row, 1,
                QtWidgets.QTableWidgetItem(self.active_account.fund_names[p.fund_id]))
            self.purchases_table.setItem(row, 2, FloatTableItem("$%.2f", p.amount))
            self.purchases_table.setItem(row, 3, FloatTableItem("%.3f", p.units_purchased))
    finally:
        # Restore UI behavior
        self.purchases_table.setUpdatesEnabled(True)
        self.purchases_table.setSortingEnabled(was_sorting)


  def populateAccountValuesTable(self):
    was_sorting = self.account_values_table.isSortingEnabled()
    self.account_values_table.setSortingEnabled(False)
    self.account_values_table.setUpdatesEnabled(False)
    try:
      row = 0
      self.account_values_table.clearContents()
      self.account_values_table.setRowCount(len(self.active_account.account_values_sorted_by_date))
      for av in self.active_account.account_values_sorted_by_date:
        self.account_values_table.setItem(row, 0, AccountValuesTableItem(av))
        self.account_values_table.setItem(row, 1, FloatTableItem("$%.2f", av.value))
        row += 1
    finally:
        self.account_values_table.setUpdatesEnabled(True)
        self.account_values_table.setSortingEnabled(was_sorting)

        
  def tableTotalWidth(self, table):
    width = 0
    for col in range(table.columnCount()):
      width += table.columnWidth(col)
    return width

  def disableEditAllTables(self):
    self.disableTableEdit(self.purchases_table)
    self.disableTableEdit(self.funds_table)
    self.disableTableEdit(self.account_values_table)

  def disableTableEdit(self, table):
    table.clearSelection()
    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers);
    self.setFocusPolicy(QtCore.Qt.NoFocus);
    table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection);


  def enableEditAllTables(self):
    self.enableTableEdit(self.purchases_table)
    self.enableTableEdit(self.funds_table)
    self.enableTableEdit(self.account_values_table)

  def enableTableEdit(self, table):
    table.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection);
    table.setFocusPolicy(QtCore.Qt.ClickFocus)

  def tableHeaderFix(self, table):
    table.setStyleSheet(
      "QHeaderView::section { Background-color:rgb(250,250,250); border-bottom-width:  10px; }" )

###############################
##
##  utility methods
##
################################

  def backupDB(self):
    try:
        backup_dir = os.path.join(os.path.dirname(self.db_filename), "backup")
        os.makedirs(backup_dir, exist_ok=True)  # Safer than exists() + mkdir

        db_name = os.path.splitext(os.path.basename(self.db_filename))[0]
        timestamp = date.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_file = os.path.join(backup_dir, f"{db_name}_{timestamp}.db")

        shutil.copyfile(self.db_filename, backup_file)
    except Exception as e:
        print(f"Backup failed: {e}")
        # Optionally show user warning

  def showWarningDialog(self, title, message, informative_text=""):
      """
      Show a warning dialog with only a Close button.
      Returns None (for consistency, though return value isn't used).
      """
      msg_box = QMessageBox(self)
      msg_box.setWindowTitle(title)
      msg_box.setText(message)
      if informative_text:
          msg_box.setInformativeText(informative_text)
      msg_box.setIcon(QMessageBox.Warning)
      msg_box.setStandardButtons(QMessageBox.Close)
      msg_box.exec()

  def showYesCancelDialog(self, title, message, informative_text="", default_button=QMessageBox.Cancel):
      """
      Show a warning dialog with Yes/Cancel buttons.
      Returns True if Yes is clicked, False if Cancel is clicked.
      """
      msg_box = QMessageBox(self)
      msg_box.setWindowTitle(title)
      msg_box.setText(message)
      if informative_text:
          msg_box.setInformativeText(informative_text)
      msg_box.setIcon(QMessageBox.Warning)
      msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
      msg_box.setDefaultButton(default_button)
      return msg_box.exec() == QMessageBox.Yes

#%%
if (__name__ == '__main__'):
  # Fix for Windows taskbar icon - must be done before QApplication creation
  try:
    # This tells Windows that this is a separate app, not just a Python script
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('stripfamily.unittracker.1.0')
  except ImportError:
    pass  # Not Windows or ctypes not available
  
  app = QtWidgets.QApplication(sys.argv)
  
  # Set application properties for better icon handling
  app.setApplicationName("UnitTracker")
  app.setApplicationDisplayName("Unit Tracker")
  app.setApplicationVersion("1.0a")

  
  # Additional settings for better taskbar integration
  if hasattr(app, 'setDesktopFileName'):
    app.setDesktopFileName("unittracker")
  
  myapp = UnitTracker(sys.argv[1])
  myapp.show()
  
  # Force the application to stay in front briefly to help with taskbar icon registration
  myapp.raise_()
  myapp.activateWindow()
  
  sys.exit(app.exec())