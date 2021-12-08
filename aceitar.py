from PyQt5 import QtCore, QtGui, QtWidgets


class solicitacao(object):
    def setupUi(self, Dialog, nome):
        self.nome =nome
        self.resposta =""
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 139)
        self.BotoAceitar = QtWidgets.QPushButton(Dialog)
        self.BotoAceitar.setGeometry(QtCore.QRect(60, 80, 75, 23))
        self.BotoAceitar.setObjectName("BotoAceitar")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(50, 10, 301, 51))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("border: 0px ;")
        self.label = QtWidgets.QLabel()             #caixa de mensagem
        self.label.setGeometry(QtCore.QRect(0, 0, 299, 49))   #caixa de mensagem            
        self.label.setObjectName("textEdit") 
        self.Dialog = Dialog
        #self.scrollAreaWidgetContents = QtWidgets.QWidget()
        #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 299, 49))
        #self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.label)
        self.Negar = QtWidgets.QPushButton(Dialog)
        self.Negar.setGeometry(QtCore.QRect(270, 80, 75, 23))
        self.Negar.setObjectName("Negar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BotoAceitar.setText(_translate("Dialog", "Aceitar"))
        self.Negar.setText(_translate("Dialog", "Negar"))
        self.label.setText('<div align="center"><b ><span>'+self.nome+'</span> deseja conversar com você</b></div>')
        self.BotoAceitar.clicked.connect(self._aceitar)
        self.Negar.clicked.connect(self._negar)

    def _aceitar(self):
        self.resposta ="aceitar"
        self.Dialog.close()
    def _negar(self):
        self.resposta = "negar"
        self.Dialog.close()

