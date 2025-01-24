import pygame as p
import random

colors = {"red":0,"blue":1,"green":2,"black":3,"yellow":4}

class Types:
    def __init__(self,id, nom,description):
        self.id = id
        self.nom = nom
        self.description = description

    def capacite(self):
        raise NotImplementedError("The method not implemented")
    
class Archer(Types):
    def __init__(self):
        super().__init__(0, "Archer", "Eliminez la première ou la dernière carte de la File")

    def capacite(self,Player,Game, Carte):
        #Todo
        return
    
class Soldat(Types):
    def __init__(self):
        super().__init__(1, "Soldat", "Eliminez une carte adjacente")

    def capacite(self,Player,Game, Carte):
        file = Game.file_influance
        ajdCard = random.choice([file[Carte.pos-1], file[Carte.pos+1]])  
        Game.discard(ajdCard)
    
class Espion(Types):
    def __init__(self):
        super().__init__(2, "Espion", "Volez 1 point d'influence à un joueur dont l'une des cartes est adjacente")

    def capacite(self,Player,Game, Carte):
        file = Game.file_influance
        ajdCard = random.choice([file[Carte.pos-1], file[Carte.pos+1]])  
        Game.getPlayer(ajdCard.idPlayer).ptsinflu -= 1
        Player.ptsinflu += 1
           
class Heritier(Types):
    def __init__(self):
        super().__init__(3, "Héritier", "S'il n'y a pas de d'atre carte révélée du même nom gagnez 2 points d'influence")

    def capacite(self,Player,Game, Carte):
        #Todo
        return
    
class Changeforme(Types):
    def __init__(self):
        super().__init__(4, "Changeforme", "Copiez la capacité d'un personnage révélé adjacent")

    def capacite(self,Player,Game, Carte):
        #Todo
        return

class Seigneur(Types):
    def __init__(self):
        super().__init__(5,"Seigneur", "Gagnez 1 point d'influence et 1 point supplémentaire par carte adjacente de votre famille")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += 1
        file = Game.file_influance
        try:
            if (file[Carte.pos-1].couleur == Carte.couleur): Player.ptsinflu += 1
        except: pass

        try: 
            if(file[Carte.pos+1].couleur == Carte.couleur): Player.ptsinflu += 1
        except: pass
    
class Assassinat(Types):
    def __init__(self):
        super().__init__(6, "Assassinat", "Eliminez une carte n'importe pù dans la File. Défaussez l'Assassinat")

    def capacite(self,Player,Game, Carte):
        #Todo
        return
    
class DecretRoyal(Types):
    def __init__(self):
        super().__init__(7, "Décret Royal", "Déplacez une carte n'importe où dans la File sauf sur une autre carte. Défaussez le Décret royal")

    def capacite(self,Player,Game, Carte):
        #Todo
        return

class Embuscade(Types):
    def __init__(self):
        super().__init__(8, "Embuscade", "Défaussez les points d'influences présents sur l'Embuscade puis gagnez 1 point d'influence. Défaussez l'Embuscade")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += 1
        file = Game.file_influance
        Game.discard(Carte.pos)

    def onDeath():
        return 
    
    
class Complot(Types):
    def __init__(self):
        super().__init__(9, "Complot", "Gagnez le double de point d'influence présents sur le Complot. Défaussez le Complot")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += (Carte.ptsinflu*2)
        Game.discard(Carte.pos)

class Carte(p.sprite.Sprite):
    def __init__(self, type:Types):
        self.couleur = None
        self.type = type
        self.img = type
        self.idPlayer = -1
        self.pos = -1
        self.ptsinflu = 0
        self.shown = False
    
    def set_player(self,joueur):
        self.idPlayer = joueur.id
        self.couleur = joueur.couleur
        return self
    
    def capacite(self,game):
        if self.pos == -1 or not self.shown:
            print("can't use card ")
            return 
        player = game.get_player(self.idPlayer)
        self.type.capacite(player,game)

types : list[Types] = []

def full_deck(joueur):
    out = []
    for e in types:
        out.append(Carte(e).set_player(joueur))
    return out
    