import pygame as p

colors = ["red","blue","green","black","yellow"]
ids = {0:"Archer",1:"Soldat",2:"Espion",3:"Héritier",4:"Assassinat",5:"Décret Royal",
                       6:"Embuscade", 7:"Complot", 8:"Changeforme", 9:"Seigneur"}

class Card:
    def __init__(self, id, couleur):
        self.id = id
        self.name = ids[id]
        self.couleur = couleur
        Card.get_img(self.id,self.couleur)
    
    def get_img(id,couleur):
        p.image.load("client/assets/cartes/"+ids[id]+"/"+couleur+".png")
        pass

types = [Archer(), Soldat(), Espion(), Heritier(), Assassinat(), DecretRoyal(),
                       Embuscade(), Complot(), Changeforme(), Seigneur()]