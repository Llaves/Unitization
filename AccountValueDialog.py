# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#

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
    # connect date edit finished signal
    # keyboard tracking is disable in designer file so that signal occurs only on loss of focus
    self.account_date.editingFinished.connect(self.checkDate)
    self.calendar = self.account_date.calendarWidget()
    #is there already a purchase on today's date?
    self.checkDate()

    if self.edit_mode:
      self.account_value.setText("%.2f" % (self.old_account_value.value))
      the_date = self.old_account_value.date
      q_today = QtCore.QDate()
      q_today.setDate(int(the_date[0:4]), int(the_date[5:7]), int(the_date[8:10]))
      self.account_date.setDate(q_today)
      self.account_date.setEnabled(False)
      self.setWindowTitle("Edit Fund")
    else:
      # initialize the date to today's date
      today = date.today()
      q_today = QtCore.QDate()
      q_today.setDate(today.year, today.month, today.day)
      self.account_date.setDate(q_today)




  def checkBlank(self):
    if (self.account_value.text() != ""):
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
    else:
      self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

  def date(self):
    date = self.account_date.date()
    return str(date.year()) + "/" + "{0:02d}".format(date.month()) + "/" + "{0:02d}".format(date.day())

  def accountValueDollars(self):
    return float(self.account_value.text())


  def checkDate(self):
    if not self.calendar.hasFocus():
    #this is a real change for the date
      print ("checkDate called")
      date = self.date()
      if (date in self.parent.active_account.account_values_by_id):
        print ("date found")
        self.account_value.setEnabled(False)
        self.known_account_value = self.parent.active_account.account_values_by_id[date]
        self.account_value.setText('{0:.2f}'.format(self.known_account_value.value))
        self.account_value.setToolTip("Value exists for this date. Use edit if you want to change it")
      else:
        #check if account_value came from a previously known date, then blank out the edit box
        if self.known_account_value:
          self.account_value.setEnabled(True)
          self.account_value.setText('')
          # clear known_account_value
          self.known_account_value = None
          self.account_value.setToolTip("")
