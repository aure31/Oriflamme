import loader as l
import pygame

class GroupElement:
    def __init__(self, name):
        self.name = name
        self.elements = {}
        self.menus = []
        self.show = None

    def affiche(self,window):
        for element in self.elements.values():
            element.affiche(window)
    
    def addElement(self,name,element):
        self.elements[name] = element
        element.addMenu(self)

    def addMenu(self,menu):
        self.menus.append(menu)
    
    def getElement(self,name):
        return self.elements[name]
    
    def isAffiche(self):
        if self.show is not None:
            return self.show
        for menu in self.menus:
            if menu.isAffiche():
                return True
        return False
    

class ListElement:
    def __init__(self):
        self.elements = []
        self.menus = []

    def addMenu(self,menu):
        self.menus.append(menu)

    def affiche(self,window):
        for element in self.elements:
            element.affiche(window)
    
    def addElement(self,element):
        self.elements.append(element)
        element.menus = self.menus

    def removeElement(self,element):
        self.elements.remove(element)


class DynamicTextList(ListElement):
    def __init__(self,start:tuple[int,int] = (0,0),threshold:int = 10,color:tuple[int,int,int] = (255,255,255)):
        super().__init__()
        self.start = start
        self.threshold = threshold
        self.color = color
    
    def setText(self,text:list[str]):
        from client.classes import Texte
        self.elements = []
        y = self.start[1]
        for txt in text:
            self.addElement(Texte(txt,self.start[0],y,self.color))
            y += self.threshold


class CardListElement(GroupElement):
    def __init__(self):
        super().__init__("cartes")
        self.elements = {}
        self.menus = []
        self.card_width = 200
        self.card_height = 365
        self.margin = 15
        self.visible_height = 180
        self.y_position = 900 - self.visible_height
        self.selected_card = None

    def affiche(self, window):
        if not l.game or not l.game.cartes:
            return
        total_width = (len(l.game.cartes) * self.card_width) + ((len(l.game.cartes) - 1) * self.margin)
        start_x = (window.get_width() - total_width) // 2

        mouse_pos = pygame.mouse.get_pos()
        
        for i, card in enumerate(l.game.cartes):
            x = start_x + (i * (self.card_width + self.margin))
            y = self.y_position
            card_rect = pygame.Rect(x, y, self.card_width, self.visible_height)
            if card_rect.collidepoint(mouse_pos):
                y = 900 - self.card_height
            
            card.pos.x = x
            card.pos.y = y
            card.affiche(window, (x, y))

    def handle_click(self, pos):
        if not l.game or not l.game.cartes:
            return None
        for i, card in enumerate(l.game.cartes):
            card_rect = pygame.Rect(card.pos.x, card.pos.y, self.card_width, self.visible_height)
            if card_rect.collidepoint(pos):
                return i
        return None


class InfluenceFileElement(GroupElement):
    def __init__(self):
        super().__init__("influence_file")
        self.card_width = 100
        self.card_height = 182
        self.margin = 10
        self.y_position = 400

    def affiche(self, window):
        if not l.game or not l.game.file_influence:
            return
        total_width = (len(l.game.file_influence) * self.card_width) + ((len(l.game.file_influence) - 1) * self.margin)
        start_x = (window.get_width() - total_width) // 2

        for i, pile in enumerate(l.game.file_influence):
            x = start_x + (i * (self.card_width + self.margin))
            y = self.y_position
            
            if pile:
                top_card = pile[-1]
                scaled_img = pygame.transform.scale(top_card.getImg(), (self.card_width, self.card_height))
                window.blit(scaled_img, (x, y))
