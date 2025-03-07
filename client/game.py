import pygame as p
from card import HandCard,PlayCard
from joueur import Joueur

class Game():
    game = None
    def __init__(self,itselfplayer:Joueur):
        self.itself = itselfplayer
        self.joueurs = {}
        self.cartes = []
        self.file_influence : list[list[PlayCard]] = []
        self.tour = 0
        Game.game = self

    def setPlayerList(self,playerlist:list[str]):
        for joueur in playerlist:
            self.joueurs.append(Joueur.decode(joueur))

    def get_player(self,id:int) -> Joueur:
        for joueur in self.joueurs:
            if joueur.id == id:
                return joueur
        return None

    def setHand(self,hand:list[str]):
        if self.itself.couleur is None:
            raise ValueError("client : need to set color before setting the hand")
        self.cartes = [HandCard(int(e[0]),self.itself.couleur) for e in hand]

    def add_card_file(self, id_carte : int, pos : int , id_joueur : int = None) -> PlayCard:
        if id_joueur is None:
            id_joueur = self.itself.id
        carte = HandCard(id_carte,joueur.couleur).toPlayCard(joueur.id)
        self.file_influence.insert(pos,carte)
        return carte

    def remove_card_file(self, pos : int):
        self.file_influence.pop(pos)

    def play_card(self,hand_pos : int, new_pos : int):
        card = self.cartes[hand_pos]
        self.file_influence.insert(new_pos,card.toPlayCard())
        self.cartes.pop(hand_pos)


    def parse_pos(self,pos:int) -> int:
        if pos == -1:
            return len(self.file_influence)
        elif pos == -2:
            return 0
        elif pos >= 0 and pos < len(self.file_influence) and self.file_influence[pos][-1].idPlayer == self.itself.id :
            return pos
