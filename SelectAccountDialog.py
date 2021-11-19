# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:22:38 2021

@author: David
"""

from select_account import *


class SelectAccountDialog(QtWidgets.QDialog, Ui_selectAccountDialog):
  def __init__ (self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.buttonBox.accepted.connect(self.accepted)
    self.parent = parent


  def selectedAccount(self):
    return self.selectAccountComboBox.currentData()

  def accepted(self):
    print(self.parent)
    self.parent.setActiveAccount(self.selectAccountComboBox.currentData())