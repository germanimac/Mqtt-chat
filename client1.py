import paho.mqtt.client as mqtt
import time

import threading
import time


##########Defining all call back functions###################

def on_connect(client,userdata,flags,rc):# called when the broker responds to our connection request
    print("Connected - rc:",rc)
def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    global FLAG
    global chat
   # if str(message.topic) != pubtop:
    msg = message.payload.decode("utf-8").split(",")
    if(msg[0] != nome):
        if(msg[1]==nome):
            print("Privado->[%s]:%s" %(msg[0],msg[2]))
        else:
            print("[%s:[%s]]:%s" %(msg[1], msg[0],msg[2]))
        #print(msg[2])
        if msg == "Stop" or msg == "stop":
            FLAG = False
        
        #else:
        #    chat = input("Enter Message: ")
        #    client.publish(pubtop,chat)
def on_subscribe(client, userdata,mid,granted_qos):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")


broker_address = "localhost"
port = 1883


nome = input("Insira Nome:")
#pac.append(nome)
dest = input("Insira um nome ou Grupo:")
#pac.append(dest)

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port)
#threading.Thread(target=envia, args=(client, )).start()
time.sleep(1)




pubtop = dest
subtop = dest
FLAG = True
chat = None

client.loop_start()
client.subscribe(subtop)
client.subscribe(nome)

time.sleep(1)

while True:
    chat = input("Enter Message:")
    if(chat == "stop"):
        pubtop = input("Insira um nome ou Grupo:")
    msg = nome+","+pubtop+","+chat
    client.publish(pubtop,msg)
client.disconnect()
client.loop_stop()