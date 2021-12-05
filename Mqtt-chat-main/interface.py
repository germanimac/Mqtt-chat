from PyQt5 import QtCore, QtGui, QtWidgets
from message_struct import Chat_mqtt
from Screen1 import screen1
#from Screen2 import screen2
from Screen3 import screen3

from kafka.admin import client
import paho.mqtt.client as mqtt
import time
from mensagens import mensagens
import threading
import time
from kafka import KafkaConsumer
from json import loads




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
    tela1 = screen1()
    tela1.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    nome = tela1.name

    cliente = Chat_mqtt()
    cliente.my_user(nome)
    cliente.client.on_subscribe = on_subscribe
    cliente.client.on_unsubscribe = on_unsubscirbe
    cliente.client.on_connect = on_connect
    cliente.client.on_message = on_message
    cliente.client.connect("localhost",1883)
    cliente.inicia()
    print(nome)
    #app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    tela3 = screen3(nome)
    tela3.setupUi(MainWindow)
    tela3.name = nome
    MainWindow.show()
    app.exec_()
    