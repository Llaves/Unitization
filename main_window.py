# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1893, 1386)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(460, 40, 1371, 1191))
        self.tabWidget.setObjectName("tabWidget")
        self.funds_tab = QtWidgets.QWidget()
        self.funds_tab.setObjectName("funds_tab")
        self.funds_table = QtWidgets.QTableWidget(self.funds_tab)
        self.funds_table.setGeometry(QtCore.QRect(10, 10, 1331, 1141))
        self.funds_table.setRowCount(10)
        self.funds_table.setColumnCount(3)
        self.funds_table.setObjectName("funds_table")
        self.funds_table.verticalHeader().setVisible(False)
        self.tabWidget.addTab(self.funds_tab, "")
        self.purchases_tab = QtWidgets.QWidget()
        self.purchases_tab.setObjectName("purchases_tab")
        self.purchases_table = QtWidgets.QTableWidget(self.purchases_tab)
        self.purchases_table.setGeometry(QtCore.QRect(20, 10, 1331, 1141))
        self.purchases_table.setGridStyle(QtCore.Qt.SolidLine)
        self.purchases_table.setRowCount(10)
        self.purchases_table.setColumnCount(4)
        self.purchases_table.setObjectName("purchases_table")
        self.purchases_table.verticalHeader().setVisible(False)
        self.tabWidget.addTab(self.purchases_tab, "")
        self.account_values_tab = QtWidgets.QWidget()
        self.account_values_tab.setObjectName("account_values_tab")
        self.account_values_table = QtWidgets.QTableWidget(self.account_values_tab)
        self.account_values_table.setGeometry(QtCore.QRect(10, 10, 1331, 1141))
        self.account_values_table.setRowCount(10)
        self.account_values_table.setColumnCount(2)
        self.account_values_table.setObjectName("account_values_table")
        self.account_values_table.verticalHeader().setVisible(False)
        self.tabWidget.addTab(self.account_values_tab, "")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 120, 381, 281))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(3)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 20, 281, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.account_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.account_name.setText("")
        self.account_name.setAlignment(QtCore.Qt.AlignCenter)
        self.account_name.setObjectName("account_name")
        self.verticalLayout.addWidget(self.account_name)
        self.brokerage = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.brokerage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.brokerage.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.brokerage.setLineWidth(3)
        self.brokerage.setText("")
        self.brokerage.setAlignment(QtCore.Qt.AlignCenter)
        self.brokerage.setObjectName("brokerage")
        self.verticalLayout.addWidget(self.brokerage)
        self.account_number = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.account_number.setText("")
        self.account_number.setAlignment(QtCore.Qt.AlignCenter)
        self.account_number.setObjectName("account_number")
        self.verticalLayout.addWidget(self.account_number)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1893, 38))
        self.menuBar.setObjectName("menuBar")
        self.menuAccounts = QtWidgets.QMenu(self.menuBar)
        self.menuAccounts.setObjectName("menuAccounts")
        self.menuFunds = QtWidgets.QMenu(self.menuBar)
        self.menuFunds.setObjectName("menuFunds")
        self.menuAdvanced = QtWidgets.QMenu(self.menuBar)
        self.menuAdvanced.setObjectName("menuAdvanced")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen_Account = QtWidgets.QAction(MainWindow)
        self.actionOpen_Account.setObjectName("actionOpen_Account")
        self.actionNew_Account = QtWidgets.QAction(MainWindow)
        self.actionNew_Account.setObjectName("actionNew_Account")
        self.actionNew_Fund = QtWidgets.QAction(MainWindow)
        self.actionNew_Fund.setCheckable(False)
        self.actionNew_Fund.setChecked(False)
        self.actionNew_Fund.setObjectName("actionNew_Fund")
        self.actionPurchase_Fund = QtWidgets.QAction(MainWindow)
        self.actionPurchase_Fund.setObjectName("actionPurchase_Fund")
        self.actionDelete_Fund = QtWidgets.QAction(MainWindow)
        self.actionDelete_Fund.setEnabled(False)
        self.actionDelete_Fund.setObjectName("actionDelete_Fund")
        self.actionEdit_Mode = QtWidgets.QAction(MainWindow)
        self.actionEdit_Mode.setCheckable(True)
        self.actionEdit_Mode.setChecked(False)
        self.actionEdit_Mode.setObjectName("actionEdit_Mode")
        self.actionNo_Warnings = QtWidgets.QAction(MainWindow)
        self.actionNo_Warnings.setCheckable(True)
        self.actionNo_Warnings.setObjectName("actionNo_Warnings")
        self.actionDelete_Account = QtWidgets.QAction(MainWindow)
        self.actionDelete_Account.setEnabled(False)
        self.actionDelete_Account.setObjectName("actionDelete_Account")
        self.actionEdit_Account = QtWidgets.QAction(MainWindow)
        self.actionEdit_Account.setEnabled(False)
        self.actionEdit_Account.setObjectName("actionEdit_Account")
        self.actionEdit_Fund = QtWidgets.QAction(MainWindow)
        self.actionEdit_Fund.setEnabled(False)
        self.actionEdit_Fund.setObjectName("actionEdit_Fund")
        self.actionExport_to_Excel = QtWidgets.QAction(MainWindow)
        self.actionExport_to_Excel.setEnabled(False)
        self.actionExport_to_Excel.setObjectName("actionExport_to_Excel")
        self.actionHide_Empty = QtWidgets.QAction(MainWindow)
        self.actionHide_Empty.setCheckable(True)
        self.actionHide_Empty.setObjectName("actionHide_Empty")
        self.menuAccounts.addAction(self.actionOpen_Account)
        self.menuAccounts.addAction(self.actionNew_Account)
        self.menuAccounts.addAction(self.actionEdit_Account)
        self.menuAccounts.addAction(self.actionDelete_Account)
        self.menuAccounts.addAction(self.actionExport_to_Excel)
        self.menuFunds.addAction(self.actionNew_Fund)
        self.menuFunds.addAction(self.actionPurchase_Fund)
        self.menuFunds.addAction(self.actionHide_Empty)
        self.menuAdvanced.addAction(self.actionEdit_Mode)
        self.menuAdvanced.addAction(self.actionNo_Warnings)
        self.menuBar.addAction(self.menuAccounts.menuAction())
        self.menuBar.addAction(self.menuFunds.menuAction())
        self.menuBar.addAction(self.menuAdvanced.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UnitTracker"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.funds_tab), _translate("MainWindow", "Funds"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.purchases_tab), _translate("MainWindow", "Purchases"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.account_values_tab), _translate("MainWindow", "Account Values"))
        self.label.setText(_translate("MainWindow", "Account Description"))
        self.menuAccounts.setTitle(_translate("MainWindow", "Accounts"))
        self.menuFunds.setTitle(_translate("MainWindow", "Funds"))
        self.menuAdvanced.setTitle(_translate("MainWindow", "Advanced"))
        self.actionOpen_Account.setText(_translate("MainWindow", "Open Account"))
        self.actionNew_Account.setText(_translate("MainWindow", "New Account"))
        self.actionNew_Fund.setText(_translate("MainWindow", "New Fund"))
        self.actionPurchase_Fund.setText(_translate("MainWindow", "Purchase Fund"))
        self.actionDelete_Fund.setText(_translate("MainWindow", "Delete Fund"))
        self.actionEdit_Mode.setText(_translate("MainWindow", "Edit Mode"))
        self.actionNo_Warnings.setText(_translate("MainWindow", "No Warnings"))
        self.actionDelete_Account.setText(_translate("MainWindow", "Delete Account"))
        self.actionEdit_Account.setText(_translate("MainWindow", "Edit Account"))
        self.actionEdit_Fund.setText(_translate("MainWindow", "Edit Fund"))
        self.actionExport_to_Excel.setText(_translate("MainWindow", "Export to Excel"))
        self.actionHide_Empty.setText(_translate("MainWindow", "Hide Empty"))

