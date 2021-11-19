# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_account.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_selectAccountDialog(object):
    def setupUi(self, selectAccountDialog):
        selectAccountDialog.setObjectName("selectAccountDialog")
        selectAccountDialog.resize(648, 311)
        self.buttonBox = QtWidgets.QDialogButtonBox(selectAccountDialog)
        self.buttonBox.setGeometry(QtCore.QRect(-140, 200, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.selectAccountComboBox = QtWidgets.QComboBox(selectAccountDialog)
        self.selectAccountComboBox.setGeometry(QtCore.QRect(110, 70, 441, 71))
        self.selectAccountComboBox.setObjectName("selectAccountComboBox")

        self.retranslateUi(selectAccountDialog)
        self.buttonBox.accepted.connect(selectAccountDialog.accept)
        self.buttonBox.rejected.connect(selectAccountDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(selectAccountDialog)

    def retranslateUi(self, selectAccountDialog):
        _translate = QtCore.QCoreApplication.translate
        selectAccountDialog.setWindowTitle(_translate("selectAccountDialog", "Select Account"))

