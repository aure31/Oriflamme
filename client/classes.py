import pygame
import loader as l
from groupelement import GroupElement,ListElement
from packet.serverbound import ServerBoundMessagePacket

pygame.init()


class Element:

    def __init__(self, x: int, y: int, condition=lambda: True):
        self.condition = condition
        self.pos = pygame.Vector2(x, y)
        self.menus = []
        

    def addMenu(self, menu):
        self.menus.append(menu)

    def isAffiche(self):
        if not self.condition():
            return False
        for menu in self.menus:
            if menu.isAffiche():
                return True
        return False

    def affiche(self, window):
        pass


class EventHandler:
    listItems = [[] for i in range(11)]

    def __init__(self,priority=10):
        print("client : init EventHandler")
        EventHandler.listItems[priority].append(self)
        self.priority = priority
        pass

    def onEvent(self, event):
        pass

    def handle_event_all(event):
        for subList in EventHandler.listItems:
            for item in subList:
                item.onEvent(event)


class TextInput(Element, EventHandler):

    def __init__(self, x: int, y: int, condition=lambda: True):
        Element.__init__(self, x, y, condition)
        EventHandler.__init__(self,0)
        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
        self.border_color = (200, 200, 200)  # Couleur de bordure grise
        self.active_border_color = (0, 0, 0
                                    )  # Couleur de bordure noire quand active
        self.text = ''
        self.texte_affiché = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.width = 500
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width,
                                self.height)  # Initialiser self.rect
        self.rect.topleft = self.pos  # Définir la position de self.rect

    def onEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active and self.isAffiche():
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
        self.texte_affiché = self.text[-40:]
        text_surface = self.font.render(self.texte_affiché, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class Bouton(Element):
    pressed = False

    def __init__(self,
                 image1,
                 image2,
                 pos: pygame.Vector2 = pygame.Vector2(0, 0),
                 condition=lambda: True):
        super().__init__(pos.x, pos.y, condition)
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
        retour = pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()) and not Bouton.pressed
        Bouton.presse(retour)
        if retour:
            #l.click.play()
            self.onClique()
        return retour

    def presse(retour):
        if not pygame.mouse.get_pressed()[0]:
            Bouton.pressed = False
        elif retour:
            Bouton.pressed = True

    def onClique(self):
        pass


class Texte(Element):

    def __init__(self,
                 texte,
                 x,
                 y,
                 couleur=(0, 0, 0),
                 bg_color=None,
                 taille=32,
                 police="client/assets/arial.ttf",
                 condition=lambda: True):
        super().__init__(x, y, condition)
        self.texte = texte
        self.couleur = couleur
        self.bg_color = bg_color
        self.font = pygame.font.Font(police, taille)

    def set_text(self, texte):
        self.texte = texte

    def affiche(self, surface):
        if not self.condition(): return
        # Rendre le texte
        text_surface = self.font.render(self.texte, True, self.couleur,
                                        self.bg_color)
        # Afficher le texte à la position (x, y)
        surface.blit(text_surface, self.pos)
        #print("client : affiche texte : ",self.texte)

class Image(Element):
    
    def __init__(self, image, x, y, condition=lambda: True):
        super().__init__(x, y, condition)
        self.image = pygame.image.load(image)

    def affiche(self, surface):
        if not self.condition(): return
        surface.blit(self.image, self.pos)


class Chat(GroupElement, EventHandler):

    def __init__(self):
        EventHandler.__init__(self)
        GroupElement.__init__(self, "Chat")
        self.messages: ListElement = ListElement()
        self.show = False
        self.addElement("background", Image("client/assets/chat.png", 0, 290))
        self.addElement("text_input", TextInput(0, l.window.get_height() - 40))
        self.addElement("messages", self.messages)

    def affiche(self, surface: pygame.Surface):
        if self.show:
            super().affiche(surface)
        else:
            return

    def addMessage(self, message):
        if message == "":
            pass
        elif message == "Wj54Jie4/":
            self.messages.addElement(Texte("Message inaproprié (non envoyé)",10,l.screen_height-60, (255, 0, 0), None, 20))
        elif message[0] == '/':
            self.messages.addElement(Texte(message[1:],10,l.screen_height-60, (255, 247, 0), None, 20))
        elif message[0] == '@':
            self.messages.addElement(Texte(message[1:],10,l.screen_height-60, (43, 185, 0), None, 20))
        else:
            self.messages.addElement(Texte(message,10,l.screen_height-60, (255, 255, 255), None, 20))
        if len(self.messages.elements) > 18:
            self.messages.elements.pop(0)
        self.update_pos()

    def update_pos(self):
        for msg in self.messages.elements:
            msg.pos.y -= 30

    def sendMessages(self,message):
        l.reseau.send(ServerBoundMessagePacket(message))

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            text_input : TextInput = self.getElement("text_input")
            if event.key == pygame.K_t and not text_input.active and l.menu in self.menus :
                if self.show:
                    self.show = False
                else:
                    self.show = True
            if event.key == pygame.K_RETURN:
                if self.gmdetecte(text_input.get_text()):
                    self.addMessage("Wj54Jie4/")
                else:
                    format_text = "["+l.reseau.name+"] : "+text_input.get_text()
                    self.addMessage(format_text)
                    self.sendMessages(format_text)
                text_input.clear()

    def gmdetecte(self, message):
        message = message.lower()
        for mot in l.gm:
            if mot in message:
                return True
        return False
