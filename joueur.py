import pygame as p
from cartes import Carte

class Joueur:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
        self.cartes = []
        self.defausse = []
        self.ptsinflu = 1

    def set_id(self,id):
        self.id = id
        return self

    def play_card(self,card:Carte):
        self.cartes.remove(card)