import pygame as p
from card import HandCard,PlayCard
import loader as l
from joueur import Joueur
from packet.serverbound import ServerBoundPlayCardPacket
from menu import MenuList

class Game():
    game = None
    def __init__(self,id:int,name:str):
        self.itself = Joueur(id,name)
        self.joueurs = {}
        self.cartes = []
        self.file_influence : list[list[PlayCard]] = []
        self.tour = 0
        Game.game = self

    def setPlayersColor(self,colors:list[str]):
        for data in colors:
            self.joueurs[int(data[0])].couleur = data[1:]

    def setPlayerList(self,playerlist:list[str]):
        MenuList.ATTENTE.value.getElement("playerList").setText([e[1:] for e in playerlist])
        self.joueurs = { int(joueur[0]) : Joueur.decode(joueur) for joueur in playerlist }


    def getPlayer(self,id:int) -> Joueur:
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

    def addCardFile(self, id_carte : int, pos : int , id_joueur : int = None) -> PlayCard:
        joueur = self.getPlayer(id_joueur)
        carte = HandCard(id_carte,joueur.couleur).toPlayCard(joueur.id)
        self.insertFile(pos,carte)
        return carte
    
    def insertFile(self,pos:int,card:PlayCard):
        if pos == -1 or pos == -2:
            self.file_influence.insert(self.parsePos(pos),[card])
        else:
            self.file_influence[pos].append(card)

    def removeCardFile(self, pos : int):
        self.file_influence.pop(pos)

    def playCard(self,hand_pos : int, new_pos : int):
        card = self.cartes[hand_pos]
        self.insertFile(new_pos,card.toPlayCard())
        self.cartes.pop(hand_pos)
        ServerBoundPlayCardPacket(card.type.id,str(new_pos)).send(l.network)


    def parsePos(self,pos:int) -> int:
        if pos == -1:
            return len(self.file_influence)
        elif pos == -2:
            return 0
        elif pos >= 0 and pos < len(self.file_influence) and self.file_influence[pos][-1].idPlayer == self.itself.id :
            return pos
        else:
            raise ValueError("client : Invalid position")
