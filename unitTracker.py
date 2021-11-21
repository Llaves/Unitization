# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:15:55 2021

@author: David
"""

import sys
from os import path
from main_window import *
from AddAccountDialog import AddAccountDialog
from SelectAccountDialog import SelectAccountDialog
from AddFundDialog import AddFundDialog
from UnitPurchaseDialog import UnitPurchaseDialog
from database import connectDB, initializeDB, fetchAccounts
from db_objects import Account, Fund, AccountValue, UnitPurchase




#%%
class UnitTracker(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.setupUi(self)

    #set up the funds, purchases tables
    self.funds_table.setHorizontalHeaderLabels(["Name", "Initial Units", "End Units"])
    self.purchases_table.setHorizontalHeaderLabels(["Date", "Fund Name", "Amount", "Units Purchased"])
    #windows fix for missing rule beneath header
    self.funds_table.horizontalHeader().setStyleSheet(
      "QHeaderView::section { Background-color:rgb(250,250,250); border-bottom-width:  10px; }" )
    self.purchases_table.horizontalHeader().setStyleSheet(
      "QHeaderView::section { Background-color:rgb(250,250,250); border-bottom-width:  10px; }" )
    #hide the tab view until we have an active account
    self.tabWidget.setVisible(False)
    #disable edit for fund and purchases tables
    self.disableTableEdit(self.funds_table)
    self.disableTableEdit(self.purchases_table)
    self.funds_table.setMaximumWidth(self.tableTotalWidth(self.funds_table) + 2)
    self.purchases_table.setMaximumWidth(self.tableTotalWidth(self.purchases_table) + 2)

    # disable menu items until account is loaded
    self.menuFunds.setEnabled(False)
    self.menuPurchases.setEnabled(False)



# database variables
    self.db_filename = "test.db"
    self.con = connectDB(self.db_filename)  #connection to sqlite

    self.accounts = fetchAccounts(self.con)
    # self.funds
    self.active_account = None



    # connect the menu items to methods
    self.actionNew_Account.triggered.connect(self.newAccount)
    self.actionOpen_Account.triggered.connect(self.openAccount)
    self.actionNew_Fund.triggered.connect(self.newFund)
    self.actionPurchase_Fund.triggered.connect(self.purchaseFund)

  def newAccount(self):
    print("new Account clicked")
    dialog = AddAccountDialog(self)
    dialog.open()


  def openAccount(self):
    dialog = SelectAccountDialog(self)
    # populate the comboBox
    for a in self.accounts:
      dialog.selectAccountComboBox.insertItem(9999, a.name, a)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      self.setActiveAccount(dialog.selectedAccount())

  def populateFundsTable(self):
    row = 0
    for f in self.active_account.funds:
      self.funds_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f.name))
      self.funds_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(f.initial_units)))
      end_units =self.active_account.end_units[self.active_account.fundCol(f)]
      self.funds_table.setItem(row, 2, QtWidgets.QTableWidgetItem("%.3f" % end_units))
      row += 1

  def populatePurchasesTable(self):
    row = 0
    for p in self.active_account.purchases:
      self.purchases_table.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(
                                     self.active_account.account_values[p.date_id].date))
      self.purchases_table.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(self.active_account.fund_names[p.fund_id]))
      self.purchases_table.setItem(row, 2, QtWidgets.QTableWidgetItem("$%.2f" % p.amount))
      self.purchases_table.setItem(row, 3, QtWidgets.QTableWidgetItem("%.3f" % p.units_purchased))
      row += 1

  def setActiveAccount(self, account):
      self.active_account = account
      self.setWindowTitle("unitTracker - %s" % account.name)
      self.active_account.initialize(self.con)
      #populate the funds table in the funds tab
      self.populateFundsTable()
      #populate the purchases table in the purchases tab
      self.populatePurchasesTable()

      # set the account summary box
      self.account_name.setText(self.active_account.name)
      self.brokerage.setText(self.active_account.brokerage)
      self.account_number.setText(self.active_account.account_no)
      #show the tab view
      self.tabWidget.setVisible(True)
      #enable menu items now that we have an account
      self.menuFunds.setEnabled(True)
      self.menuPurchases.setEnabled(True)



  def newFund(self):
    dialog = AddFundDialog(self)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      new_fund = Fund(0, dialog.fundName(), dialog.initialUnits(), self.active_account.id)
      new_fund.insertIntoDB(self.con)
      print (new_fund)
      self.active_account.funds += [new_fund]
      self.active_account.createFundIdx()
      self.active_account.initialUnitValues()
      self.active_account.processPurchases()
      self.populateFundsTable()


  def purchaseFund(self):
    print("purchase fund clicked")


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


#%%
app = QtWidgets.QApplication(sys.argv)
myapp = UnitTracker()
myapp.show()
app.exec()


