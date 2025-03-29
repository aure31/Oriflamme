from card import HandCard,PlayCard
import loader as l
from joueur import Joueur
from packet.serverbound import ServerBoundPlayCardPacket,ServerBoundShowCardPacket
from menu import MenuList

class Game():
    def __init__(self,id:int,name:str):
        self.itself = Joueur(id,name)
        self.itself.couleur = None
        self.joueurs = {}
        self.cartes = []
        self.file_influence: list[list[PlayCard]] = []
        self.tour = 0
        l.game = self

    def setPlayersColor(self, colors: list[str]):
        for data in colors:
            player_id = int(data[0])
            color = data[1:]
            if player_id == self.itself.id:
                self.itself.couleur = color
            if player_id in self.joueurs:
                self.joueurs[player_id].couleur = color

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

    def setHand(self, cards):
        self.cartes = []
        x_start = 400
        y_position = 800
        spacing = 120
        
        for i, card_id in enumerate(cards):
            try:
                new_card = HandCard(card_id, self.itself.couleur)
                new_card.rect = new_card.img.get_rect()
                new_card.rect.x = x_start + (i * spacing)
                new_card.rect.y = y_position
                self.cartes.append(new_card)
            except Exception as e:
                print(f"Error creating card {i+1}: {str(e)}")

# Actions dans le jeu
    def addCardFile(self, id_carte : int, pos : int , id_joueur : int = None) -> PlayCard:
        joueur = self.getPlayer(id_joueur)
        carte = HandCard(id_carte,joueur.couleur).toPlayCard(joueur.id)
        self.insertFile(pos,carte)
        return carte
    
    def insertFile(self, pos:int, card:PlayCard):
        if pos == -1 or pos == -2:
            print(f"Ajout d'une carte en position {pos}")
            self.file_influence.insert(self.parsePos(pos), [card])
        else:
            print(f"Ajout d'une carte à la pile {pos}")
            self.file_influence[pos].append(card)

    def removeCardFile(self, pos : int):
        self.file_influence.pop(pos)

    def showCard(self,pos : int, shown : bool):
        if shown :
            self.file_influence[pos][-1].setShown(True)
            ServerBoundShowCardPacket(pos).send(l.network)

    def playCard(self,hand_pos : int, new_pos : int):
        card = self.cartes[hand_pos]
        self.insertFile(new_pos,card.toPlayCard())
        self.cartes.pop(hand_pos)
        ServerBoundPlayCardPacket(hand_pos,str(new_pos)).send(l.network)


    def parsePos(self,pos:int) -> int:
        if pos == -1:
            return len(self.file_influence)
        elif pos == -2:
            return 0
        elif pos >= 0 and pos < len(self.file_influence) and self.file_influence[pos][-1].idPlayer == self.itself.id :
            return pos
        else:
            raise ValueError("client : Invalid position")
