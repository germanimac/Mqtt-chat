# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)
class screen2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(576, 233)
        self.Botaogrupo = QtWidgets.QRadioButton(Dialog)
        self.Botaogrupo.setGeometry(QtCore.QRect(190, 120, 81, 17))
        self.Botaogrupo.setObjectName("Botaogrupo")
        self.BotaoPrivado = QtWidgets.QRadioButton(Dialog)
        self.BotaoPrivado.setGeometry(QtCore.QRect(320, 120, 82, 17))
        self.BotaoPrivado.setObjectName("BotaoPrivado")
        self.enviar = QtWidgets.QPushButton(Dialog)
        self.enviar.setGeometry(QtCore.QRect(210, 160, 161, 31))
        self.enviar.setObjectName("enviar")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 70, 521, 31))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Botaogrupo.setText(_translate("Dialog", "Grupo"))
        self.BotaoPrivado.setText(_translate("Dialog", "Privado"))
        self.enviar.setText(_translate("Dialog", "Enviar"))
        self.textEdit.setPlaceholderText(_translate("Dialog", "Nome de Pessoa ou Grupo"))
        

class screen3(object):
    def __init__(self, nome=""):
        self.name=nome
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.w = None
        #Dialog.setObjectName("Dialog")
        MainWindow.resize(774, 461)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(20, 370, 581, 71))
        self.textEdit.setObjectName("textEdit")
        self.Grupos = QtWidgets.QPushButton(MainWindow)
        self.Grupos.setGeometry(QtCore.QRect(630, 320, 121, 31))
        self.Grupos.setObjectName("Grupos")
        self.Envio = QtWidgets.QPushButton(MainWindow)
        self.Envio.setGeometry(QtCore.QRect(630, 370, 121, 71))
        self.Envio.setObjectName("Envio")
        self.scrollArea = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea.setGeometry(QtCore.QRect(20, 19, 581, 331))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 579, 329))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.listView = QtWidgets.QListView(MainWindow)
        self.listView.setGeometry(QtCore.QRect(630, 21, 121, 291))
        self.listView.setObjectName("listView")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("MainWindow", ("Olá " + self.name)))
        self.Grupos.setText(_translate("MainWindow", "Adicionar"))
        self.Grupos.clicked.connect(self.adicionar)
        self.Envio.setText(_translate("MainWindow", "Enviar"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Digite a mensagem que deseja enviar"))

    def adicionar(self):
        
        Dialog.show()
        #self.w.show()
        
        

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = screen3()
    ui.setupUi(MainWindow)
    Dialog = QtWidgets.QDialog()
    w = screen2()
    w.setupUi(Dialog)
    MainWindow.show()
    app.exec_()
