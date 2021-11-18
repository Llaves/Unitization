# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_account_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddAccountDialog(object):
    def setupUi(self, AddAccountDialog):
        AddAccountDialog.setObjectName("AddAccountDialog")
        AddAccountDialog.resize(930, 480)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddAccountDialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 380, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(AddAccountDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(170, 80, 611, 221))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.acct_name_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.acct_name_edit.setObjectName("acct_name_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.acct_name_edit)
        self.brokerage_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.brokerage_edit.setObjectName("brokerage_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.brokerage_edit)
        self.account_number_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.account_number_edit.setObjectName("account_number_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.account_number_edit)

        self.retranslateUi(AddAccountDialog)
        self.buttonBox.accepted.connect(AddAccountDialog.accept)
        self.buttonBox.rejected.connect(AddAccountDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddAccountDialog)

    def retranslateUi(self, AddAccountDialog):
        _translate = QtCore.QCoreApplication.translate
        AddAccountDialog.setWindowTitle(_translate("AddAccountDialog", "Add Account"))
        self.label.setText(_translate("AddAccountDialog", "Account Name"))
        self.label_2.setText(_translate("AddAccountDialog", "Brokerage"))
        self.label_3.setText(_translate("AddAccountDialog", "Account Number"))

