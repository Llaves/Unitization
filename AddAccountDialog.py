# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:53:31 2021

@author: David
"""

from add_account_dialog import *
from db_objects import Account

class AddAccountDialog(QtWidgets.QDialog, Ui_AddAccountDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.btn_save = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
    self.btn_save.setEnabled(False)
    self.account_number.textChanged.connect(self.onTextChanged)
    self.acct_name.textChanged.connect(self.onTextChanged)
    self.brokerage.textChanged.connect(self.onTextChanged)
    self.parent = parent

  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.btn_save.setEnabled(bool(self.account_number.text())
                              and bool(self.acct_name.text())
                              and bool(self.brokerage_edit.text()))

  def accept(self):
    a = Account(0, self.acct_name.text(), self.brokerage_edit.text(), self.account_number.text())
    a.insertIntoDB(self.parent.con)
    self.parent.con.commit()
    print("Implement check on database insertion")
    self.parent.accounts += [a]
    self.parent.setActiveAccount(a)
    QtWidgets.QDialog.accept(self)