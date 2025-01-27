from joueur import Joueur
from cartes import Carte,full_deck,colors
import random
import time

states={}



class Game:
    def __init__(self):
        self.file_influence :list[list[Carte]] = [[]]
        self.players:list[Joueur] = []
        self.state = "waiting"
        self.first_player = -1
        self.color = colors.copy()
        self.tour = 0

    def random_color(self):
        return self.color.pop(random.randint(0,len(self.color)))

    def join_player(self,nom):
        if self.state == "waiting":
            self.players.append(
                Joueur(nom,self.random_color(),len(self.players)))
            print(f"{nom} join the game")

    def start_game(self):
        for p in self.players :
            self.gen_deck(p)
        self.first_player = random.randint(0,len(self.players))
        self.state="start"
        print("game started")
        time.sleep(1)
        self.placement()
            



    def add_card(self,idPlayer,card,slot):
        if slot == -1:
            self.file_influence.append(card)
        elif slot == -2:
            self.file_influence.insert(0,card)
        elif slot in range(len(self.file_influence)) and self.file_influence[slot][0].idPlayer == idPlayer:
            self.file_influence[slot].append(card)
        else:
            raise ValueError
        
    def get_top_cards(self):
        result = []
        for lst in self.file_influence:
            result.append(lst[-1])
        return result
    
    def get_card(self,index) -> Carte :
        return self.file_influence[index][-1]
    
    def placement(self):
        self.tour +=1
        for p in self.players:
            print("A "+p.nom+" de joué !")
            card ,slot = p.play_card(self)
            self.add_card(p.id,card,slot)
        time.sleep(1)
        self.end_round()
            
 
    #phase a la fin du tours
    def end_round(self):
        for lst in self.file_influence:
            card = lst[-1]
            if card.shown:
                card.capacite(self)
                continue
            #retourne ou non la carte
            player = self.get_player(card.idPlayer)
            act = player.action()
            if act:
                card.capacite(self)
                player.ptsinflu += card.ptsinflu
            else :
                card.ptsinflu+=1
        if self.tour == 6:
            self.end_partie()
        else:
            self.placement()

    def end_partie(self):
        print("end")
            
    def get_file_size(self):
        return len(self.file_influence)

    def end_turn(self):
        self.state = "end"

    def get_player(self,idPlayer) -> Joueur:
        return self.players[idPlayer]
    

    def discard(self, cardPos : int):
        sous_lst=len(self.file_influence[cardPos])
        card = None
        if sous_lst == 1:
            card = self.file_influence.pop(cardPos)[0]
        else :
            card = self.file_influence[cardPos].pop()
        player = self.get_player(card.idPlayer)
        player.defausse.append(card)
        if(card.type.id == 8): Carte.type.onDeath(Game.get_player(card.idPlayer), Game, Carte, card)

    def gen_deck(player:Joueur):
        out = full_deck(player)
        defausse = []
        for i in range(3):
            defausse.append(out.pop(random.randrange(len(out))))
        player.cartes = out
        player.defausse = defausse