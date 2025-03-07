from utils.parser import Parser

class Joueur(Parser):
    def __init__(self,id:int = -1,nom:str= ""):
        self.nom = nom
        self.id = id
        self.cartes = []
        self.defausse = []
        self.ptsinflu = 1
        self.couleur = None

    def decode(data:str):
        id = int(data[0])
        nom = data[1:]
        return Joueur(id,nom)