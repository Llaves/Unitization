# -*- coding: utf-8 -*-

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
Created on Thu Nov 18 11:53:31 2021

@author: David
"""

from add_account_dialog import *
from db_objects import Account
from copy import copy

class AddAccountDialog(QtWidgets.QDialog, Ui_AddAccountDialog):
  def __init__(self, parent, edit_mode = False, old_account = None):
    QtWidgets.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.btn_save = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
    self.btn_save.setEnabled(False)
    self.account_number.textChanged.connect(self.onTextChanged)
    self.acct_name.textChanged.connect(self.onTextChanged)
    self.brokerage.textChanged.connect(self.onTextChanged)
    self.parent = parent
    self.edit_mode = edit_mode
    self.old_account = copy(old_account)

    # Get all existing account names from the parent's database object
    self.account_names = [a.name for a in self.parent.accounts]


    if self.edit_mode:
      self.acct_name.setText(self.old_account.name)
      self.brokerage.setText(self.old_account.brokerage)
      self.account_number.setText(self.old_account.account_no)
      self.setWindowTitle("Edit current account")
      # In edit mode, don't check against the account's current name
      if self.old_account.name in self.account_names:
        self.account_names.remove(self.old_account.name)

    # Hide the warning label by default
    self.duplicate_account_warning.setVisible(False)

  @QtCore.pyqtSlot()
  def onTextChanged(self):
    # Check if the entered account name already exists
    name_is_duplicate = self.acct_name.text() in self.account_names
    
    # Show or hide the warning label based on whether the name is a duplicate
    self.duplicate_account_warning.setVisible(name_is_duplicate)
    
    # Check that all text fields have content
    all_fields_filled = (bool(self.account_number.text())
                              and bool(self.acct_name.text())
                              and bool(self.brokerage.text()))
    
    # The save button is enabled only if all fields are filled AND the name is unique
    self.btn_save.setEnabled(all_fields_filled and not name_is_duplicate)
    
  def accept(self):
    self.account = Account(0, self.acct_name.text(), self.brokerage.text(), self.account_number.text())
    if self.edit_mode:
      self.account.id = self.old_account.id
    QtWidgets.QDialog.accept(self)
