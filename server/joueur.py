import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .cartes import Carte
from .client import Client
import random
import pygame

pygame.init()

#chat_img = pygame.image.load("client/assets/chat.png")

class Action:
    def run():
        return

class Joueur:
    def __init__(self, nom:str,client:'Client'):
        self.client = client
        self.nom = nom
        self.couleur = None
        self.id = client.id
        self.cartes : list[Carte] = []
        self.defausse = []
        self.ptsinflu = 1
        # self.chat = Chat()
        
    def get_name(self):
        return self.nom

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
    

# class Chat:
#     def __init__(self):
#         self.messages = []

#     def affiche(self, surface):
#         surface.blit(chat_img, (0,290))
#         for mess in self.messages:
#             mess.affiche(surface, 10, 830 - self.messages.index(mess) * 30)

#     def envoyer(self, message):
#         if message == "":
#             pass
#         elif message[0] == '/':
#             self.messages.insert(0, Texte(message, (255,247,0), None, 20))
#         elif message[0] == '@':
#             self.messages.insert(0, Texte(message, (43,185,0), None, 20))
#         else:
#             self.messages.insert(0, Texte(message, (255,255,255), None, 20))
#         if len(self.messages) > 19:
#             self.messages.pop()