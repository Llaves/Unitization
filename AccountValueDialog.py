# -*- coding: utf-8 -*-

#  © Copyright 2021 David Strip - david@stripfamily.net

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Created on Tue Nov 30 15:33:16 2021

@author: David
"""

from account_value_dialog import *
from PyQt5.QtWidgets import QMessageBox
from db_objects import AccountValue
from copy import copy
from datetime import date

class AccountValueDialog(QtWidgets.QDialog, Ui_accountValueDialog):
  def __init__(self, parent, edit_mode = False, old_account_value = None):
    QtWidgets.QDialog.__init__(self, parent)

    self.parent = parent
    self.setupUi(self)
    self.edit_mode = edit_mode
    self.old_account_value = copy(old_account_value)
    self.known_account_value = None

    # set validator to doubles, two decimal places, greater than zero
    v = QtGui.QDoubleValidator()
    v.setBottom(0)
    v.setDecimals(2)
    v.setNotation(QtGui.QDoubleValidator.StandardNotation)
    self.account_value.setText("0")
    self.account_value.setValidator(v)
    self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
    self.account_value.textChanged.connect(self.checkBlank)

    # enable calendar popup
    self.account_date.setCalendarPopup(True)
    self.calendar = self.account_date.calendarWidget()
    # connect calendar click to delayed date check
    self.calendar.clicked.connect(self.onCalendarDateSelected)

    if self.edit_mode:
      self.account_value.setText("%.2f" % (self.old_account_value.value))
      the_date = self.old_account_value.date
      q_today = QtCore.QDate()
      q_today.setDate(int(the_date[0:4]), int(the_date[5:7]), int(the_date[8:10]))
      self.account_date.setDate(q_today)
      self.account_date.setEnabled(False)
      self.setWindowTitle("Edit Account Value")
    else:
      # initialize the date to today's date
      today = date.today()
      q_today = QtCore.QDate()
      q_today.setDate(today.year, today.month, today.day)
      self.account_date.setDate(q_today)
      # initial validation of today's date
      self.checkDate()

  def checkBlank(self):
    if (self.account_value.text() != ""):
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
    else:
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

  def date(self):
    date_obj = self.account_date.date()
    return str(date_obj.year()) + "/" + "{0:02d}".format(date_obj.month()) + "/" + "{0:02d}".format(date_obj.day())

  def accountValueDollars(self):
    return float(self.account_value.text())

  def getLatestDate(self):
    """Get the latest date from existing account values"""
    if not self.parent.active_account.account_values_by_id:
      return None

    latest_date_str = None
    for account_value_obj in self.parent.active_account.account_values_by_id.values():
      if latest_date_str is None or account_value_obj.date > latest_date_str:
        latest_date_str = account_value_obj.date

    return latest_date_str

  def onCalendarDateSelected(self, selected_date):
    """Handle date selection from calendar popup"""
    QtCore.QTimer.singleShot(100, self.checkDate)

  def checkDate(self):
    date_str = self.date()

    # First check if an account value already exists for this date
    found_account_value = None
    for account_value_obj in self.parent.active_account.account_values_by_id.values():
      if account_value_obj.date == date_str:
        found_account_value = account_value_obj
        break

    if found_account_value:
      self.account_value.setEnabled(False)
      self.known_account_value = found_account_value
      self.account_value.setText('{0:.2f}'.format(found_account_value.value))
      self.account_value.setToolTip("Value exists for this date. Use edit if you want to change it")
      #disable OK button if in add mode
      if not self.edit_mode:
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
      return  # stop here if date is already taken

    # If no value exists for this date, then check if it's older than the latest
    latest_date = self.getLatestDate()
    if latest_date and date_str < latest_date:
      msg = QtWidgets.QMessageBox()
      msg.setIcon(QtWidgets.QMessageBox.Warning)
      msg.setWindowTitle("Date Warning")
      msg.setText(f"Warning: The selected date ({date_str}) is older than the latest existing date ({latest_date}).")
      msg.setInformativeText("This may cause issues with your account history. Do you want to continue?")
      msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
      msg.setDefaultButton(QtWidgets.QMessageBox.No)

      result = msg.exec_()
      if result == QtWidgets.QMessageBox.No:
        # Reset to today's date
        today = date.today()
        q_today = QtCore.QDate()
        q_today.setDate(today.year, today.month, today.day)
        self.account_date.setDate(q_today)
        return

    # If we reach here, it's a valid new date with no conflicts
    self.account_value.setEnabled(True)
    self.account_value.setText('')
    self.known_account_value = None
    self.account_value.setToolTip("")

