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
from database import connectDB, initializeDB, fetchAccounts
from db_objects import Account




#%%
class UnitTracker(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.setupUi(self)

    #set up the funds table
    self.funds_table.setHorizontalHeaderLabels(["Name", "Initial Units", "End Units"])
    #windows fix for missing rule beneath header
    self.funds_table.horizontalHeader().setStyleSheet(
      "QHeaderView::section { Background-color:rgb(250,250,250); border-bottom-width:  10px; }" )
    #hide the tab view until we have an active account
    self.tabWidget.setVisible(False)



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
    print ("open account clicked")
    dialog = SelectAccountDialog(self)
    #dialog.buttonBox.accepted.connect(self.openAccountComplete)
    # populate the comboBox
    for a in self.accounts:
      dialog.selectAccountComboBox.insertItem(0, a.name, a)
    if (dialog.exec() == QtWidgets.QDialog.Accepted):
      self.setActiveAccount(dialog.selectedAccount())

  def setActiveAccount(self, account):
    self.active_account = account
    self.setWindowTitle("unitTracker - %s" % account.name)
    self.active_account.initialize(self.con)
    row = 0
    for f in self.active_account.funds:
      print (f.name)
      self.funds_table.setItem(row, 0, QtWidgets.QTableWidgetItem(f.name))
      self.funds_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(f.initial_units)))
      end_units =self.active_account.end_units[self.active_account.fund_to_indx_dict[f.id]]
      self.funds_table.setItem(row, 2, QtWidgets.QTableWidgetItem("%.3f" % end_units))
      row += 1
    #show the tab view
    self.tabWidget.setVisible(True)



  def newFund(self):
    print("new fund clicked")

  def purchaseFund(self):
    print("purchase fund clicked")





#%%
app = QtWidgets.QApplication(sys.argv)
myapp = UnitTracker()
myapp.show()
app.exec()


