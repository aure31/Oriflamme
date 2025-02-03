import pygame
import math
import os
WHITE = (255,255,255)
pygame.init()
pygame.mixer.init()
#all class for graphique elements

#class for put somme text in the screen
class texte:
  
  def initialisation(self):
    self.bold = False
    self.italic = False
    self.underline = False
    
  def __init__(self,text:list,x,y,scale,color=(255,255,255),space=0):
    self.text_x = x
    self.text_y = y
    self.scale = scale
    self.text = text
    self.text_color = color
    self.space = space
    self.normal_font = pygame.font.SysFont('comicsans', self.scale)
    self.initialisation()
  
  
  def affiche(self,WIN):
    NORMAL_FONT = self.normal_font
    dist = len(self.text)
    
     #set the font style
    NORMAL_FONT.set_bold(self.bold)
    NORMAL_FONT.set_italic(self.italic)
    NORMAL_FONT.set_underline(self.underline)
    
    for i in range(dist) :
      
      text_font = NORMAL_FONT.render(self.text[i], 1, self.text_color)
      #get the distance between the text
      dist_height = text_font.get_height()/2+self.space
      #relly complexe formul for juste put some text in the middle of the screen
      WIN.blit(text_font,
           (self.text_x - text_font.get_width() / 2, self.text_y - ((dist_height * dist)/2 - dist_height*i) - (text_font.get_height()/4-self.space)))
      
      #debug thing
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
      #print(self.y - ((dist_height * dist)/2 - dist_height*i)," : ",dist_height," : ",text_font.get_height()," : ",(dist_height * dist)/2)
      
  def set_bold(self,b:bool):
    self.bold = b
    
  def set_italic(self,i:bool):
    self.italic = i
    
  def set_underline(self,u:bool):
    self.underline = u
    
  def add_line(self,text):
    self.text.append(text)
    
class button_template:
  can_click = True
  def __init__(self,cord:tuple,scale,color,border_width=0,border_color=(0,0,0)):
      self.scale = scale
      self.color = color
      self.x = cord[0]
      self.y = cord[1]
      self.border_width = border_width
      self.border_color = border_color
      self.is_click = False
      
  def affiche(self,WIN):
    pass
  
  def mouseHover(self) -> bool:
    pass
  
  def click(self) -> bool:
    pass
    

class cir_button(button_template):
  def __init__(self,cord:tuple,scale,color,border_width=0,border_color=(0,0,0)):
    button_template.__init__(self,cord,scale,color,border_width,border_color)
    self.size = scale
    self.color = color
    self.x = cord[0]
    self.y = cord[1]
    self.border_width = border_width
    self.border_color = border_color
      
  def affiche(self,WIN):
    pygame.draw.circle(WIN, self.color, (self.x,self.y), self.size)
    if self.border_width != 0 :
      pygame.draw.circle(WIN, self.border_color, (self.x,self.y), self.size,self.border_width)
    if not pygame.mouse.get_pressed()[0]:
      button_template.can_click = True
    #debug thing
    #pygame.draw.circle(WIN, (255,255,0), (self.x, self.y), 10)
      
  def mouseHover(self) -> bool:
    if math.dist((self.x,self.y), pygame.mouse.get_pos()) <= self.scale :
      return True
    return False
  
  def click(self) -> bool:
    if self.mouseHover() and pygame.mouse.get_pressed()[0] and self.can_click:
      button_template.can_click = False
      return True
    return False
    

# make a simple rectangle button with a color and a scale
class rect_button(button_template):
    can_click = True
    def __init__(self,cord:tuple,scale,color,border_width=0,border_color=(0,0,0)):
        if isinstance(scale, int):
          self.recwidth = scale
          self.recheight = scale
        elif isinstance(scale, tuple) and len(scale) == 2:  # Vérifier si scale est une tuple de longueur 2
            self.recwidth = scale[0]
            self.recheight = scale[1]
        else:
            raise ValueError("L'échelle (scale) doit être un entier ou un tuple de deux entiers (largeur, hauteur).")
        button_template.__init__(self,cord,scale,color,border_width,border_color)
      
    def affiche(self,WIN):
      pygame.draw.rect(WIN, self.color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight))
      if self.border_width != 0 :
        pygame.draw.rect(WIN, self.border_color ,pygame.Rect(self.x-self.recwidth/2,self.y-self.recheight/2,self.recwidth,self.recheight),self.border_width)
      if not pygame.mouse.get_pressed()[0]:
        rect_button.can_click = True
      self.is_click = False
      self.click()
        
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
        
        
    def mouseHover(self) -> bool:
      mouseX = pygame.mouse.get_pos()[0]
      mouseY = pygame.mouse.get_pos()[1]
      #print(self.x-self.width/2," : ",self.x+self.width/2," : ", mouseX," : ",self.x-self.width/2 <= mouseX ," : ", self.x+self.width/2 >= mouseX)
      if self.x-self.width/2 <= mouseX and self.x+self.width/2 >= mouseX and self.y-self.recheight/2 <= mouseY and self.y+self.recheight/2 >= mouseY :
        return True
      else : return False
      
    def click(self) -> bool:
      #print(self.mouseHover() , pygame.mouse.get_pressed()[0] , self.can_click)
      if self.mouseHover() and pygame.mouse.get_pressed()[0] and self.can_click:
        rect_button.can_click = False
        self.is_click = True
        return True
      else : return False
      
      
class cir_text_button(cir_button,texte):
  
  def __init__(self,text:str, cord: tuple, scale : float, color,text_scale = 0, border_width=0, border_color=(0, 0, 0)):
    
    
    if color[0]+color[1]+color[2] > 382 :
        self.text_color = (0,0,0)
    else :
        self.text_color = (255,255,255)
        
    if text_scale == 0:
      text_scale = scale
    texte.__init__(self, text, cord[0], cord[1]-text_scale/8, text_scale, self.text_color)
    
    self.size = scale
    if text_scale == 0:
      text_height = 0
      for text in self.text:
        render = self.normal_font.render(text,1,color)
        heigth =render.get_height()/1.4
        #print(render.get_width(),":",render.get_height(),":",scale)
        if render.get_width() > self.size:
          self.size = render.get_width()
        text_height += heigth
        if text_height > self.size:
          self.size = text_height
        
    cir_button.__init__(self, cord, self.size, color, border_width, border_color)
    
  def affiche(self,WIN):
    cir_button.affiche(self,WIN)
    texte.affiche(self,WIN)
    
  def change_text(self,text):
      self.text = text
      
# make a button with a text in the middle      
class text_button(rect_button,texte):
    def __init__(self,text:list,coord:tuple,scale:int,color:tuple,width=0,border_width=0,border_color=(0,0,0)):
        if isinstance(scale, int):
          scale = (scale,scale)
        rect_button.__init__(self,coord,scale,color,border_width,border_color)
        
        if color[0]+color[1]+color[2] > 500 :
          self.text_color = (0,0,0)
        else :
          self.text_color = (255,255,255)
        
        texte.__init__(self,[text],coord[0],coord[1]-scale[1]/8,scale[1],self.text_color)
        
        
        self.cwidth = width
        self.max_text_width = 0
        self.text_height = 0
        for text in self.text:
          if self.normal_font.render(text,1,color).get_width() > self.max_text_width:
            self.max_text_width = self.normal_font.render(text,1,color).get_width()
          self.text_height += self.normal_font.render(text,1,color).get_height()
        self.width = self.max_text_width+20+self.cwidth
        self.height = self.text_height+10
        self.recheight = self.height
        self.recwidth = self.width
        
      
    def affiche(self,WIN):
      rect_button.affiche(self,WIN)
      texte.affiche(self,WIN)
      
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
      
    def change_text(self,text):
      self.text = text
      
# make a button with a image
class button_image:
    def __init__(self,image,x,y,scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.image = pygame.transform.scale(image,scale)
      
    def affiche(self,WIN):
      WIN.blit(self.image,(self.x,self.y))

    def mouseHover(self):
      if math.dist((self.x+self.scale[0]/2,self.y+self.scale[1]/2), pygame.mouse.get_pos()) <= self.scale[0]/2 :
        return True
      else : return False
      
class select_button(button_template):
    def __init__(self,text:list,coord:tuple,scale,color,width=0,border_width=0,border_color=(0,0,0),default_selected=0):
      
      self.custom_color = color
      n_button = len(text)
      if isinstance(color,tuple) or len(color) != n_button:
        self.custom_color = [color for i in range(n_button)]
      self.unselected_color = [(self.custom_color[i][0]+40,self.custom_color[i][1]+40,self.custom_color[i][2]+40) for i in range(n_button)]
      self.button = []
      self.selected = default_selected
      
      button_template.__init__(self,coord,scale,color,border_width,border_color)
      max_width = 0
      for i in range(n_button):
        self.button.append(text_button(text[i],coord,scale,self.unselected_color[i],width,border_width,border_color))
        #print(self.button[i].width,self.button[i].normal_font.render(text[i],1,color).get_width())
        if self.button[i].width > max_width:
          max_width = self.button[i].width
      
      if self.selected != None:
        self.button[self.selected].color = self.custom_color[self.selected]
        self.button[self.selected].border_color = (200,200,200)
          
      max_height = max(self.button, key=lambda x: x.height).height
      midle_lenth = max_width*(n_button-1)/2
      for i in range(n_button):
        self.button[i].recwidth = max_width
        self.button[i].recheight = max_height
        self.button[i].x = coord[0]-midle_lenth+i*max_width
        self.button[i].text_x = coord[0]-midle_lenth+i*max_width
      
    def affiche(self,WIN):
      for currant in self.button:
        currant.affiche(WIN)
      self.click()
      #print(self.selected)
      
    def click(self) -> int:
      for i in range(len(self.button)):
          if self.button[i].is_click:
            self.button[i].color = self.custom_color[i]
            self.button[i].border_color = (200,200,200)
            if self.selected != None and self.selected != i:
              self.button[self.selected].color = self.unselected_color[self.selected]
              self.button[self.selected].border_color = (255,255,255)
            self.selected = i
            return i 
      return None
    
    def get_value(self) -> int:
      return self.selected
      #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
 
class number_selector(button_template):
  def __init__(self,coord:tuple,scale,color,text_scale=0,width=0,border_width=0,border_color=(0,0,0),default_value=1):
    self.x = coord[0]
    self.y = coord[1]
    self.scale = scale
    self.color = color
    self.number = default_value
    self.max_number = 50
    self.min_number = 1
    self.cwidth = width
    self.text_font = pygame.font.SysFont('comicsans',self.scale)
    self.text = text_button(str(self.number),(self.x,self.y),self.scale,self.color,self.cwidth,border_width,border_color)
    self.minus_button = cir_text_button("-",(self.x-self.scale*2.5-self.cwidth/2,self.y),self.scale,self.color,text_scale,border_width,border_color)
    self.plus_button = cir_text_button("+",(self.x+self.scale*2.5+self.cwidth/2,self.y),self.scale,self.color,text_scale,border_width,border_color)
    
  def affiche(self,WIN):
    self.text.affiche(WIN)
    self.minus_button.affiche(WIN)
    self.plus_button.affiche(WIN)
    
    self.click()
    
  def click(self) -> int:
    if self.minus_button.click() and self.number > self.min_number:
        self.number -= 1    
    elif self.plus_button.click() and self.number < self.max_number:
        self.number += 1
    else :
      return None
    self.text.change_text([str(self.number)])
    return self.number
    #pygame.draw.circle(WIN, (255,0,0), (self.x, self.y), 10)
  
  def get_value(self) -> int:
    return self.number
      
class TextInput:
    def __init__(self, x, y, screen):
        self.rect = pygame.Rect(x, y, 500, 40)  # Taille fixe de 500x300
        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
        self.border_color = (200, 200, 200)  # Couleur de bordure grise
        self.text = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)  # Police par défaut
        self.screen = screen
        self.active = False  # Indique si le champ est actif

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Si le champ est déjà actif, on ne change pas son état
                self.active = True
            else:
                self.active = False  # Désactiver si on clique ailleurs

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:  # Valider avec la touche Entrée
                    print(f'Texte validé : {self.text}')
                    self.last_valid_text = self.text  # Stocker le dernier texte validé
                    self.clear()  # Vider le champ de texte
                elif event.key == pygame.K_BACKSPACE:  # Supprimer le dernier caractère
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # Ajouter le caractère

    def clear(self):
        self.text = ''  # Vider le champ de texte

    def get_last_valid_text(self):
        return self.last_valid_text  # Retourner le dernier texte validé

    def draw(self):
        # Dessiner le fond de la barre d'entrée
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # Dessiner la bordure
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)
        # Dessiner le texte
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Texte noir
        self.screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
