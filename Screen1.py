# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Entrada.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import time

nome = None
class screen1(object):
    def setupUi(self, MainWindow):
    
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(414, 128)
        self.my_window = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(40, 50, 251, 31))
        self.textEdit.setObjectName("textEdit")
        self.Entrar = QtWidgets.QPushButton(MainWindow)
        self.Entrar.setGeometry(QtCore.QRect(290, 50, 75, 31))
        self.Entrar.setObjectName("Entrar")
        self.name = None
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Entrar.setText(_translate("MainWindow", "Entrar"))
        self.Entrar.clicked.connect(self.input_name)

    def input_name(self):
        self.name= self.textEdit.toPlainText()
        
        if len(self.name) != 0:
            self.my_window.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = screen1()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    nome = ui.name
    print(nome)
    