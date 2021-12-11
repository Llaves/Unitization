# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#


"""
Created on Sat Nov 20 15:42:13 2021

@author: David
"""

from add_fund import *
from PyQt5.QtWidgets import QMessageBox
from db_objects import Fund
from copy import copy

class AddFundDialog(QtWidgets.QDialog, Ui_addFund):
  def __init__(self, parent, edit_mode = False, old_fund = None):
      QtWidgets.QDialog.__init__(self, parent)
      self.parent = parent
      self.setupUi(self)
      self.edit_mode = edit_mode
      self.old_fund = copy(old_fund)

      # set validator to doubles, three decimal places, greater than zero
      v = QtGui.QDoubleValidator()
      v.setBottom(0)
      v.setDecimals(3)
      self.initial_units.setText("0")
      v.setNotation(QtGui.QDoubleValidator.StandardNotation)
      self.initial_units.setValidator(v)
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
      self.fund_name.textChanged.connect(self.onTextChanged)
      # although we initialize to 0, user could change this to blank, which would be invalid, but still
      # pass validator
      self.initial_units.textChanged.connect(self.onTextChanged)
      self.delete_fund.hide()
      self.delete_fund.stateChanged.connect(self.onCheckChange)
      self.buttonBox.accepted.connect(self.initialUnitsCheck)
      self.buttonBox.accepted.disconnect(self.accept)

      if self.edit_mode:
        self.fund_name.setText(self.old_fund.name)
        self.initial_units.setText(str(self.old_fund.initial_units))
        self.setWindowTitle("Edit Fund")
        self.delete_fund.show()




  @QtCore.pyqtSlot()
  def onTextChanged(self):
    self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(bool(self.initial_units.text())
                                                                      and bool(self.fund_name.text()))

  # initial units should almost never be entered if there are already purchases in the account, as this will
  # change all the unit counts that had been previously calculated. Require checking through a warning before
  # allowing this
  def initialUnitsCheck(self):
    if ((((not self.edit_mode) and (float(self.initial_units.text()) > 0)
          and (len(self.parent.active_account.purchases) > 0)) or
         (self.edit_mode and (float(self.initial_units.text()) != self.old_fund.initial_units)))
        and self.parent.warnings_enabled):
      msg_box = QMessageBox()
      if self.edit_mode:
        msg_box.setText("You have changed the initial units value in an existing fund")
      else:
        msg_box.setText("You have entered an initial units value in an account that has existing fund purchases")
      msg_box.setInformativeText("If you proceed, unit values for all funds in this account "\
                                  "will change starting with the initial purchases.")
      msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
      msg_box.setDefaultButton(QMessageBox.Discard)
      msg_box.setWindowTitle("UnitTracker Warning")
      if (msg_box.exec() == QMessageBox.Discard):
        self.initial_units.setText("0")
        return

    self.fund = Fund(0, self.fundName(), self.initialUnits(), self.parent.active_account.id)
    if self.edit_mode:
      self.fund.id = self.old_fund.id
    QtWidgets.QDialog.accept(self)



  def onCheckChange(self):
    if self.delete_fund.isChecked():
      self.fund_name.setEnabled(False)
      self.initial_units.setEnabled(False)
    else:
      self.fund_name.setEnabled(True)
      self.initial_units.setEnabled(True)

  def delete(self):
    return self.delete_fund.isChecked()

  def fundName(self):
    return self.fund_name.text()

  def initialUnits(self):
    return float(self.initial_units.text())

  def initialUnitsChanged(self):
    return self.old_fund.initial_units != self.initialUnits()
