import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.cartes import Carte
from client.classes import *
import random
import pygame

pygame.init()

chat_img = pygame.image.load("client/assets/chat.png")

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
        
    def get_name(self):
        return self.nom

    def play_card(self,game) -> tuple[Carte,int]:
        cards = ", ".join([str(e.type) for e in self.cartes ])
        index = eval(input("Choisissez une carte parmis :\n"+cards+"\nChoix : "))
        carte= self.cartes.pop(index)
        cards : list[str] =[str(e) for e in game.get_top_cards()]
        slot = eval(input("Plateau : \n"+"\n".join(cards)+"\n" + "Choisissez la position entre -2 et -1 (Gauche / Droite)"+ "\n"))
        return carte,slot

    
    def action(self):
        input_rdm = bool(input("Voulez vous la retourner ? (true or false) : "))
        
        return input_rdm
    
    def choiceAjd(self):
        return random.choice[-1, 1] 
    
    def choiceEvrywhere(self, Game):
        return random.randint(0, Game.get_file_size())
    
    def choiceCard(self,Game):
        return eval(input("Choisissez une carte parmis :\n"+", ".join(Game.get_top_cards())+" : "))

    def ask(self,text:str):
        return input(text)
    

class Chat:
    def __init__(self):
        self.messages = []

    def affiche(self, surface):
        surface.blit(chat_img, (0,290))
        for mess in self.messages:
            mess.affiche(surface, 10, 830 - self.messages.index(mess) * 30)

    def envoyer(self, message):
        if message == "":
            pass
        elif message[0] == '/':
            self.messages.insert(0, Texte(message, (255,247,0), None, 20))
        elif message[0] == '@':
            self.messages.insert(0, Texte(message, (43,185,0), None, 20))
        else:
            self.messages.insert(0, Texte(message, (255,255,255), None, 20))
        if len(self.messages) > 19:
            self.messages.pop()