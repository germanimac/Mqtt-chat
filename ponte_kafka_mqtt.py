import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time
from kafka.admin import KafkaAdminClient, NewTopic
from mensagens import mensagens
from kafka import KafkaProducer
from json import dumps
 
usuarios = []

class mqtt_bridge():
    def __init__(self):

        self.admin_client = KafkaAdminClient( ##inicializa kaftaAdmin
        bootstrap_servers="localhost:9092", 
        client_id='MQTTBridge'
        )
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],  #inicializa produtor
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

        mqtt_broker = "localhost"                     #configura mqtt
        self.mqtt_client = mqtt.Client("MQTTBridge")  #configura mqtt                    
        self.mqtt_client.connect(mqtt_broker)         #configura mqtt            
        self.mqtt_client.loop_start()                 #configura mqtt    
        self.mqtt_client.subscribe("mqttBridge")      #configura mqtt               
        self.mqtt_client.on_message = self.on_message #configura mqtt                    
        while True:
            pass
        self.mqtt_client.loop_end()

    def on_message(self, client, userdata, message): #mensagens recebidas
        msg = mensagens()
        msg_payload = message.payload.decode("utf-8")
        msg.str_to_msg(msg_payload)
        
        if msg.tipo == 7: #se msg.tipo == 7 quer dizer que usuario esta entrando no programa
            try:  # tenta criar um tópico kafta pro usuario, se ja houver, não faz nada
                if msg.remetente not in usuarios: 
                    usuarios.append(msg.remetente)
                topic_list = []
                topic_list.append(NewTopic(msg.remetente, num_partitions=1, replication_factor=1))
                self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
            except:
                pass
        elif msg.tipo == 5:   ## tenta se conectar com um cliente, se não existir devolve erro ao cliente
            if msg.destinatario not in usuarios:
                print(usuarios)
                data = {'message': ','+msg.msg_to_str()+','}
                self.producer.send(msg.remetente, value=data)
        else: ##envia mensagem
            data = {'message': ','+msg.msg_to_str()+','}
            self.producer.send(msg.destinatario, value=data)
            time.sleep(1)

#kafka_producer.produce(str("msg_payload").encode('ascii'))

mqtt_kafta= mqtt_bridge()  #ponte mqtt_kafta