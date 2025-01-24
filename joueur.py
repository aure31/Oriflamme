import pygame as p
from cartes import Carte
import random

class Action:
    def run():
        return

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
    
    def action(self):
        input_rdm = bool(random.randint(0,1))
        return input_rdm
    
    def choiceAjd(self):
        return random.choice[-1, 1] 
    
    def choiceEvrywhere(self, Game):
        return random.randint(0, Game.get_file_size())