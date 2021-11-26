import paho.mqtt.client as mqtt
import time

import threading
import time

topics = []
bloqueados =  []
class Mensagens():
    def __init__(self):
        self.tipo =0
        self.mensagem = ""
        self.remetente = ""
        self.destinatario = ""
    
    def escreve_msg(self, mensagem, remetente, destinatario):
        self.mensagem = mensagem
        self.remetente = remetente
        self.destinatario = destinatario

    def le_msg(self):
        return self
    def _dest(self, dest):
        self.destinatario = dest
    def str_to_msg(self, strmsg):
        str_msg = strmsg.decode("utf-8").split(",")
        self.tipo =int(str_msg[0])
        self.mensagem = str_msg[1]
        self.remetente = str_msg[2]
        self.destinatario = str_msg[3]

    def msg_to_str(self):
        return (str(self.tipo) + "," + self.mensagem +"," + self.remetente +"," + self.destinatario)

class Chat_mqtt():
    def __init__(self):

        self.nome = ""
        self.topics = []
        self.bloqueados = []
        self.grupos = []
        self.contatos = []
        self.pubtop = ""
        self.subtop = ""
        

    def my_user(self, nome):
        self.nome = nome
        self.client = mqtt.Client(self.nome)

    def inicia(self):
        self.topics.append(self.nome)
        self.client.subscribe(self.nome)
        
    """ def main(self):
        msg = Mensagens()
        msg.remetente = self.nome
        dest = input("Novo Contato:")
        msg.destinatario =dest
        self.novo_chat(dest)

        while True:
            chat = input("Enter Message:")
            if(chat == "stop"):
                novo = input("Insira um nome ou Grupo:")
                pubtop = self.nova_conversa(novo)
            elif chat == "desbloquear":
                contato = input("Nome do usuario para debloquear:")       
                self.debloqueia(contato)
            elif chat == "sair":
                break
            else:
                msg = nome+","+pubtop+","+chat
                client.publish(pubtop,msg) """

    def novo_chat(self, _nova_conversa, tipo = "privado"):
        if tipo == "privado":
            self.novo_contato(_nova_conversa)
        elif tipo == "grupo":
            self.novo_grupo(_nova_conversa)
    
    def novo_grupo(self, nome):
        if(nome in self.grupos):
            self.pubtop = nome
            return 0
        else:
            self.subtop = nome
            self.pubtop = nome
            self.adiciona_grupo(nome)
            self.client.subscribe(nome)
            return 1

    def novo_contato(self, nome):
        if(nome in self.contatos):
            self.pubtop = nome
            return 0
        elif nome in self.bloqueados:
            self.pubtop = nome
            self.desbloqueia(nome)
            self.adiciona_contato(nome)
            return 1
        else:
            self.pubtop = nome
            self.adiciona_contato(nome)
            self.solicitacao(nome)
            return 1
            
    def desbloqueia(self, nome):
        if(nome in self.bloqueados):
            indice = self.bloqueados.index(nome)
            del self.bloqueados[indice]

    def solicitacao (self, nome):
        solicita = Mensagens()
        solicita.destinatario =nome
        solicita.tipo = 5
        solicita.remetente = self.nome
        self.send_msg(solicita, 5)

    def finaliza(self):
        self.client.disconnect()
        self.client.loop_stop()
    
    def bloqueia(self, contato):
        self.bloqueados.append(contato)
    
    def adiciona_contato(self, contato):
        self.topics.append(contato)
        self.contatos.append(contato)

    def adiciona_grupo(self, grupo):
        self.topics.append(grupo)
        self.grupos.append(grupo)
        self.client.subscribe(grupo)
    
    def deleta_grupo_contato(self, nome):
        if nome in self.topics:
            indice = self.topics.index(nome)
            del self.topics[indice]
            if nome in self.contatos:
                indice = self.contatos.index(nome)
                del self.contatos[indice]
            else:
                indice = self.grupos.index(nome)
                del self.grupos[indice]
                self.client.unsubscribe(nome)
        else:
            print("Não encontrado")
    
    def send_msg(self, msg, pubtop, tipo = -1):
        if(tipo != -1):
            msg.tipo = tipo
        self.client.publish(pubtop,msg.msg_to_str())
        
def on_connect(self,client,userdata,flags,rc):# called when the broker responds to our connection request
        print("Connected - rc:",rc)

def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    global FLAG
    global chat
    print(message)
    msg = message.payload.decode("utf-8").split(",")
    #self.recebe_mensagem(msg)

def on_subscribe(client, userdata,mid,granted_qos):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
def on_unsubscirbe( client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
def on_disconnect( client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")

##########Defining all call back functions###################

cliente1 = Chat_mqtt()
cliente1.my_user("joao")
cliente1.client.on_subscribe = on_subscribe
cliente1.client.on_unsubscribe = on_unsubscirbe
cliente1.client.on_connect = on_connect
cliente1.client.on_message = on_message
cliente1.client.connect("localhost",1883)
cliente1.client.loop_start()

#cliente1.main()
cliente1.finaliza
#
