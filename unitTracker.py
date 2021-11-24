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
    self.disableTableEdit(self.funds_table)
    self.disableTableEdit(self.purchases_table)
    self.disableTableEdit(self.account_values_table)
    self.funds_table.setMaximumWidth(self.tableTotalWidth(self.funds_table) + 2)
    self.purchases_table.setMaximumWidth(self.tableTotalWidth(self.purchases_table) + 2)
    self.account_values_table.setMaximumWidth(self.tableTotalWidth(self.account_values_table) + 2)


    #  disable menu items until account is loaded
    self.menuFunds.setEnabled(False)
    self.menuPurchases.setEnabled(False)



    #  database variables
    self.db_filename = "test.db"
    self.con = connectDB(self.db_filename)  # connection to sqlite

    self.accounts = fetchAccounts(self.con)
    self.active_account = None


    # GI Control

    #  connect the menu items to methods
    self.actionNew_Account.triggered.connect(self.newAccount)
    self.actionOpen_Account.triggered.connect(self.openAccount)
    self.actionNew_Fund.triggered.connect(self.newFund)
    self.actionPurchase_Fund.triggered.connect(self.purchaseFund)
    self.actionDelete_Fund.triggered.connect(self.deleteFund)

    # advanced mode options
    self.warnings_enabled = True

  # capture the close event so that we can properly close the database connection
  def closeEvent(self, event):
    self.con.close()
    self.close()

  def newAccount(self):
    print("new Account clicked")
    dialog = AddAccountDialog(self)
    dialog.open()


  def openAccount(self):
    dialog = SelectAccountDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      self.setActiveAccount(dialog.selectedAccount())

  def populateFundsTable(self):
    row = 0
    self.funds_table.clearContents()
    for f in self.active_account.funds:
      self.funds_table.setItem(row, 0, FundTableItem(f))  # QtWidgets.QTableWidgetItem(f.name))
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
      self.menuPurchases.setEnabled(True)



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
    if self.warnings_enabled:
      msg_box = QMessageBox()
      msg_box.setText("Warning: deleted funds cannot be restored.")
      msg_box.setInformativeText("Deleting a fund will result in recomputation of historical"\
                                 " unit values for remaining funds. Consider using the Hide Empty Funds "\
                                   "option in the Advanced menu")

      msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
      msg_box.setIcon(QMessageBox.Warning)
      msg_box.setWindowTitle("UnitTracker Warning")
      msg_box.setDefaultButton(QMessageBox.Discard)
      if (msg_box.exec() == QMessageBox.Yes):
        print ("deleting fund")
        dialog = DeleteFundDialog(self)
        if (dialog.exec() == QtWidgets.QDialog().Accepted):
          print(dialog.fund())
          self.active_account.deleteFund(dialog.fund(), self.con)
          self.populateFundsTable()
          self.populatePurchasesTable()


  # misc dialog management functions
  def tableTotalWidth(self, table):
    width = 0
    for col in range(table.columnCount()):
      width += table.columnWidth(col)
    return width

  def disableTableEdit(self, table):
    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers);
    table.setFocusPolicy(QtCore.Qt.NoFocus);
    table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection);

  def tableHeaderFix(self, table):
    table.setStyleSheet(
      "QHeaderView::section { Background-color:rgb(250,250,250); border-bottom-width:  10px; }" )


#%%
app = QtWidgets.QApplication(sys.argv)
myapp = UnitTracker()
myapp.show()
app.exec()
