# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete_fund.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FundDeleteDialog(object):
    def setupUi(self, FundDeleteDialog):
        FundDeleteDialog.setObjectName("FundDeleteDialog")
        FundDeleteDialog.resize(640, 265)
        self.buttonBox = QtWidgets.QDialogButtonBox(FundDeleteDialog)
        self.buttonBox.setGeometry(QtCore.QRect(-140, 190, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.fund_to_delete = QtWidgets.QComboBox(FundDeleteDialog)
        self.fund_to_delete.setGeometry(QtCore.QRect(290, 40, 281, 31))
        self.fund_to_delete.setObjectName("fund_to_delete")
        self.label = QtWidgets.QLabel(FundDeleteDialog)
        self.label.setGeometry(QtCore.QRect(90, 40, 161, 25))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FundDeleteDialog)
        self.label_2.setGeometry(QtCore.QRect(150, 110, 321, 71))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(FundDeleteDialog)
        self.buttonBox.rejected.connect(FundDeleteDialog.reject)
        self.buttonBox.accepted.connect(FundDeleteDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(FundDeleteDialog)

    def retranslateUi(self, FundDeleteDialog):
        _translate = QtCore.QCoreApplication.translate
        FundDeleteDialog.setWindowTitle(_translate("FundDeleteDialog", "Delete Fund"))
        self.label.setText(_translate("FundDeleteDialog", "Fund to Delete"))
        self.label_2.setText(_translate("FundDeleteDialog", "Click Yes to delete this fund, otherwise click cancel"))

