from joueur import Joueur
from cartes import Carte,full_deck
import random

states={}



class Game:
    def __init__(self,players:list):
        self.file_influance :list[list[Carte]] = [[]]
        self.players:dict[int:Joueur] = players
        self.state = "start"

    def start_game(self):
        for p in self.players :
            self.gen_deck(self.players[p])

    def add_card(self,idPlayer,card,slot):
        if slot == -1:
            self.file_influance.append(card)
        elif slot == -2:
            self.file_influance.insert(0,card)
        elif slot in range(len(self.file_influance)) and self.file_influance[slot][0].idPlayer == idPlayer:
            self.file_influance[slot].append(card)
        else:
            raise ValueError
        
    def get_top_card(self):
        result = []
        for lst in self.file_influance:
            result.append(lst[-1])
        return result
    
    def get_card(self,index) -> Carte :
        return self.file_influance[index][-1]

    def play_round(self):
        for lst in self.file_influance:
            card = lst[-1]
            if card.shown:
                card.capacite(self)
                continue
            player = self.get_player(card.idPlayer)
            act = player.action()
            if act:
                card.capacite(self)

    def end_turn(self):
        self.state = "end"

    def get_player(self,idPlayer) -> Joueur:
        return self.players[idPlayer]


    def gen_deck(player:Joueur):
        out = full_deck(player)
        defausse = []
        for i in range(3):
            defausse.append(out.pop(random.randrange(len(out))))
        player.cartes = out
        player.defausse = defausse