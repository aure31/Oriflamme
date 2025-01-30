import pygame as p
from server.cartes import Carte
import random

class Action:
    def run():
        return

class Joueur:
    def __init__(self, nom, couleur,id):
        self.nom = nom
        self.couleur = couleur
        self.id = id
        self.cartes : list[Carte] = []
        self.defausse = []
        self.ptsinflu = 1
        
    

    def play_card(self,game) -> tuple[Carte,int]:
        cards = ", ".join([str(e.type) for e in self.cartes ])
        index = eval(input("choisisez une carte parmis \n"+cards+"\n choix : "))
        carte= self.cartes.pop(index)
        cards : list[str] =[str(e) for e in game.get_top_cards()]

        slot = eval(input("plateau : \n"+"\n".join(cards)+"\n"))
        return carte,slot

    
    def action(self):
        input_rdm = bool(input("retourné ou pas (true or false) : "))
        
        return input_rdm
    
    def choiceAjd(self):
        return random.choice[-1, 1] 
    
    def choiceEvrywhere(self, Game):
        return random.randint(0, Game.get_file_size())
    
    def choiceCard(self,Game):
        return eval(input("choisisé une carte parmis :\n"+", ".join(Game.get_top_cards())+" : "))

    def ask(self,text:str):
        return input(text)