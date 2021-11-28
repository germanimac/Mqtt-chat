import sys, pygame
import interface
import client1

usuario = False

def on_connect(client,userdata,flags,rc):# called when the broker responds to our connection request
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

pygame.init()
#pygame.font.init()

#crias as telas 
##userScreen = interface.Screen("User Screen", 800,400) 
##chatScreen = interface.Screen("chat screen")
##roomScreen = interface.Screen("room screen")

#seta a primeira screen
##win = userScreen.makeCurrent()

# enquanto nao acabar
##done = False

##while not done:
    ##userScreen.screenUpdate()
    ##chatScreen.screenUpdate()
    ##roomScreen.screenUpdate()
    #mouse_pos = pygame.mouse.get_pos()
    #mouse_click = pygame.mouse.get_pressed()
    #keys = pygame.key.get_pressed()

    #userScreen Page code
    ##if userScreen.checkUpdate():
        #screen2button = testButton.focusCheck(mouse_pos, mouse_click)
        #testeButton.showButton(userScreen.returnTitle()) #draw the button on the screen that you are on
        
        #if screen2.checkUpdate(): #if the button is clicked 
            #win = screen2.makeCurrent() #change the screen
            #menuScreen.endCurrent()
        ##pass

    #chatScreen Page code
    ##elif chatScreen.checkUpdate():
        # back button
        #returnm = returnButton.focusCheck(mouse_pos,mouse_click)
        #returnButton.showButton(chatScreen.returnTitle())

        #if returnm:
            #win = userScreen.makeCurrent()
            #userScreen.endCurrent()
        ##pass

    ##for event in pygame.event.get():
        ##if(event.type == pygame.QUIT):
            ##done = True

    ##pygame.display.update()

##pygame.quit()

# ---- Nosso antigo -----
# screen
size = width, height = 1366, 720
screen = pygame.display.set_mode([800,400])
texto_input = interface.text_input(200,200,140,32)
texto_input.input_rect_color('lightskyblue3','gray15')
texto_input.text_font()
cliente1 = client1.Chat_mqtt()

entrar = interface.botao([200,260,60,20],(255,0,0))
entrar.set_text("Entrar", "Arial", 12, (255,255,255))


# inteface loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            texto_input.mouse_event(event)

        if event.type == pygame.KEYDOWN:
            texto_input.keyboard_event(event)

        #texto_input.text_input_event()

    

    if entrar.click():
        #fechar a screen e passar o dado do nome formadoif
        if len(texto_input.user_text) !=0:
            cliente1.my_user(texto_input.user_text)
            cliente1.client.on_subscribe = on_subscribe
            cliente1.client.on_unsubscribe = on_unsubscirbe
            cliente1.client.on_connect = on_connect
            cliente1.client.on_message = on_message
            cliente1.client.connect("localhost",1883)
            cliente1.client.loop_start()
    
                
    screen.fill((202,228,241))
    entrar.desenha(screen)
    texto_input.text_input_view(screen)
    pygame.display.flip()

cliente1.finaliza()