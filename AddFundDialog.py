# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:42:13 2021

@author: David
"""

from add_fund import *
from PyQt5.QtWidgets import QMessageBox

class AddFundDialog(QtWidgets.QDialog, Ui_addFund):
  def __init__(self, parent):
      QtWidgets.QDialog.__init__(self, parent)
      self.setupUi(self)

      # set validator to doubles, three decimal places, greater than zero
      v = QtGui.QDoubleValidator()
      v.setBottom(0)
      v.setDecimals(3)
      self.initial_units.setText("0")
      self.initial_units.setValidator(v)
      if (len(parent.active_account.purchases) > 0):
        self.initial_units.editingFinished.connect(self.initialUnitsEntered)
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
      self.fund_name.textChanged.connect(self.onTextChanged)
      # although we initialize to 0, user could change this to blank, which would be invalid, but still
      # pass validator
      self.initial_units.textChanged.connect(self.onTextChanged)



  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(bool(self.initial_units.text())
                                                                      and bool(self.fund_name.text()))

  # initial units should almost never be entered if there are already purchases in the account, as this will
  # change all the unit counts that had been previously calculated. Require checking through a warning before
  # allowing this
  def initialUnitsEntered(self):
    if (float(self.initial_units.text()) > 0):
      msg_box = QMessageBox()
      msg_box.setText("You have entered an initial units value in an account that has existing fund purchases")
      msg_box.setInformativeText("If you proceed, unit values for all funds in this account"\
                                 "will change starting with the initial purchases.")
      msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
      msg_box.setDefaultButton(QMessageBox.Discard)
      if (msg_box.exec() == QMessageBox.Discard):
        self.initial_units.setText("0")







  def fundName(self):
    return self.fund_name.text()

  def initialUnits(self):
    return float(self.initial_units.text())
