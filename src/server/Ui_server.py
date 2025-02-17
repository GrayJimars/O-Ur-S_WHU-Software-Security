# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Coding\GitHub\O-Ur-S_WHU-Software-Security\src\server\server.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ServerMainWindow(object):
    def setupUi(self, ServerMainWindow):
        ServerMainWindow.setObjectName("ServerMainWindow")
        ServerMainWindow.resize(640, 480)
        ServerMainWindow.setMinimumSize(QtCore.QSize(640, 480))
        ServerMainWindow.setMaximumSize(QtCore.QSize(640, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ServerMainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ServerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 641, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label0 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label0.setObjectName("label0")
        self.horizontalLayout_2.addWidget(self.label0)
        self.serverState = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.serverState.setText("")
        self.serverState.setObjectName("serverState")
        self.horizontalLayout_2.addWidget(self.serverState)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.startServer = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startServer.setObjectName("startServer")
        self.horizontalLayout_6.addWidget(self.startServer)
        self.stopServer = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopServer.setObjectName("stopServer")
        self.horizontalLayout_6.addWidget(self.stopServer)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.ipInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ipInput.setObjectName("ipInput")
        self.horizontalLayout.addWidget(self.ipInput)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.portInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.portInput.setObjectName("portInput")
        self.horizontalLayout.addWidget(self.portInput)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        ServerMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ServerMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerMainWindow)

    def retranslateUi(self, ServerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerMainWindow.setWindowTitle(_translate("ServerMainWindow", "服务器（被控端）"))
        self.label0.setText(_translate("ServerMainWindow", "服务器状态："))
        self.startServer.setText(_translate("ServerMainWindow", "开始"))
        self.stopServer.setText(_translate("ServerMainWindow", "停止"))
        self.label_2.setText(_translate("ServerMainWindow", "地址"))
        self.ipInput.setText(_translate("ServerMainWindow", "localhost"))
        self.label_3.setText(_translate("ServerMainWindow", "端口"))
        self.portInput.setText(_translate("ServerMainWindow", "25566"))
        self.label.setText(_translate("ServerMainWindow", "日志"))
import server_rc
