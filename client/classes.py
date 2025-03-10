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
        self.active_border_color = (0, 0, 0)  # Couleur de bordure noire quand active
        self.text = ''
        self.texte_affiché = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.width = 500
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = self.pos
        
        # Nouvelles variables pour la suppression continue
        self.backspace_held = False
        self.backspace_timer = 0
        self.initial_delay = 500  # Délai initial avant répétition (en ms)
        self.repeat_delay = 50    # Délai entre chaque répétition (en ms)

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
                    self.last_valid_text = self.text
                    self.backspace_held = True
                    self.backspace_timer = pygame.time.get_ticks()
                else:
                    self.text += event.unicode
                    self.last_valid_text = self.text

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = False

    def clear(self):
        self.text = ''
        self.last_valid_text = ''  # Réinitialiser le dernier texte validé

    def get_text(self):
        return self.last_valid_text

    def affiche(self, surface):
        if not self.condition(): return
        
        # Gestion de la suppression continue
        if self.backspace_held and self.active and self.isAffiche():
            current_time = pygame.time.get_ticks()
            time_held = current_time - self.backspace_timer
            
            if time_held > self.initial_delay:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
                    self.last_valid_text = self.text
                    self.backspace_timer = current_time - (self.initial_delay - self.repeat_delay)

        # Affichage normal
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

    def set_text(self, nouveau_texte):
        self.texte = nouveau_texte

    def affiche(self, surface):
        if not self.condition(): return
        text_surface = self.font.render(self.texte, True, self.couleur, self.bg_color)
        surface.blit(text_surface, self.pos)


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
        if not message or message == "":
            return None
        if message[0] == '@' and "[" not in message:
            self.messages.addElement(Texte(message[1:], 10, l.screen_height-60, (43, 185, 0), None, 20))
        elif message[0] == '#' and "[" not in message:
            self.messages.addElement(Texte(message[1:], 10, l.screen_height-60, (155, 0, 180), None, 20))
        else:
            self.messages.addElement(Texte(message, 10, l.screen_height-60, (255, 255, 255), None, 20))
            
        if len(self.messages.elements) > 18:
            self.messages.elements.pop(0)
        self.update_pos()
        return message

    def update_pos(self):
        for msg in self.messages.elements:
            msg.pos.y -= 30

    def processMessage(self, message):
        if not message or message == "":
            return None
        if message[0] == '/':
            self.messages.addElement(Texte("Commandes désactivées", 10, l.screen_height-60, (255, 247, 0), None, 20))
            self.update_pos()
            return None
        if self.gmdetecte(message):
            self.messages.addElement(Texte("Message inaproprié (non envoyé)", 10, l.screen_height-60, (255, 0, 0), None, 20))
            self.update_pos()
            return None
        return "[" + l.reseau.name + "] : " + message

    def sendMessages(self, message):
        if message:
            l.reseau.send(ServerBoundMessagePacket(message))

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            text_input : TextInput = self.getElement("text_input")
            if event.key == pygame.K_t and not text_input.active and l.menu in self.menus:
                self.show = not self.show
            if event.key == pygame.K_RETURN:
                message = text_input.get_text()
                processed_message = self.processMessage(message)
                if processed_message:
                    self.addMessage(processed_message)
                    self.sendMessages(processed_message)
                text_input.clear()

    def gmdetecte(self, message):
        message = message.lower()
        for mot in l.mots_bannis:
            if mot.lower() in message:
                return True
        return False
