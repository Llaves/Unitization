# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_purchase_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_unitPurchaseDialog(object):
    def setupUi(self, unitPurchaseDialog):
        unitPurchaseDialog.setObjectName("unitPurchaseDialog")
        unitPurchaseDialog.resize(704, 408)
        self.buttonBox = QtWidgets.QDialogButtonBox(unitPurchaseDialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 300, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(unitPurchaseDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 581, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.fundSelector = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.fundSelector.setObjectName("fundSelector")
        self.horizontalLayout_3.addWidget(self.fundSelector)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.purchase_date = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.purchase_date.sizePolicy().hasHeightForWidth())
        self.purchase_date.setSizePolicy(sizePolicy)
        self.purchase_date.setObjectName("purchase_date")
        self.horizontalLayout_2.addWidget(self.purchase_date)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(unitPurchaseDialog)
        self.buttonBox.accepted.connect(unitPurchaseDialog.accept)
        self.buttonBox.rejected.connect(unitPurchaseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(unitPurchaseDialog)

    def retranslateUi(self, unitPurchaseDialog):
        _translate = QtCore.QCoreApplication.translate
        unitPurchaseDialog.setWindowTitle(_translate("unitPurchaseDialog", "Purchase Units"))
        self.label.setText(_translate("unitPurchaseDialog", "Fund Name"))
        self.label_2.setText(_translate("unitPurchaseDialog", "Purchase Date"))
        self.label_3.setText(_translate("unitPurchaseDialog", "Dollars invested"))

