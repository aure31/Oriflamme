import pygame as p
from card import HandCard,PlayCard
import loader as l
from joueur import Joueur
from packet.serverbound import ServerBoundPlayCardPacket

class Game():
    game = None
    def __init__(self,itselfplayer:Joueur):
        self.itself = itselfplayer
        self.joueurs = {}
        self.cartes = []
        self.file_influence : list[list[PlayCard]] = []
        self.tour = 0
        Game.game = self

    def setPlayersColor(self,colors:list[str]):
        for i in range(len(colors)):
            self.joueurs[i].couleur = colors[i]

    def setPlayerList(self,playerlist:list[str]):
        self.joueurs = { int(joueur[0]) : Joueur.decode(joueur) for joueur in playerlist }

    def get_player(self,id:int) -> Joueur:
        if id is None:
            return self.itself
        for joueur in self.joueurs:
            if joueur.id == id:
                return joueur
        return None

    def setHand(self,hand:list[str]):
        if self.itself.couleur is None:
            raise ValueError("client : need to set color before setting the hand")
        self.cartes = [HandCard(int(e[0]),self.itself.couleur) for e in hand]

    def add_card_file(self, id_carte : int, pos : int , id_joueur : int = None) -> PlayCard:
        joueur = self.get_player(id_joueur)
        carte = HandCard(id_carte,joueur.couleur).toPlayCard(joueur.id)
        self.file_influence.insert(pos,carte)
        return carte

    def remove_card_file(self, pos : int):
        self.file_influence.pop(pos)

    def play_card(self,hand_pos : int, new_pos : int):
        card = self.cartes[hand_pos]
        self.file_influence.insert(new_pos,card.toPlayCard())
        self.cartes.pop(hand_pos)
        ServerBoundPlayCardPacket(card.type.id,str(new_pos)).send(l.network)


    def parse_pos(self,pos:int) -> int:
        if pos == -1:
            return len(self.file_influence)
        elif pos == -2:
            return 0
        elif pos >= 0 and pos < len(self.file_influence) and self.file_influence[pos][-1].idPlayer == self.itself.id :
            return pos
