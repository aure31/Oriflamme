import loader as l
import utils.utils as utils
from card import HandCard 
import joueur as j
import pygame as p
import game as g
import menu as m

p.init()

#client_bound server -> client
#server_bound client -> server

class ClientBoundPacket:
    def get_id(self):
        return clientBoundPacketList.index(self.__class__)
    
    def handle(self):
        pass

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,data:list[str]):
        self.data = data

class ClientBoundIdPacket(ClientBoundPacket):
    def __init__(self,data:list[str]):
        self.id = int(data[0])

    def handle(self):
        pass

class ClientBoundMessagePacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.message = self.data[0]

    def handle(self):
        l.chat.addMessage(self.message)

class ClientBoundPlayerListPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)

    def handle(self):
        l.game.setPlayerList(self.data)
        print("client : playerlist get :",l.menu.getElement("playerList").elements)

class ClientBoundGameStartPacket(ClientBoundPacket):
    def handle(self):
        print("changement d'arrière plan")
        l.background = l.bg_game
        l.menu = m.MenuList.JEU.value

class ClientBoundGameEndPacket(ClientBoundDataPacket):
    def __init__(self, data:list[str]):
        super().__init__(data)
        self.winner = data[0]

    def handle(self):
        if l.reseau:
            l.reseau.disconect()
            l.reseau = None
        l.menu = MenuList.ACCUEIL.value

class ClientBoundColorsPacket(ClientBoundDataPacket):
    def __init__(self, data: list[str]):
        super().__init__(data)
        # Extraire l'ID du joueur (premier caractère) et la couleur (reste de la chaîne)
        self.colors = [(data[i][0], data[i][1:]) for i in range(len(data))]

    def handle(self):
        l.game.setPlayersColor(self.data)  # Utiliser directement data car setPlayersColor s'attend déjà à ce format

# game packet
class ClientBoundGameHandPacket(ClientBoundDataPacket):
    def __init__(self, data: list[str]):
        super().__init__(data)
        print("Debug - Receiving cards:", self.data)
        # Créer directement les cartes avec l'ID numérique
        self.cards = [int(card_id) for card_id in self.data]

    def handle(self):
        print("Debug - Setting hand with cards:", len(self.cards))
        l.game.setHand(self.cards)

class ClientBoundShowCardPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.card = data[1]
        self.player = data[2]

    def handle(self):
        pass

class ClientBoundPlayCardPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.pos = int(data[1])
        self.card = data[2]
        self.player = data[3]

    def handle(self):
        pass

# interaction packet
class ClientBoundChoseToShowPacket(ClientBoundPacket):
    def handle(self):
        pass

class ClientBoundChoseToPlayPacket(ClientBoundPacket):
    def handle(self):
        pass

def getClientBoundPacket(data:bytes) -> ClientBoundPacket:
    print("client : clientboundget :",data)
    id,decode = utils.unparse(data)
    packet = clientBoundPacketList[id]
    if issubclass(packet,ClientBoundDataPacket):
       return packet(decode)
    else :
        return packet()
    
clientBoundPacketList = [
    ClientBoundMessagePacket,
    ClientBoundPlayerListPacket,
    ClientBoundGameStartPacket,
    ClientBoundColorsPacket,  # Vérifier que c'est dans le même ordre
    ClientBoundGameEndPacket,
    ClientBoundGameHandPacket,
    ClientBoundShowCardPacket,
    ClientBoundPlayCardPacket,
    ClientBoundChoseToPlayPacket,
    ClientBoundChoseToShowPacket
]
