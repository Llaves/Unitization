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
        MainWindow.resize(1893, 1367)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(90, 70, 1711, 1191))
        self.tabWidget.setObjectName("tabWidget")
        self.funds_tab = QtWidgets.QWidget()
        self.funds_tab.setObjectName("funds_tab")
        self.funds_table = QtWidgets.QTableWidget(self.funds_tab)
        self.funds_table.setGeometry(QtCore.QRect(20, 30, 1331, 1141))
        self.funds_table.setRowCount(10)
        self.funds_table.setColumnCount(3)
        self.funds_table.setObjectName("funds_table")
        self.funds_table.verticalHeader().setVisible(False)
        self.tabWidget.addTab(self.funds_tab, "")
        self.purchases_tab = QtWidgets.QWidget()
        self.purchases_tab.setObjectName("purchases_tab")
        self.tabWidget.addTab(self.purchases_tab, "")
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
        self.menuPurchases = QtWidgets.QMenu(self.menuBar)
        self.menuPurchases.setObjectName("menuPurchases")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen_Account = QtWidgets.QAction(MainWindow)
        self.actionOpen_Account.setObjectName("actionOpen_Account")
        self.actionNew_Account = QtWidgets.QAction(MainWindow)
        self.actionNew_Account.setObjectName("actionNew_Account")
        self.actionNew_Fund = QtWidgets.QAction(MainWindow)
        self.actionNew_Fund.setObjectName("actionNew_Fund")
        self.actionPurchase_Fund = QtWidgets.QAction(MainWindow)
        self.actionPurchase_Fund.setObjectName("actionPurchase_Fund")
        self.menuAccounts.addAction(self.actionOpen_Account)
        self.menuAccounts.addAction(self.actionNew_Account)
        self.menuFunds.addAction(self.actionNew_Fund)
        self.menuFunds.addAction(self.actionPurchase_Fund)
        self.menuBar.addAction(self.menuAccounts.menuAction())
        self.menuBar.addAction(self.menuFunds.menuAction())
        self.menuBar.addAction(self.menuPurchases.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UnitTracker"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.funds_tab), _translate("MainWindow", "Funds"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.purchases_tab), _translate("MainWindow", "Purchases"))
        self.menuAccounts.setTitle(_translate("MainWindow", "Accounts"))
        self.menuFunds.setTitle(_translate("MainWindow", "Funds"))
        self.menuPurchases.setTitle(_translate("MainWindow", "Purchases"))
        self.actionOpen_Account.setText(_translate("MainWindow", "Open Account"))
        self.actionNew_Account.setText(_translate("MainWindow", "New Account"))
        self.actionNew_Fund.setText(_translate("MainWindow", "New Fund"))
        self.actionPurchase_Fund.setText(_translate("MainWindow", "Purchase Fund"))

