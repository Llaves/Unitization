# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#


"""
Created on Thu Nov 18 11:53:31 2021

@author: David
"""

from add_account_dialog import *
from db_objects import Account
from copy import copy

class AddAccountDialog(QtWidgets.QDialog, Ui_AddAccountDialog):
  def __init__(self, parent, edit_mode = False, old_account = None):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.btn_save = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
    self.btn_save.setEnabled(False)
    self.account_number.textChanged.connect(self.onTextChanged)
    self.acct_name.textChanged.connect(self.onTextChanged)
    self.brokerage.textChanged.connect(self.onTextChanged)
    self.parent = parent
    self.edit_mode = edit_mode
    self.old_account = copy(old_account)

    if self.edit_mode:
      self.acct_name.setText(self.old_account.name)
      self.brokerage.setText(self.old_account.brokerage)
      self.account_number.setText(self.old_account.account_no)
      self.setWindowTitle("Edit current account")

  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.btn_save.setEnabled(bool(self.account_number.text())
                              and bool(self.acct_name.text())
                              and bool(self.brokerage.text()))

  def accept(self):
    self.account = Account(0, self.acct_name.text(), self.brokerage.text(), self.account_number.text())
    if self.edit_mode:
      self.account.id = self.old_account.id
    QtWidgets.QDialog.accept(self)
