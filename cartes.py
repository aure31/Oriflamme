import pygame as p



class Types:
    def __init__(self,id, nom,description):
        self.id = id
        self.nom = nom
        self.description = description

    def capacite(self):
        raise NotImplementedError("The method not implemented")

class Seigneur(Types):
    def __init__(self):
        super().__init__(0,"Seigneur", "gagne 1")

    def capacite(self,Player,Game):
        #Todo
        return
        

class Carte(p.sprite.Sprite):
    def __init__(self, type:Types):
        self.couleur = None
        self.type = type
        self.img = type
        self.idPlayer = -1
    
    def set_player(self,joueur):
        self.idPlayer = joueur.id
        self.couleur = joueur.couleur
        return self
    
    def capacite(self,game):
        player = game.get_player(self.idPlayer)
        self.type.capacite(player,game)

types : list[Types] = []

def full_deck(joueur):
    out = []
    for e in types:
        out.append(Carte(e).set_player(joueur))
    return out
    