# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'account_value_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_accountValueDialog(object):
    def setupUi(self, accountValueDialog):
        accountValueDialog.setObjectName("accountValueDialog")
        accountValueDialog.resize(684, 268)
        self.buttonBox = QtWidgets.QDialogButtonBox(accountValueDialog)
        self.buttonBox.setGeometry(QtCore.QRect(-130, 190, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(accountValueDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 30, 581, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.account_date = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_date.sizePolicy().hasHeightForWidth())
        self.account_date.setSizePolicy(sizePolicy)
        self.account_date.setKeyboardTracking(False)
        self.account_date.setObjectName("account_date")
        self.horizontalLayout_2.addWidget(self.account_date)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.account_value = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.account_value.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_value.sizePolicy().hasHeightForWidth())
        self.account_value.setSizePolicy(sizePolicy)
        self.account_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.account_value.setObjectName("account_value")
        self.horizontalLayout.addWidget(self.account_value)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(accountValueDialog)
        self.buttonBox.accepted.connect(accountValueDialog.accept)
        self.buttonBox.rejected.connect(accountValueDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(accountValueDialog)

    def retranslateUi(self, accountValueDialog):
        _translate = QtCore.QCoreApplication.translate
        accountValueDialog.setWindowTitle(_translate("accountValueDialog", "Add Account Value"))
        self.label_2.setText(_translate("accountValueDialog", "Date"))
        self.label_4.setText(_translate("accountValueDialog", "Account Value"))

