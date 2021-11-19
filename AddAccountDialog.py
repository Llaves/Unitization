# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:53:31 2021

@author: David
"""

from add_account_dialog import *

class AddAccountDialog(QtWidgets.QDialog, Ui_AddAccountDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.btn_save = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
    self.btn_save.setEnabled(False)
    self.account_number_edit.textChanged.connect(self.onTextChanged)
    self.acct_name_edit.textChanged.connect(self.onTextChanged)
    self.brokerage_edit.textChanged.connect(self.onTextChanged)

  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.btn_save.setEnabled(bool(self.account_number_edit.text())
                              and bool(self.acct_name_edit.text())
                              and bool(self.brokerage_edit.text()))

  def accept(self):
    print ("Accept called")
    QtWidgets.QDialog.accept(self)