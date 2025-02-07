from server.joueur import Joueur
from server.cartes import Carte,full_deck,colors
import random
import time

states={}



class Game:
    def __init__(self):
        self.file_influence :list[list[Carte]] = []
        self.players:list[Joueur] = []
        self.state = "waiting"
        self.first_player = -1
        self.colors = colors.copy()
        self.tour = 0

    def attente(self):
        pass

    def partie(self):
        pass

    def fin(self):
        pass


    