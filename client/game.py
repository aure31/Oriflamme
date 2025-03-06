import pygame as p
from card import Card
from joueur import Joueur

class Game():
    game = None
    def __init__(self,itselfplayer):
        self.itself = itselfplayer
        self.joueurs = []
        self.cartes = []
        self.file_influence = []
        self.tour = 0
        Game.game = self

    def add_card_file(self, carte : Card, joueur : Joueur = None):
        if joueur is None:
            joueur = self.itself
        self.file_influence.append(carte)

    def remove_card_file(self, carte : Card, joueur : Joueur):
        pass

    def distribuer(self):
        pass

    def add_card_file(self):
        pass

    def play_card(self):
        pass