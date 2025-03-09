import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .cartes import Carte
from .client import Client
import random
import pygame
import packet.clientbound as cb

pygame.init()


class Action:
    def run():
        return

class Joueur:
    def __init__(self, nom:str , client:Client):
        self.client = client
        self.nom = nom
        self.couleur = None
        self.id = client.id
        self.cartes : list[Carte] = []
        self.defausse = []
        self.ptsinflu = 1
        
    def get_name(self):
        return self.nom
    
    def add_card_file(self) -> tuple[Carte,int]:
        pass

    def jouer(self,game) -> tuple[Carte,int]:
        cards = ", ".join([str(e.type) for e in self.cartes ])
        index = eval(input("Choisissez une carte parmis :\n"+cards+"\nChoix : "))
        carte= self.cartes.pop(index)
        cards : list[str] =[str(e) for e in game.get_top_cards()]
        slot = eval(input("Plateau : \n"+"\n".join(cards)+"\n" + "Choisissez la position entre -2 et -1 (Gauche / Droite)"+ "\n"))
        return carte,slot

    def retourner(self):
        input_rdm = bool(input("Voulez vous la retourner ? (true or false) : ")) 
        return input_rdm
    
    def choix_adj(self):
        return random.choice[-1, 1] 
    
    def choix_partout(self, Game):
        return random.randint(0, self.get_file_size())
    
    def encode(self):
        return str(self.id)+self.nom

    def decode(self):
        pass
    
    