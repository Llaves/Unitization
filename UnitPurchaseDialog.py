# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 13:49:54 2021

@author: David
"""

from unit_purchase_dialog import *

class UnitPurchaseDialog(QtWidgets.QDialog, Ui_unitPurchaseDialog):
  def __init__(self, parent = None):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)