from joueur import Joueur
from cartes import Carte
import random

states={}

full_deck=[Carte()]

class Game:
    def __init__(self,players:list):
        self.file_influance :list[list[Carte]] = [[]]
        self.players:list[Joueur] = players
        self.state = "start"

    def start_game(self):
        for p in self.players :
            self.gen_deck()

    def add_end(self,idPlayer,card):
        self.file_influance.append(card)
        self.players[idPlayer].play_card(card)
    
    def add_start(self,idPlayer,card):
        self.file_influance.insert(0,card)
        self.players[idPlayer].play_card(card)
    
    def add_on_top(self,idPlayer,card,index):
        if index not in range(len(self.file_influance)) or self.file_influance[index][0]:
            return
        self.file_influance.insert(0,card)
        self.players[idPlayer].play_card(card)

    def end_turn(self):
        self.state = "end"


    def gen_deck(player:Joueur):
        out = [i for i in range(10)]
        defausse = []
        for i in range(3):
            defausse.append(out.pop(random.randrange(len(out))))
        player.cartes = out
        player.defausse = defausse