# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Group2.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
