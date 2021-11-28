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
    
    def resp_soli (self, nome, resposta = "sim"):
        solicita = Mensagens()
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
        self.topics.append(contato)
        self.contatos.append(contato)
        cont = conversa(contato)
        self.conversas.append(cont)

    def adiciona_grupo(self, grupo):
        self.topics.append(grupo)
        self.grupos.append(grupo)
        grup = conversa(grupo)
        self.conversas.append(grup)
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
