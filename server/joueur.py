import packet.serverbound as sb
from .cartes import Carte
from .client import Client
import random


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
        self.ptsinflu = 1
        self.defausse = []
        
    def get_name(self):
        return self.nom

    def jouer(self,game) -> tuple[Carte,int]:
        cards = ", ".join([str(e.type) for e in self.cartes ])
        index = eval(input("Choisissez une carte parmis :\n"+cards+"\nChoix : "))
        carte= self.cartes.pop(index)
        cards : list[str] =[str(e) for e in game.get_top_cards()]
        slot = eval(input("Plateau : \n"+"\n".join(cards)+"\n" + "Choisissez la position entre -2 et -1 (Gauche / Droite)"+ "\n"))
        return carte,slot

    def retourner(self,index:int):
        self.client.send(sb.ServerBoundShowCardPacket(index)) 
        self.client.server.game.event.wait()
        self.client.server.game.event.clear()
    
    def choix_adj(self):
        return random.choice[-1, 1] 
    
    def choix_partout(self, Game):
        return random.randint(0, self.get_file_size())
    
    def encode(self):
        return str(self.id)+self.nom

    def decode(self):
        pass
    
    