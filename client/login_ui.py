# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\login.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self, Form):
        self.form = Form
        Form.setObjectName("Form")
        Form.resize(932, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 9, 1, 1, 1)
        self.login_btn = QtWidgets.QPushButton(Form)
        self.login_btn.setObjectName("login_btn")
        self.gridLayout.addWidget(self.login_btn, 7, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.register_btn = QtWidgets.QPushButton(Form)
        self.register_btn.setObjectName("register_btn")
        self.gridLayout.addWidget(self.register_btn, 8, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 10, 1, 1, 1)
        self.login_pass = QtWidgets.QLineEdit(Form)
        self.login_pass.setObjectName("login_pass")
        self.gridLayout.addWidget(self.login_pass, 6, 1, 1, 1)
        self.login_login = QtWidgets.QLineEdit(Form)
        self.login_login.setObjectName("login_login")
        self.gridLayout.addWidget(self.login_login, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Настройка соединения"))
        self.login_btn.setText(_translate("Form", "Sign in"))
        self.label.setText(_translate("Form", "Login"))
        self.register_btn.setText(_translate("Form", "Sign up"))
        self.label_2.setText(_translate("Form", "Password"))