import pygame
import loader as l

pygame.init()

class Element:
    def __init__(self,x:int,y:int,condition = lambda : True):
        self.condition = condition
        self.pos = pygame.Vector2(x,y)

    def setMenu(self,menu):
        self.menu = menu

    def affiche(self):
        pass

class EventHandler:
    listItems = []

    def __init__(self):
        EventHandler.listItems.append(self)
        pass
    
    def onEvent(self, event):
        pass

    def handle_event_all(event):
        for item in EventHandler.listItems:
            item.onEvent(event)

class TextInput(Element,EventHandler):
    def __init__(self, x : int , y : int,condition = lambda : True):
        super(Element).__init__(x,y,condition)
        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
        self.border_color = (200, 200, 200)  # Couleur de bordure grise
        self.active_border_color = (0, 0, 0)  # Couleur de bordure noire quand active
        self.text = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.width = 500
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Initialiser self.rect
        self.rect.topleft = self.pos  # Définir la position de self.rect
        TextInput.inputList.append(self)

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(f'Texte validé : {self.text}')
                    self.last_valid_text = self.text
                    self.active = False  # Désactiver le champ de texte
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.last_valid_text = self.text  # Mettre à jour le dernier texte validé après suppression
                else:
                    self.text += event.unicode
                    self.last_valid_text = self.text  # Mettre à jour le dernier texte validé

    def clear(self):
        self.text = ''
        self.last_valid_text = ''  # Réinitialiser le dernier texte validé

    def get_text(self):
        return self.last_valid_text

    def affiche(self, surface):
        if not self.condition(): return
        pygame.draw.rect(surface, self.bg_color, self.rect)
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(surface, border_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))



class Bouton(Element):
    pressed = False
    def __init__(self, image1 , image2 , pos : pygame.Vector2 = pygame.Vector2(0, 0), condition = lambda : True):
        super().__init__(pos.x,pos.y,condition)
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.rect = self.image1.get_rect()
        self.rect.topleft = (pos.x, pos.y)
        
    def affiche(self, surface):
        if not self.condition(): return
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.image2, self.rect.topleft)
        else:
            surface.blit(self.image1, self.rect.topleft)
        self.estClique()
    
    def setCoord(self, x, y):
        self.rect.topleft = (x, y)
        return self

    def estClique(self):
        retour = pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and not Bouton.pressed 
        Bouton.presse(retour)
        if retour:
            l.click.play()
            self.onClique()
        return retour
    
    def presse(retour):
        if not pygame.mouse.get_pressed()[0]:
            Bouton.pressed = False
        elif retour : 
            Bouton.pressed = True 

    def onClique(self):
        pass
    
class Texte(Element):
    def __init__(self, texte, x , y, couleur=(0, 0, 0), bg_color=None, taille=32, police = "client/assets/arial.ttf", condition = lambda : True):
        super().__init__(x,y,condition)
        self.texte = texte
        self.couleur = couleur
        self.bg_color = bg_color
        self.font = pygame.font.Font(police, taille)

    def set_text(self, texte):
        self.texte = texte

    def affiche(self, surface):
        if not self.condition(): return
        # Rendre le texte
        text_surface = self.font.render(self.texte, True, self.couleur, self.bg_color)
        # Afficher le texte à la position (x, y)
        surface.blit(text_surface, self.pos)

class Chat:
    def __init__(self):
        self.messages = []
        self.img = pygame.image.load("client/assets/chat.png")
        self.text_input = TextInput(0, 860)
        self.show = False

    def affiche(self, surface:pygame.Surface):
        if not self.show : return
        surface.blit(self.img, (0,290))
        for mess in self.messages:
            mess.affiche(surface, 10, 830 - self.messages.index(mess) * 30)

    def envoyer(self, message):
        if message == "":
            pass
        elif message[0] == '/':
            self.messages.insert(0, Texte(message, (255,247,0), None, 20))
        elif message[0] == '@':
            self.messages.insert(0, Texte(message, (43,185,0), None, 20))
        else:
            self.messages.insert(0, Texte(message, (255,255,255), None, 20))
        if len(self.messages) > 19:
            self.messages.pop()

    def requetesServer(self):
        pass # C'est là que tu mets les packets pour le seveur