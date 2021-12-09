from PyQt5 import QtCore, QtGui, QtWidgets
from message_struct import Chat_mqtt
from Screen1 import screen1
from Screen2 import screen2
from aceitar import solicitacao
#from Screen3 import screen3
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from kafka.admin import client
import paho.mqtt.client as mqtt
import time
from mensagens import mensagens
import threading
import time
from kafka import KafkaConsumer
from json import loads
import sqlite3 

import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMainWindow, QLabel
from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QTextDocument, QTextOption
from PyQt5.QtCore import QThread
# from PyQt5.QtGui import
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
    
)

#cur.execute("INSERT INTO stocks VALUES (?, ?, ?)",("leo","joao", "hahahaha lalal"))
USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#90caf9", USER_THEM: "#a5d6a7"}


USER_TRANSLATE = {USER_ME: QPoint(20, 0), USER_THEM: QPoint(0, 0)}

BUBBLE_PADDING = QMargins(15, 5, 35, 5)
TEXT_PADDING = QMargins(25, 15, 45, 15)



class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    _font = None

    def paint(self, painter, option, index):
        painter.save()
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.
        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from the top left/right.
        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20))

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # draw the text
        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        textrect.setHeight(doc.size().height())
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    def run(self):
        """Long-running task."""
        print(cliente.nome)
        message_payload = None
        for message in cliente.consumer:
            message_payload = str(message.value.decode("utf-8"))
            self.progress.emit((message_payload))
        self.finished.emit()

class screen3(object):
    def __init__(self, user):
        self.name=user.nome
        self.dest =""
        self.user=user
        self.tipo_conversa =""
        self.contatos = []
    def setupUi(self, MainWindow): #screen 3

        MainWindow.setObjectName("MainWindow")              #tela principal            
        MainWindow.resize(800, 461)                         #tela principal
        self.centralwidget = QtWidgets.QWidget(MainWindow)  #tela principal                        
        self.centralwidget.setObjectName("centralwidget")   #tela principal                            

        
        self.textEdit = QtWidgets.QTextEdit(MainWindow)             #caixa de mensagem
        self.textEdit.setGeometry(QtCore.QRect(20, 370, 581, 71))   #caixa de mensagem            
        self.textEdit.setObjectName("textEdit")                     #caixa de mensagem                

        self.Grupos = QtWidgets.QPushButton(MainWindow)             #botao adicionar                            
        self.Grupos.setGeometry(QtCore.QRect(630, 320, 121, 31))    #botao adicionar                        
        self.Grupos.setObjectName("Grupos")                         #botao adicionar

        self.Envio = QtWidgets.QPushButton(MainWindow)               #botao enviar                         
        self.Envio.setGeometry(QtCore.QRect(630, 370, 121, 71))      #botao enviar                    
        self.Envio.setObjectName("Envio")                            #botao enviar

        
        

        
        self.scrollArea = QtWidgets.QScrollArea(MainWindow)         #Area de Mensagens                    
        self.scrollArea.setGeometry(QtCore.QRect(20, 19, 581, 331)) #Area de Mensagens                
        self.scrollArea.setWidgetResizable(True)                    #Area de Mensagens
        self.scrollArea.setObjectName("scrollArea")                 #Area de Mensagens
        
        self.messages = QListView()                                # mensagens                                     
        self.messages.setGeometry(QtCore.QRect(0, 0, 579, 329))    # mensagens                             
        self.messages.setItemDelegate(MessageDelegate())           # mensagens                         
        self.model = MessageModel()                                # mensagens 
        self.messages.setModel(self.model)

        #self.scrollArea.setWidget(self.messages)                    
    
        
        self.listWidget = QtWidgets.QListWidget(MainWindow)
        self.listWidget.setGeometry(QtCore.QRect(630, 21, 150, 291))
        self.listWidget.setObjectName("listWidget")
        index = 0

        self.retranslateUi(MainWindow, self.user)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    def retranslateUi(self, Dialog, cliente):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("MainWindow", ("Olá " + self.name))) #Titulo 

        self.Grupos.setText(_translate("MainWindow", "Adicionar")) #Define texto
        self.Grupos.clicked.connect(self.adicionar)                 #click chama metodo adicionar

        self.Envio.setText(_translate("MainWindow", "Enviar")) #Define texto
        self.Envio.clicked.connect(self.enviar)                 #click chama metodo enviar

        self.textEdit.setPlaceholderText(_translate("MainWindow", "Digite a mensagem que deseja enviar")) #define placeholder 
        self.runLongTask()  # chama metodo

        self.listWidget.itemSelectionChanged.connect(self.selectionChanged) 
        
    
    def rolagem(self):
        print("rolou")
        lambda x,y: self.bar.setValue(0)
    def selectionChanged(self):
        widget = self.scrollArea.takeWidget()
        self.messages = QListView()                                # mensagens                                     
        self.messages.setGeometry(QtCore.QRect(0, 0, 579, 329))    # mensagens                             
        self.messages.setItemDelegate(MessageDelegate())           # mensagens                         
        self.model = MessageModel()                                # mensagens 
        self.messages.setModel(self.model)
        self.scrollArea.setWidget(self.messages)
        contato = [item.text() for item in self.listWidget.selectedItems()]
        print(contato[0])
        self.dest =contato[0]
        if contato[0] in self.user.grupos:
            self.user.novo_chat(contato[0],"grupo")
            self.tipo_conversa = "grupo"
            for row in cur.execute("SELECT * FROM stocks WHERE dest =:dd",{"dd":self.dest}):
                print(row)
                if row[0] != self.name:
                    self.model.add_message(USER_THEM,"("+row[0]+")\n" +row[2])
                else:
                    self.model.add_message(USER_ME, row[2])
        else:
            self.user.novo_chat(contato[0],"privado")
            self.tipo_conversa = "privado"
            print("aqui")
            for row in cur.execute("SELECT * FROM stocks WHERE (dest =:dd AND remetente =:rr) OR (dest =:df AND remetente =:rf)",{"dd":self.name, "rr":self.dest,"df":self.dest, "rf":self.name}):
                print(row)
                if row[0] != self.name:
                    self.model.add_message(USER_THEM,row[2])
                else:
                    self.model.add_message(USER_ME, row[2])
        
        
            


        
    def runLongTask(self): #este método é responsável por criar e executar a thread consumidora do kafka
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
           
    def reportProgress(self, message): #metodo que le informações consumidas do kafka
        message_payload =message.split(",")
        print(message_payload )
        del message_payload[0]
        del message_payload[-1]
        
        if int(message_payload[0]) == 5:
                ui.setupUi(Dialog1, message_payload[2])
                Dialog1.exec_()
                if ui.resposta == "aceitar":
                    self.user.adiciona_contato(message_payload[2])
                    self.atualiza_lista_contatos()
                else:
                    self.user.bloqueia(message_payload[2])

        else:
            if(cliente.nome != message_payload[2]):
                print(message_payload)
                print(message_payload[0])
                print(self.dest)
                if message_payload[0] == '0' and message_payload[2] not in self.user.bloqueados and message_payload[2] == self.dest:
                    self.model.add_message(USER_THEM,message_payload[1]) #PRINTA NA TELA
                    print("privadaa")
                    cur.execute("INSERT INTO stocks VALUES (? ,? ,?)",(message_payload[2] ,message_payload[3] ,message_payload[1]))
                    con.commit()
                elif message_payload[0] == '1' and message_payload[3] == self.dest:
                    print("GRupo")
                    self.model.add_message(USER_THEM,"("+message_payload[2]+")\n" +message_payload[1]) #PRINTA NA TELA
                    cur.execute("INSERT INTO stocks VALUES (? ,? ,?)",(message_payload[2] ,message_payload[3] ,message_payload[1]))
                    con.commit()
                elif message_payload[2] not in self.user.bloqueados:
                    print("Aquiiii")
                    cur.execute("INSERT INTO stocks VALUES (? ,? ,?)",(message_payload[2] ,message_payload[3] ,message_payload[1]))
                    con.commit()
                else:
                    print("ta caido aqui")
                


    def enviar(self):  # envia mensagem
        msg = mensagens() # objeto do tipo mensagens
        msg.remetente = self.name # remetente = atributo nome
        msg.destinatario = self.dest # destinatario = atributo dest
        msg.mensagem = (self.textEdit.toPlainText())  #le texto no campo do texto
        print("destino:"+self.dest)
        print("Mensagem:")
        print(msg.mensagem)
        if self.dest in self.user.grupos: #caso conversa for de grupo
            msg.tipo = 1                    #seta o tipo pra 1
            if len(msg.mensagem) != 0:
                print("mandou pro grupo")
                mensagem =str(msg.tipo) + "," + msg.mensagem +"," + self.name +"," + self.dest
                print(mensagem)
                self.user.client.publish("mqttBridge",mensagem)
                self.model.add_message(USER_ME, msg.mensagem) #PRINTA NA TELA
                cur.execute("INSERT INTO stocks VALUES (? ,? ,?) ",(msg.remetente ,msg.destinatario ,msg.mensagem))
                con.commit()

        else:
            msg.tipo = 0
            if len(msg.mensagem) != 0:
                print("mandou privado")
                mensagem =str(msg.tipo) + "," + msg.mensagem +"," + self.name +"," + self.dest
                print(mensagem)
                self.user.client.publish("mqttBridge",mensagem)
                #self.user.send_msg(msg,"",0) #ENVIA MENSAGEM
                self.model.add_message(USER_ME, msg.mensagem) #PRINTA NA TELA
                cur.execute("INSERT INTO stocks VALUES (? ,? ,?) ",(msg.remetente ,msg.destinatario ,msg.mensagem))
                con.commit()
        
  
    def adicionar(self):
        Dialog.exec_()  #Executa screen2
        print(tela2.nova_conversa) #printa tipo de conversa e o nome
        if tela2.nova_conversa[0] != "null":
            self.user.novo_chat(tela2.nova_conversa[1],tela2.nova_conversa[0]) #inicia conversa com o nome [1] e tipo [0]
            #self.dest = tela2.nova_conversa[1]  #salva nome da conversa no atributo dest
            self.tipo_conversa = tela2.nova_conversa[0]
            self.atualiza_lista_contatos()
        
    def atualiza_lista_contatos(self):
        for x in self.user.contatos:
            if x not in self.contatos:
                item = QListWidgetItem(x)
                item.setSizeHint(QSize(-1, 50))
                self.listWidget.addItem(item)
                self.contatos.append(x)
        for x in self.user.grupos:
            if x not in self.contatos:
                item = QListWidgetItem(x)
                item.setSizeHint(QSize(-1, 50))
                self.listWidget.addItem(item)
                self.contatos.append(x)

def on_connect(client,userdata,flags,rc):# called when the broker responds to our connection request
    print("Connected - rc:",rc)

def on_subscribe(client, userdata,mid,granted_qos):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
    #quando conectar no topico informar aos clientes conectados no topico
    #informo que esta conectando com user name, uma flag de conecao se 1 append no vetor senao remove, topico geral que todos se conectam
    # mandar a mensagem de estar se conectando com o seu user
    
def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    # aqui separar o que esta entre virgula
    msg_list = message.payload.decode("utf-8").split(",")
    print(msg_list)
    

def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
    #remove o nome do usuario que desconectou; manda mensagem de conecçao com 0
    
def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    tela1 = screen1()        #   declara objeto tela1    
    tela1.setupUi(MainWindow)#   "instancia" objeto          
    MainWindow.show()        #    executa     
    app.exec_()              #   executa

    nome = tela1.name       #sava nome
    Dialog = QtWidgets.QDialog() #decla objetos para a screen2 (iniciar novas conversas)
    tela2 = screen2() #decla objetos para a screen2 (iniciar novas conversas)
    tela2.setupUi(Dialog)   #decla objetos para a screen2 (iniciar novas conversas)
    
    # Insert a row of data
    
    # Save (commit) the changes
    
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    
    Dialog1 = QtWidgets.QDialog()
    ui = solicitacao()

    cliente = Chat_mqtt()                           #                                
    cliente.my_user(nome)                           #                                
    cliente.client.on_subscribe = on_subscribe      #  Inicia cliente Mqtt                         
    cliente.client.on_unsubscribe = on_unsubscirbe  ##                              
    cliente.client.on_connect = on_connect          ##                      
    cliente.client.on_message = on_message          ##                      
    cliente.client.connect("localhost",1883)        ##                        
    cliente.inicia()                                #
    con = sqlite3.connect(nome+".db")
    cur = con.cursor()

    # Create table
    try:
        cur.execute("CREATE TABLE stocks(remetente text, dest text, mensagem text)")
    except:
        pass
    cliente.consumer = KafkaConsumer(                   #                        
         bootstrap_servers=['localhost:9092'],          #    Inicia o consumidor do kaka        
         auto_offset_reset='earliest',                  #    
         enable_auto_commit=True,                       #
         group_id=cliente.nome) #passar nome do usuario #                    
    cliente.consumer.subscribe(cliente.topics)          #                
    
    tela3 = screen3(cliente)    #                
    tela3.setupUi(MainWindow)   #Declara e Inicia screen 3                
    tela3.name = nome           #        
    app.exec_()                 #
    con.close()