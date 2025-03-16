import pygame as p
from classes import Element

colors = ["jaune", "rouge", "bleu", "vert", "violet"]
memo_import = {}

class Type:
    def __init__(self, id, name , path):
        self.id = id
        self.name = name
        self.path = path


class HandCard(Element):
    __types__ = [
        Type(0, "Archer", "archer"),
        Type(1, "Soldat", "soldat"),
        Type(2, "Espion", "espion"),
        Type(3, "Héritier", "heritier"),
        Type(4, "Changeforme", "changeforme"),
        Type(5, "Seigneur", "seigneur"),
        Type(6, "Assassinat", "assassinat"),
        Type(7, "Décret Royal", "decretroyal"),
        Type(8, "Embuscade", "embuscade"),
        Type(9, "Complot", "complot")
    ]
    
    def __init__(self, id: int, color: str):
        super().__init__(0, 0)
        self.type = HandCard.__types__[id]
        if color is None:
            print(f"Warning - No color specified for card {id}")
            color = "gris"
        self.color = color.lower()
        print(f"Debug - Creating card: type={self.type.path}, color={self.color}")
        self.img = self.getImg()
        self.back = self.getBack()

    def getBack(self):
        if not self.color in memo_import:
            path = f"client/assets/cartes/back/dos_{self.color}.png"
            try:
                memo_import[self.color] = p.image.load(path)
            except Exception as e:
                print(f"Error loading back image {path}: {str(e)}")
                raise
        return memo_import[self.color]

    def getImg(self):
        path = f"client/assets/cartes/{self.type.path}/{self.type.path}_{self.color}.png"
        if not (self.type.id, self.color) in memo_import:
            try:
                memo_import[(self.type.id, self.color)] = p.image.load(path)
            except Exception as e:
                print(f"Error loading image {path}: {str(e)}")
                raise
        return memo_import[(self.type.id, self.color)]
    
    def toPlayCard(self,idPlayer:int = -1):
        return PlayCard(self)

    def affiche(self, window, pos):
        scaled_img = p.transform.scale(self.img, (200, 365))
        window.blit(scaled_img, pos)
    
    
class PlayCard(HandCard):
    def __init__(self, idPlayer:int, card:HandCard):
        super().__init__(card.type.id,card.color)
        self.type = card.type
        self.color = card.color
        self.img = card.img
        self.back = card.back
        self.idPlayer = idPlayer
        self.ptsinflu = 0
        self.shown = False

    def setShown(self,shown:bool):
        self.shown = shown
    
    def getImg(self):
        if self.shown:
            return self.img
        else:
            return self.back
        
    def getBack(self):
        return self.back
    
    def affiche(self,window,pos):
        window.blit(self.getImg(),pos)