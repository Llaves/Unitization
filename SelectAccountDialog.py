# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#



from select_account import *


class SelectAccountDialog(QtWidgets.QDialog, Ui_selectAccountDialog):
  def __init__ (self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    # populate the comboBox
    for a in parent.accounts:
      self.select_account.insertItem(9999, a.name, a)


  def selectedAccount(self):
    return self.select_account.currentData()
