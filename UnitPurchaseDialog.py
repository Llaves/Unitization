# -*- coding: utf-8 -*-


#
# © 2021 David Strip - david@stripfamily.net
#


from unit_purchase_dialog import *
from datetime import date
from copy import copy

class UnitPurchaseDialog(QtWidgets.QDialog, Ui_unitPurchaseDialog):
  def __init__(self, parent, edit_mode = False, unit_purchase = None):
    QtWidgets.QDialog.__init__(self, parent)

    self.parent = parent
    self.known_account_value = None
    self.edit_mode = edit_mode
    self.old_purchase = copy(unit_purchase)

    self.setupUi(self)

    if self.edit_mode:
      self.setWindowTitle("Edit Purchase")
      self.delete_purchase.show()
      fund = [f for f in self.parent.active_account.funds if f.id == self.old_purchase.fund_id][0]
      self.fund_selector.insertItem(9999, fund.name, fund)
      self.fund_selector.setEnabled(False)
      self.purchase_dollars.setText("%.2f" % (self.old_purchase.amount))
      d = self.parent.active_account.account_values_by_id[self.old_purchase.date_id].date
      old_date = QtCore.QDate()
      old_date.setDate(int(d[0:4]), int(d[5:7]), int(d[8:10]))
      self.purchase_date.setDate(old_date)
    else:
      self.delete_purchase.hide()
      self.purchase_dollars.setText("0")
      # populate the comboBox
      combo = self.fund_selector
      for f in self.parent.active_account.funds:
        combo.insertItem(9999, f.name, f)
      # initialize the date to today's date
      today = date.today()
      q_today = QtCore.QDate()
      q_today.setDate(today.year, today.month, today.day)
      self.purchase_date.setDate(q_today)


    # enable calendar popup
    self.purchase_date.setCalendarPopup(True)
    # connect date edit finished signal
    # keyboard tracking is disable in designer file so that signal occurs only on loss of focus
    self.purchase_date.editingFinished.connect(self.checkDate)
    self.calendar = self.purchase_date.calendarWidget()
    #is there already a purchase on today's date?
    self.checkDate()

    # set the validator for purchase amount
    v = QtGui.QDoubleValidator()
    v.setBottom(0)
    v.setDecimals(2)
    self.purchase_dollars.setValidator(v)
    # use this validator for account value as well
    self.account_value.setValidator(v)

  def date(self):
    date = self.purchase_date.date()
    return str(date.year()) + "/" + "{0:02d}".format(date.month()) + "/" + "{0:02d}".format(date.day())

  def fund(self):
    return self.fund_selector.currentData()

  def dollarsPurchased(self):
    return float(self.purchase_dollars.text())

  def accountValueDollars(self):
    return float(self.account_value.text())

  def knownAccountValueObj(self):
    return self.known_account_value

  def delete(self):
    return self.delete_purchase.isChecked()

  def checkDate(self):
    if not self.calendar.hasFocus():
    #this is a real change for the date
      date = self.date()
      #check if there is an entry for this date
      if (date in self.parent.active_account.account_values_by_id):
        print ("date found")
        self.account_value.setEnabled(False)
        self.known_account_value = self.parent.active_account.account_values_by_id[date]
        self.account_value.setText('{0:.2f}'.format(self.known_account_value.value))
      else:
        self.account_value.setEnabled(True)
        self.account_value.setText('')
        # clear known_account_value
        self.known_account_value = None
