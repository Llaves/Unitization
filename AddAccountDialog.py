# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:53:31 2021

@author: David
"""

from add_account_dialog import *

class AddAccountDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_AddAccountDialog()
    self.ui.setupUi(self)
    self.btn_save = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
    self.btn_save.setEnabled(False)
    self.ui.account_number_edit.textChanged.connect(self.onTextChanged)
    self.ui.acct_name_edit.textChanged.connect(self.onTextChanged)
    self.ui.brokerage_edit.textChanged.connect(self.onTextChanged)

  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.btn_save.setEnabled(bool(self.ui.account_number_edit.text())
                              and bool(self.ui.acct_name_edit.text())
                              and bool(self.ui.brokerage_edit.text()))

  def accept(self):
    print ("Accept called")
    QtWidgets.QDialog.accept(self)