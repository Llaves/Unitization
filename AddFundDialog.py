# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:42:13 2021

@author: David
"""

from add_fund import *

class AddFundDialog(QtWidgets.QDialog, Ui_addFund):
  def __init__(self, parent = None):
      QtWidgets.QDialog.__init__(self, parent)
      self.setupUi(self)

      # set validator to doubles, three decimal places, greater than zero
      v = QtGui.QDoubleValidator()
      v.setBottom(0)
      v.setDecimals(3)
      self.initialUnitsEdit.setValidator(v)


  def fundName(self):
    return self.fundNameEdit.text()

  def initialUnits(self):
    return float(self.initialUnitsEdit.text())
