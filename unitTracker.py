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




#%%
class UnitTracker(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # database variables
    self.db_filename = "test.db"
    self.con = connectDB(self.db_filename)  #connection to sqlite

    self.accounts = fetchAccounts(self.con)
    # self.funds
    self.active_account = None



    # connect the menu items to methods
    self.ui.actionNew_Account.triggered.connect(self.newAccount)
    self.ui.actionOpen_Account.triggered.connect(self.openAccount)
    self.ui.actionNew_Fund.triggered.connect(self.newFund)
    self.ui.actionPurchase_Fund.triggered.connect(self.purchaseFund)

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
    dialog.open()

  def setActiveAccount(self, account):
    self.active_account = account
    self.setWindowTitle("unitTracker - %s" % account.name)

  def newFund(self):
    print("new fund clicked")

  def purchaseFund(self):
    print("purchase fund clicked")





#%%
app = QtWidgets.QApplication(sys.argv)
myapp = UnitTracker()
myapp.show()
app.exec()


