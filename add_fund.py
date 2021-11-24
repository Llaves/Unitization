# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_fund.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addFund(object):
    def setupUi(self, addFund):
        addFund.setObjectName("addFund")
        addFund.resize(621, 271)
        self.buttonBox = QtWidgets.QDialogButtonBox(addFund)
        self.buttonBox.setGeometry(QtCore.QRect(-130, 180, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(addFund)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 30, 481, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.fund_name = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.fund_name.setObjectName("fund_name")
        self.horizontalLayout_3.addWidget(self.fund_name)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.initial_units = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initial_units.sizePolicy().hasHeightForWidth())
        self.initial_units.setSizePolicy(sizePolicy)
        self.initial_units.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.initial_units.setObjectName("initial_units")
        self.horizontalLayout_4.addWidget(self.initial_units)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(addFund)
        self.buttonBox.accepted.connect(addFund.accept)
        self.buttonBox.rejected.connect(addFund.reject)
        QtCore.QMetaObject.connectSlotsByName(addFund)

    def retranslateUi(self, addFund):
        _translate = QtCore.QCoreApplication.translate
        addFund.setWindowTitle(_translate("addFund", "Add Fund"))
        self.label.setText(_translate("addFund", "Fund Name"))
        self.label_2.setText(_translate("addFund", "Initial Units"))

