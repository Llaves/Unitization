# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:15:55 2021

@author: David
"""

import sys
from main_window import *
from AddAccountDialog import AddAccountDialog
from SelectAccountDialog import SelectAccountDialog
from AddFundDialog import AddFundDialog
from UnitPurchaseDialog import UnitPurchaseDialog
from DeleteFundDialog import DeleteFundDialog
from database import connectDB, fetchAccounts
from db_objects import Fund, AccountValue, UnitPurchase
from PyQt5.QtWidgets import QMessageBox


class FundTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, fund):
    QtWidgets.QTableWidgetItem.__init__(self, fund.name)
    self.fund = fund

class AccountValuesTableItem(QtWidgets.QTableWidgetItem):
  def __init__(self, account_value):
    QtWidgets.QTableWidgetItem.__init__(self, account_value.date)
    self.account_value = account_value

class ItemRightAlign(QtWidgets.QTableWidgetItem):
  def __init__(self, item):
    QtWidgets.QTableWidgetItem.__init__(self, item)
    self.setTextAlignment(int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))


#%%
class UnitTracker(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.setupUi(self)

    # set up the funds, purchases tables
    self.funds_table.setHorizontalHeaderLabels(["Name", "Initial Units", "End Units"])
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
    self.funds_table.setMaximumWidth(self.tableTotalWidth(self.funds_table) + 2)
    self.purchases_table.setMaximumWidth(self.tableTotalWidth(self.purchases_table) + 2)
    self.account_values_table.setMaximumWidth(self.tableTotalWidth(self.account_values_table) + 2)


    #  disable menu items until account is loaded
    self.menuFunds.setEnabled(False)



    #  database variables
    self.db_filename = "test.db"
    self.con = connectDB(self.db_filename)  # connection to sqlite

    self.accounts = fetchAccounts(self.con)
    self.active_account = None


    # GI Control

    #  connect the menu items to methods
    self.actionNew_Account.triggered.connect(self.newAccount)
    self.actionOpen_Account.triggered.connect(self.openAccount)
    self.actionDelete_Account.triggered.connect(self.deleteAccount)
    self.actionNew_Fund.triggered.connect(self.newFund)
    self.actionPurchase_Fund.triggered.connect(self.purchaseFund)
    self.actionDelete_Fund.triggered.connect(self.deleteFund)
    self.actionEdit_Mode.triggered.connect(self.editMode)
    self.actionNo_Warnings.triggered.connect(self.noWarnings)


    # advanced mode options
    self.warnings_enabled = True

  # capture the close event so that we can properly close the database connection
  def closeEvent(self, event):
    self.con.close()
    self.close()

  def noInitialUnitsWarning(self):
    msg_box = QMessageBox()
    msg_box.setText("You must have at least one fund with non-zero initial units in order "\
                    "for entries to show in the purchases tab")

    msg_box.setWindowTitle("UnitTracker Warning")
    msg_box.setStandardButtons(QMessageBox.Close)
    msg_box.exec()

  def dangerousEditWarning(self):
    if self.warnings_enabled:
      msg_box = QMessageBox()
      msg_box.setText("Warning: The edit you are about to perform cannot be undone")
      msg_box.setInformativeText(" This edit may result in recomputation of all fund units dating back" \
                                 " to the start of this account\n" \
                                   "Click Yes to continue with this edit, otherwise click Cancel")
      msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
      msg_box.setIcon(QMessageBox.Warning)
      msg_box.setWindowTitle("UnitTracker Warning")
      msg_box.setDefaultButton(QMessageBox.Cancel)
      return (msg_box.exec() == QMessageBox.Yes)
    else:
      return True


  def newAccount(self):
    print("new Account clicked")
    dialog = AddAccountDialog(self)
    if dialog.exec() == QtWidgets.QDialog.Accepted:
      self.noInitialUnitsWarning()



  def openAccount(self):
    dialog = SelectAccountDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      self.setActiveAccount(dialog.selectedAccount())
      if self.active_account.initialUnitsIsZero():
        self.noInitialUnitsWarning()()

  def deleteAccount(self):
    if self.dangerousEditWarning():
      dialog = SelectAccountDialog(self)
      dialog.setWindowTitle("Select Account to Delete")
      if (dialog.exec() == QtWidgets.QDialog.Accepted):
        if dialog.selectedAccount() == self.active_account:
          msg_box = QMessageBox()
          msg_box.setText("You cannot delete the currently active account")
          msg_box.setInformativeText("Open a different account and try again")
          msg_box.setStandardButtons(QMessageBox.Close )
          msg_box.setWindowTitle("UnitTracker Warning")
          msg_box.exec()
        else:
          acct = dialog.selectedAccount()
          acct.deleteAccount(self.con)
          self.accounts.remove(acct)




  def populateFundsTable(self):
    row = 0
    self.funds_table.clearContents()
    for f in self.active_account.funds:
      self.funds_table.setItem(row, 0, FundTableItem(f))
      self.funds_table.setItem(row, 1, ItemRightAlign(str(f.initial_units)))
      end_units =self.active_account.end_units[f.id]
      self.funds_table.setItem(row, 2, ItemRightAlign("%.3f" % end_units))
      row += 1

  def populatePurchasesTable(self):
    row = 0
    self.purchases_table.clearContents()
    for p in self.active_account.purchases:
      self.purchases_table.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(
                                     self.active_account.account_values_by_id[p.date_id].date))
      self.purchases_table.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(self.active_account.fund_names[p.fund_id]))
      self.purchases_table.setItem(row, 2, ItemRightAlign("$%.2f" % p.amount))
      self.purchases_table.setItem(row, 3, ItemRightAlign("%.3f" % p.units_purchased))
      row += 1

  def populateAccountValuesTable(self):
    row = 0
    self.account_values_table.clearContents()
    for av in self.active_account.account_values:
      self.account_values_table.setItem(row, 0, AccountValuesTableItem(av))
      self.account_values_table.setItem(row, 1, ItemRightAlign("$%.2f" % av.value))
      row += 1

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

      # set the account summary box
      self.account_name.setText(self.active_account.name)
      self.brokerage.setText(self.active_account.brokerage)
      self.account_number.setText(self.active_account.account_no)
      # show the tab view
      self.tabWidget.setVisible(True)
      # enable menu items now that we have an account
      self.menuFunds.setEnabled(True)



  def newFund(self):
    dialog = AddFundDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      new_fund = Fund(0, dialog.fundName(), dialog.initialUnits(), self.active_account.id)
      new_fund.insertIntoDB(self.con)
      self.active_account.addFund(new_fund,self.con)
      self.populateFundsTable()


  def purchaseFund(self):
    print("purchase fund clicked")
    dialog = UnitPurchaseDialog(self)
    if (dialog.exec() == QtWidgets.QDialog().Accepted):
      print ("Units purchased")
      print (dialog.date())
      print (dialog.fund())
      print (dialog.dollarsPurchased())
      # get existing AccountValue obj or create a new one
      if dialog.knownAccountValueObj():
        print("date found")
        av = dialog.knownAccountValueObj()
      else:
        print("date not found")
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

  def deleteFund(self):
    if self.dangerousEditWarning():
      dialog = DeleteFundDialog(self)
      if (dialog.exec() == QtWidgets.QDialog().Accepted):
        print(dialog.fund())
        self.active_account.deleteFund(dialog.fund(), self.con)
        self.populateFundsTable()
        self.populatePurchasesTable()

  def editMode(self):
    if self.actionEdit_Mode.isChecked():
      self.actionDelete_Account.setEnabled(True)
      self.actionDelete_Fund.setEnabled(True)
      self.funds_table.cellDoubleClicked.connect(self.fundTableEdit)
      self.enableEditAllTables()
      msg_box = QMessageBox()
      msg_box.setText("You have enabled potentially dangerous edits that cannot be undone.\n"\
                      "Proceed with care")
      msg_box.setStandardButtons(QMessageBox.Close)
      msg_box.setWindowTitle("UnitTracker Warning")
      msg_box.exec()
    else:
      self.funds_table.cellDoubleClicked.disconnect(self.fundTableEdit)
      self.disableEditAllTables()

  def fundTableEdit(self, row, col):
    print ("FundTableEdit row = %d col = %d" % (row,col))
    print (self.funds_table.item(row, 0).fund)

    self.funds_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, 2), True)



  def noWarnings(self):
    self.warnings_enabled = not self.actionNo_Warnings.isChecked()


  # misc dialog management functions
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
    table.setFocusPolicy(QtCore.Qt.NoFocus);
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


#%%
app = QtWidgets.QApplication(sys.argv)
myapp = UnitTracker()
myapp.show()
app.exec()
