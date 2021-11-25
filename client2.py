import paho.mqtt.client as mqtt
import time

import threading
import time
import random

# Broker endereço e porta
broker_address = "localhost"
port = 1883

# vetor de pessoas online
users_online = []

# meu usuario
meu_user = ""

# formato da mensagem [funcao,flag,mensagem,...]

def envia(client):
    chat = "mensagem"
    while True:
        chat = input("Entre com sua mensagem:\n")
        client.publish(pubtop,chat)


##########Defining all call back functions###################

def on_connect(client,userdata,flags,rc):# called when the broker responds to our connection request
    print("Connected - rc:",rc)

def on_subscribe(client, userdata,mid,granted_qos):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
    #quando conectar no topico informar aos clientes conectados no topico
    #informo que esta conectando com user name, uma flag de conecao se 1 append no vetor senao remove, topico geral que todos se conectam
    # mandar a mensagem de estar se conectando com o seu user
    meu_user = input("Digite seu nome: ")
    msg_connect = "connect_status,1," + meu_user
    client.publish("geral",msg_connect)

def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    # aqui separar o que esta entre virgula
    msg_list = message.payload.decode("utf-8").split(",")
    #print(msg_list)
    # verifica se a mensagem recebida eh de atualizacao dos usuarios online
    if msg_list[0] == "connect_status":
        print("Comando: ",msg_list[0])
        if msg_list[1] == "1":
            print("Meu user: ",meu_user)
            print("Usuario: ",msg_list[2])
            if msg_list[2] != meu_user: 
                print("Online: ",msg_list[0])
                users_online.append(msg_list[2])
                
    
    print("Users Online:",users_online)

    global FLAG
    global chat
    # verificar se eh alguem se conectando, se for nao verifica voce tem q receber, 1 pos da msg se eh pra conectar ou nao e o 2 o user name
    # recebeu 1 eh alguem conectando online.append o user name; se for 0 faz online.remove com o username    
    if str(message.topic) != pubtop:
        msg = str(message.payload.decode("utf-8"))
        print(str(message.topic),msg)
        if msg == "Stop" or msg == "stop":
            FLAG = False
        
       # else:
       #     chat = input("Enter Message: ")
       #     client.publish(pubtop,chat)

def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
    #remove o nome do usuario que desconectou; manda mensagem de conecçao com 0
    msg_connect = ["connect_status",0,meu_user]
    client.publish("geral",msg_connect)

def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")




client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port)

#CENTRAL topico fixo, todos os clientes que contarem, se inscrevem nesse topico
pubtop  = "central"
subtop = "/chat/client2"

FLAG = True
chat = None

client.loop_start()
client.subscribe("geral")
threading.Thread(target=envia, args=(client, )).start()
time.sleep(1)

while True:
    if FLAG == False or chat == "Stop" or chat == "stop":
        break

client.disconnect()
client.loop_stop()