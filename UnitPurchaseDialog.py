# -*- coding: utf-8 -*-


#
# Â© 2021 David Strip - david@stripfamily.net
#


from unit_purchase_dialog import *
from datetime import date, datetime
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
    self.calendar = self.purchase_date.calendarWidget()
    # Connect to calendar's clicked signal to detect when date is selected
    self.calendar.clicked.connect(self.onCalendarDateSelected)
    #is there already a purchase on today's date?
    self.checkDate()

    # set the validator for purchase amount
    v = QtGui.QDoubleValidator()
    v.setBottom(0)
    v.setDecimals(2)
    self.purchase_dollars.setValidator(v)
    # use this validator for account value as well
    self.account_value.setValidator(v)
    
    # Connect signals to validate form and enable/disable OK button
    self.purchase_dollars.textChanged.connect(self.validateForm)
    self.account_value.textChanged.connect(self.validateForm)
    
    # Initial form validation
    self.validateForm()

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

  def validateForm(self):
    """Validate form inputs and enable/disable OK button accordingly"""
    purchase_amount_valid = False
    account_value_valid = False
    
    # Check if purchase amount is valid and non-zero
    try:
      purchase_amount = float(self.purchase_dollars.text())
      purchase_amount_valid = purchase_amount > 0
    except (ValueError, TypeError):
      purchase_amount_valid = False
    
    # Check account value - either we have a known value or user entered one
    if self.known_account_value is not None:
      account_value_valid = True
    else:
      try:
        account_value = float(self.account_value.text())
        account_value_valid = account_value > 0
      except (ValueError, TypeError):
        account_value_valid = False
    
    # Enable OK button only if both values are valid
    ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
    if ok_button:
      ok_button.setEnabled(purchase_amount_valid and account_value_valid)

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
    # Use QTimer to delay the check slightly so the calendar popup has time to close
    QtCore.QTimer.singleShot(100, self.checkDate)

  def checkDate(self):
      date_str = self.date()
      
      # Check if date is older than any existing date
      latest_date = self.getLatestDate()
      if latest_date and date_str < latest_date:
          # Show warning dialog
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
              self.purchase_date.setDate(q_today)
              return
      
      # Search for an account value object with matching date
      found_account_value = None
      for account_value_obj in self.parent.active_account.account_values_by_id.values():
          if account_value_obj.date == date_str:
              found_account_value = account_value_obj
              break
      
      if found_account_value:
          print("date found")
          self.account_value.setEnabled(False)
          self.known_account_value = found_account_value
          self.account_value.setText('{0:.2f}'.format(found_account_value.value))
      else:
          self.account_value.setEnabled(True)
          self.account_value.setText('')
          self.known_account_value = None
      
      # Re-validate form after date change
      self.validateForm()