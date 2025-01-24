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

    def add_end(self,idPlayer,card):
        self.file_influance.append(card)
        self.players[idPlayer].play_card(card)
    
    def add_start(self,idPlayer,card):
        self.file_influance.insert(0,card)
        self.players[idPlayer].play_card(card)
    
    def add_on_top(self,idPlayer,card,index):
        if index not in range(len(self.file_influance)) or self.file_influance[index][0].idPlayer != idPlayer:
            return
        self.file_influance[index].append(card)
        self.players[idPlayer].play_card(card)

    def play_round(self):
        for lst in self.file_influance:
            card = lst[-1]
            player = self.get_player(card.idPlayer)
            player.action()

    def end_turn(self):
        self.state = "end"

    def get_player(self,idPlayer) -> Joueur:
        return self.players[idPlayer]
    

    def discard(self, cardPos):
        self.file_influance.pop(cardPos)

    def gen_deck(player:Joueur):
        out = full_deck(player)
        defausse = []
        for i in range(3):
            defausse.append(out.pop(random.randrange(len(out))))
        player.cartes = out
        player.defausse = defausse