# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:28:37 2021

@author: David
"""
from delete_fund import *

class DeleteFundDialog(QtWidgets.QDialog, Ui_FundDeleteDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.parent = parent
    self.setupUi(self)

    #populate the combo box
    combo = self.fund_to_delete
    for f in self.parent.active_account.funds:
      combo.insertItem(9999, f.name, f)

  def fund(self):
    return self.fund_to_delete.currentData()
