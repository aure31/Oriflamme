import pygame as p

colors = ["red","blue","green","black","yellow"]
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
        self.img = self.get_img()

    def get_img(self):
        if not (id,self.color) in memo_import:
            memo_import[(id,self.color)] = p.image.load("client/assets/cartes/"+self.type.path+"/"+self.color+".png")
        return memo_import[(id,self.color)]
    
    def toPlayCard(self,idPlayer:int = -1):
        return PlayCard(self)

class PlayCard(HandCard):
    def __init__(self, HandCard:HandCard):
        super().__init__(HandCard)
        self.idPlayer = -1
        self.ptsinflu = 0
        self.shown = False
    
    
