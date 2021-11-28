
import sys, pygame

#color_light = (170,170,170)# light shade of the button
color_dark = (100,100,100) # dark shade of the button

RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 40, 0)
DARK_BLUE = (0, 0, 40)
DARK_RED = (120, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
MARROM = (75, 54, 33)
MARROM_ESCURO = (40,19,0)


# text font


# button class
class botao:
    def __init__(self, pos_tam, color = color_dark): #construtor recebe a tela e sua cor
        self.pos_tam= pos_tam
        self.color =color
        self.pos_text = [(pos_tam[0]+5),(pos_tam[1]+5)]
        self.check =False
        self.set_text()

    def set_text(self, texto = "", font = "Corbel", size = 20, color = BLACK):
        
        font = pygame.font.SysFont(font,size) # configura texto
        self.text = font.render(texto , True , color) 

    def desenha(self, tela):
        self.tela =tela
        color_light = (self.color[0]*0.7,self.color[1]*0.7,self.color[2]*0.7)
        #print(color_light)
        self.tela.blit(self.text , self.pos_text)
        mouse = pygame.mouse.get_pos()
        if self.pos_tam[0] <= mouse[0] <= self.pos_tam[0] + self.pos_tam[2] and self.pos_tam[1] <= mouse[1] <= self.pos_tam[1] + self.pos_tam[3]: # botao de entrada
            pygame.draw.rect(self.tela, color_light, self.pos_tam )
            self.tela.blit(self.text , self.pos_text )
        else:
            pygame.draw.rect(self.tela,self.color, self.pos_tam )
            self.tela.blit(self.text , self.pos_text )
    
    def click(self):
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0) and self.pos_tam[0] <= mouse[0] <= self.pos_tam[0]+self.pos_tam[2] and self.pos_tam[1] <= mouse[1] <= self.pos_tam[1]+self.pos_tam[3] and self.check == False:
            self.check =True
            print('Clicked')
            return True

        if pygame.mouse.get_pressed() == (0, 0, 0):
            self.check =False
        return False

# text input class
class text_input():
    def __init__(self,esquerda, topo, largura, altura ):
        self.esquerda =esquerda
        self.topo = topo
        self.largura =largura
        self.altura =altura
        self.active = False
        self.input_rect = pygame.Rect(esquerda, topo, largura, altura)
        self.user_text = ""
    
    def input_rect_color(self, color_active, color_passive):
        self.color_active = pygame.Color(color_active)
        self.color_passive = pygame.Color(color_passive)
    
    def text_font(self, font = None, tamanho = 32):
        self.base_font = pygame.font.Font(font,tamanho)

    def mouse_event(self, event):
        if self.input_rect.collidepoint(event.pos):
                self.active = True
        else:
            self.active = False
    
    def keyboard_event(self, event, limit =40):
        if self.active == True:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else: 
                if len(self.user_text) <= limit:
                    self.user_text += event.unicode 

    def text_input_view(self,screen):
        if self.active:
            color = self.color_active
        else:
            color = self.color_passive

        #draw the rect
        pygame.draw.rect(screen,color,self.input_rect,2)
        text_surface = self.base_font.render(self.user_text, True,(0,0,0))
        screen.blit(text_surface,(self.input_rect.x+5,self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

colours = {"White" : (255,255,255)}
class Screen():
    def __init__(self,title,width = 640, height = 445,fill=colours["White"]):
        self.title = title
        self.width = width
        self.height = height
        self.fill = fill
        self.current = False
    
    def makeCurrent(self):
        pygame.display.set.caption(self.title)
        self.current = True
        self.screen = pygame.display.set_mode((self.width, self.height))    

    def endCurrent(self):
        self.current = False

    def checkUpdate(self):
        return self.current
        
    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)
    
    def returnTitle(self):
        return self.screen
