# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 13:49:54 2021

@author: David
"""

from unit_purchase_dialog import *
from datetime import date

class UnitPurchaseDialog(QtWidgets.QDialog, Ui_unitPurchaseDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.parent = parent
    self.setupUi(self)
    #populate the comboBox
    combo = self.fundSelector
    for f in self.parent.active_account.funds:
      combo.insertItem(9999, f.name, f)
    #initialize the date to today's date
    today = date.today()
    q_today = QtCore.QDate()
    q_today.setDate(today.year, today.month, today.day)
    self.purchase_date.setDate(q_today)
    #enable calendar popup
    self.purchase_date.setCalendarPopup(True)
    #get the calendar widget for checking focus
    self.calendar = self.purchase_date.calendarWidget()
    #connect date edit finished signal
    self.purchase_date.editingFinished.connect(self.checkDate)
    self.known_account_value = None
    #set the validator for purchase amount
    v = QtGui.QDoubleValidator()
    v.setBottom(0)
    v.setDecimals(2)
    self.purchaseDollars.setText("0")
    self.purchaseDollars.setValidator(v)
    # use this validator for account value as well
    self.account_value.setValidator(v)

  def date(self):
    date = self.purchase_date.date()
    return str(date.year()) + "/" + "{0:02d}".format(date.month()) + "/" + "{0:02d}".format(date.day())

  def fund(self):
    return self.fundSelector.currentData()

  def dollarsPurchased(self):
    return float(self.purchaseDollars.text())

  def accountValue(self):
    return float(self.account_value.text())

  def checkDate(self):
    if (not self.calendar.hasFocus()):
      #this is a real change for the date
      date = self.date()
      if (date in self.parent.active_account.account_values_by_date):
        print ("date found")
        self.account_value.setEnabled(False)
        self.known_account_value = self.parent.active_account.account_values_by_date[date]
        self.account_value.setText('{0:.2f}'.format(self.known_account_value.value))
      else:
        #check if account_value came from a previously known date, then blank out the edit box
        if self.known_account_value:
          self.account_value.setEnabled(True)
          self.account_value.setText('')
