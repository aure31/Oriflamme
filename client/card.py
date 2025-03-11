import pygame as p

colors = ["rouge","bleu","vert","gris","jaune"]
memo_import = {}

class Type:
    def __init__(self, id, name , path):
        self.id = id
        self.name = name
        self.path = path



class HandCard:
    __types__ = [ Type(0, "Archer", "archer"),
            Type(1, "Soldat", "soldat"),
            Type(2, "Espion", "espion"),
            Type(3, "Héritier", "heritier"),
            Type(4, "Changeforme", "changeforme"),
            Type(5,"Seigneur", "seigneur"),
            Type(6, "Assassinat", "assassinat"),
            Type(7, "Décret Royal", "decretroyal"),
            Type(8, "Embuscade", "embuscade"),
            Type(9, "Complot", "complot")
            ]

    def __init__(self, id:int,color:str):
        self.type = HandCard.__types__[id]
        if color not in colors:
            raise ValueError("client : Invalid Color")
        self.color = color
        self.img = self.getImg()
        self.back = self.getBack()

    def getBack(self):
        if not self.color in memo_import:
            memo_import[self.color] = p.image.load("client/assets/cartes/back/"+self.color+".png")
        return memo_import[self.color]

    def getImg(self):
        if not (id,self.color) in memo_import:
            memo_import[(id,self.color)] = p.image.load("client/assets/cartes/"+self.type.path+"/"+self.color+".png")
        return memo_import[(id,self.color)]
    
    def toPlayCard(self,idPlayer:int = -1):
        return PlayCard(self)
    

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
    
    
