from kafka.admin import client
import paho.mqtt.client as mqtt
import time
from mensagens import mensagens
import threading
import time
from kafka import KafkaConsumer
from json import loads
# tipo 0:mensafens privadas
# tipo 1 mensagens grupo
# tipo 2 
# tipo 3
# tipo 4 novo grupo
# tipo 5 solicitação
# tipo 6 responde solicitação
# tipo 7 iniciar usuario
# tipo 
# tipo 
topics = []
bloqueados =  []

class conversa():
    def __init__(self, nome):
        self.nome= nome
        self.mensagens = []
        
    def new_message(self, msg):
        self.index=self.index+1
        self.mensagens.append(msg)

class Chat_mqtt():
    def __init__(self):

        self.nome = ""
        self.topics = []
        self.bloqueados = []
        self.grupos = []
        self.contatos = []
        self.pubtop = ""
        self.subtop = ""
        self.conversas = [[]]
        self.consumer = None
    def my_user(self, nome):
        self.nome = nome
        self.client = mqtt.Client(self.nome)

    def inicia(self):
        msg =mensagens()
        self.topics.append(self.nome)
        msg.escreve_msg("sub",self.nome,"")
        msg.tipo = 7
        self.client.publish("mqttBridge",msg.msg_to_str())
    

    def novo_chat(self, _nova_conversa, tipo = "privado"):
        if tipo == "privado":
            self.novo_contato(_nova_conversa)
        elif tipo == "grupo":
            self.novo_grupo(_nova_conversa)
    
    def novo_grupo(self, nome):
        if(nome in self.grupos):
            return 0
        else:
            self.adiciona_grupo(nome)
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
        solicita = mensagens()
        solicita.destinatario =nome
        solicita.tipo = 5
        solicita.remetente = self.nome
        self.send_msg(solicita, 5)
    
    def resp_soli (self, nome, resposta = "sim"):
        solicita = mensagens()
        solicita.destinatario =nome
        solicita.tipo = 6
        solicita.remetente = self.nome
        solicita.mensagem = resposta
        self.send_msg(solicita, 6)

    def finaliza(self):
        self.client.disconnect()
        self.client.loop_stop()
    
    def bloqueia(self, contato):
        self.bloqueados.append(contato)
    
    def adiciona_contato(self, contato):
        
        self.contatos.append(contato)
        

    def adiciona_grupo(self, grupo):
        self.topics.append(grupo)
        self.grupos.append(grupo)
        
        novo_grupo = mensagens()
        novo_grupo.destinatario = self.nome
        novo_grupo.tipo = 4
        novo_grupo.remetente = grupo
        self.send_msg(novo_grupo,"", 4)
        self.consumer.subscribe(self.topics)
        
    
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
                #self.client.unsubscribe(nome)
        else:
            print("Não encontrado")
    
    def send_msg(self, msg, pubtop, tipo = -1):
        if(tipo != -1):
            msg.tipo = tipo
        self.client.publish("mqttBridge",msg.msg_to_str())
    
    def atribui_conversa(self, msg):
        if msg.remetente == self.nome:
            index = self.busca_conversa(msg.destinatario)
            self.conversas[index].new_message(msg.str_to_str())
        elif msg.destinatario == self.nome:
            index = self.busca_conversa(msg.remetente)
            self.conversas[index].new_message(msg.str_to_str())
        else:
            index = self.busca_conversa(msg.destinatario)
            self.conversas[index].new_message(msg.str_to_str())
   
    def busca_conversa(self, nome):
        x = 0
        while self.contatos[x].nome !=nome:
            x=x+1
        return x
    def consulta_conversa(self, nome):
        index = self.busca_conversa(nome)
        return self.conversas[index].mensagens
        


##########Defining all call back functions###################



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


"""
def envia(client):
    msg = mensagens()
    msg.remetente = cliente.nome
    dest = input("Novo Contato:")
    msg.destinatario =dest
    cliente.novo_chat(dest,"grupo")
    while True:
        msg.mensagem = input("Enter Message:")
        cliente.send_msg(msg,"pad")

if __name__ == "__main__":
    nome = input("Nome do usuario:")

    cliente = Chat_mqtt()
    cliente.my_user(nome)
    cliente.client.on_subscribe = on_subscribe
    cliente.client.on_unsubscribe = on_unsubscirbe
    cliente.client.on_connect = on_connect
    cliente.client.on_message = on_message
    cliente.client.connect("localhost",1883)
    cliente.inicia()

    _topics =[]
    _topics.append(cliente.nome)
    cliente.consumer = KafkaConsumer(
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         enable_auto_commit=True,
         group_id=cliente.nome) #passar nome do usuario

    cliente.consumer.subscribe(cliente.topics)  
    threading.Thread(target=envia, args=(client, )).start()
    msg_recebidas = mensagens()
    for message in cliente.consumer:
        message_payload = str(message.value.decode("utf-8")).split(",")
        del message_payload[0]
        del message_payload[-1]
        if int(message_payload[0]) == 5:
            print("Usuario ainda não existe")
        else:
            if(cliente.nome != message_payload[2]):
                print (message_payload)


    time.sleep(3000) """