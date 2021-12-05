class mensagens():
    def __init__(self):
        self.tipo =0
        self.mensagem = ""
        self.remetente = ""
        self.destinatario = ""
    def preenche_obj(self,msg_list):
        self.mensagem = msg_list[1]
        self.remetente = msg_list[2]
        self.destinatario = msg_list[3]
        self.tipo =msg_list[0]
    def escreve_msg(self, mensagem, remetente, destinatario):
        self.mensagem = mensagem
        self.remetente = remetente
        self.destinatario = destinatario

    def le_msg(self):
        return self
        
    def _dest(self, dest):
        self.destinatario = dest
    def str_to_msg(self, strmsg):
        str_msg = strmsg.split(",")
        self.tipo =int(str_msg[0])
        self.mensagem = str_msg[1]
        self.remetente = str_msg[2]
        self.destinatario = str_msg[3]

    def msg_to_str(self):
        return (str(self.tipo) + "," + self.mensagem +"," + self.remetente +"," + self.destinatario)
