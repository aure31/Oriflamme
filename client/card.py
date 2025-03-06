import pygame as p

colors = ["red","blue","green","black","yellow"]
memo_import = {}

class Type:
    def __init__(self, id, name , path):
        self.id = id
        self.name = name
        self.path = path

class Archer(Type):
    def __init__(self):
        super().__init__(0, "Archer", "archer")

class Soldat(Type):
    def __init__(self):
        super().__init__(1, "Soldat", "soldat")

class Espion(Type):
    def __init__(self):
        super().__init__(2, "Espion", "espion")

class Heritier(Type):
    def __init__(self):
        super().__init__(3, "Héritier", "heritier")

class Changeforme(Type):
    def __init__(self):
        super().__init__(4, "Changeforme", "changeforme")

class Seigneur(Type):
    def __init__(self):
        super().__init__(5,"Seigneur", "seigneur")

class Assassinat(Type):
    def __init__(self):
        super().__init__(6, "Assassinat", "assassinat")

class DecretRoyal(Type):
    def __init__(self):
        super().__init__(7, "Décret Royal", "decretroyal")

class Embuscade(Type):
    def __init__(self):
        super().__init__(8, "Embuscade", "embuscade")

class Complot(Type):
    def __init__(self):
        super().__init__(9, "Complot", "complot")

class HandCard:
    __types__ : list[Type] = [Archer(), Soldat(), Espion(), Heritier(), Assassinat(), DecretRoyal(),
                       Embuscade(), Complot(), Changeforme(), Seigneur()]

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
    
    
