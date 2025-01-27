import pygame as p
import random

colors = ["red","blue","green","black","yellow"]



class Types:
    def __init__(self,id, nom,description):
        self.id = id
        self.nom = nom
        self.description = description

    def capacite(self):
        raise NotImplementedError("The method not implemented")
    
    def __str__(self): 
        return self.nom
    
class Archer(Types):
    def __init__(self):
        super().__init__(0, "Archer", "Eliminez la première ou la dernière carte de la File")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        ajdCard = random.choice([file[0], file[-1]])
        Game.discard(ajdCard.pos)

    
class Soldat(Types):
    def __init__(self):
        super().__init__(1, "Soldat", "Eliminez une carte adjacente")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        ajdCard = random.choice([file[Carte.pos-1], file[Carte.pos+1]])  
        Game.discard(ajdCard.pos)
    
class Espion(Types):
    def __init__(self):
        super().__init__(2, "Espion", "Volez 1 point d'influence à un joueur dont l'une des cartes est adjacente")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        ajdCard = random.choice([file[Carte.pos-1], file[Carte.pos+1]])  
        Game.getPlayer(ajdCard.idPlayer).ptsinflu -= 1
        Player.ptsinflu += 1
           
class Heritier(Types):
    def __init__(self):
        super().__init__(3, "Héritier", "S'il n'y a pas de d'atre carte révélée du même nom gagnez 2 points d'influence")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        for card in file:
            if(card.shown is True and card.pos != Carte.pos and card.type != 3): Player.ptsinflu += 2 

    
class Changeforme(Types):
    def __init__(self):
        super().__init__(4, "Changeforme", "Copiez la capacité d'un personnage révélé adjacent")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        leftCheck = (file[Carte.pos-1].shown == True and file[Carte.pos+1].shown == False)
        rightCheck = (file[Carte.pos-1].shown == False and file[Carte.pos+1].shown == True)
        if(leftCheck):
            if(file[Carte.pos-1].type != 4): file[Carte.pos-1].capacite()
        if(rightCheck): 
            if(file[Carte.pos-1].type != 4): file[Carte.pos+1].capacite()       
        if(file[Carte.pos-1].shown == True or file[Carte.pos+1].shown == True):
            choice = Player.askAjd() 
            if(file[Carte.pos-1].type != 4): file[Carte.pos+choice].capacite()

class Seigneur(Types):
    def __init__(self):
        super().__init__(5,"Seigneur", "Gagnez 1 point d'influence et 1 point supplémentaire par carte adjacente de votre famille")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += 1
        file = Game.get_top_cards()
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
        file = Game.get_top_cards()
        rndCardPos = random.randint(0, Game.get_file_size())
        Game.discard(rndCardPos)
        if(Carte not in Player.defausse):
            Game.discard(Carte.pos)    

class DecretRoyal(Types):
    def __init__(self):
        super().__init__(7, "Décret Royal", "Déplacez une carte n'importe où dans la File sauf sur une autre carte. Défaussez le Décret royal")

    def capacite(self,Player,Game, Carte):
        file = Game.get_top_cards()
        choice = Player.choiceEvrywhere()
        file.insert(choice, Carte)
        Game.discard(Carte.pos)

class Embuscade(Types):
    def __init__(self):
        super().__init__(8, "Embuscade", "Défaussez les points d'influences présents sur l'Embuscade puis gagnez 1 point d'influence. Défaussez l'Embuscade ou ")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += 1
        file = Game.get_top_cards()
        Game.discard(Carte.pos)

    def onDeath(self, Player, Game, CarteWhoKill, Carte):
        Game.discard(CarteWhoKill.pos)
        Game.discard(Carte.pos)
        Player.ptsinflu += 4
    
    
class Complot(Types):
    def __init__(self):
        super().__init__(9, "Complot", "Gagnez le double de point d'influence présents sur le Complot. Défaussez le Complot")

    def capacite(self,Player,Game, Carte):
        Player.ptsinflu += (Carte.ptsinflu)
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
    
    def __str__(self):
        return "Shown : "+ str(self.shown)+", Couleur : "+ self.couleur+", Type : " +  str(self.type)
    
    def capacite(self,game):
        if self.pos == -1 or not self.shown:
            print("can't use card ")
            return 
        player = game.get_player(self.idPlayer)
        self.type.capacite(player,game)

types : list[Types] = [Archer(), Soldat(), Espion(), Heritier(), Assassinat(), DecretRoyal(),
                       Embuscade(), Complot(), Changeforme(), Seigneur()]

def full_deck(joueur):
    out = []
    for e in types:
        out.append(Carte(e).set_player(joueur))
    return out
    