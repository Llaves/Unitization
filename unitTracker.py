# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:15:55 2021

@author: David
"""

import sys
from os import path
from main_window import *
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




#%%
class unitTracker(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.actionOpen_Account.triggered.connect(self.openAccount)

  def openAccount(self):
    print("clicked")
    dialog = AddAccountDialog(self)

    dialog.open()



#%%
app = QtWidgets.QApplication(sys.argv)
myapp = unitTracker()
myapp.show()
app.exec()


