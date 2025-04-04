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
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.winner = data[0]

    def handle(self):
        pass

class ClientBoundColorsPacket(ClientBoundDataPacket):
    def __init__(self, data: list[str]):
        super().__init__(data)
        self.colors = [(data[i][0], data[i][1:]) for i in range(len(data))]

    def handle(self):
        l.game.setPlayersColor(self.data)

# game packet
class ClientBoundGameHandPacket(ClientBoundDataPacket):
    def __init__(self, data: list[str]):
        super().__init__(data)
        print("Debug - Receiving cards:", self.data)
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
        self.player = int(data[3])

    def handle(self):
        l.game.addCardFile(self.id,self.pos,self.player)

class ClientBoundSetPlayerPtsPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.pts = int(data[0])
        self.player = int(data[1])

    def handle(self):
        l.game.getPlayer(self.player).ptsinflu = self.pts


class ClientBoundAddCardPtsInfluPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.pts = int(data[0])
        self.pos = int(data[1])

    def handle(self):
        l.game.file_influence[self.pos][-1].ptsinflu = self.pts

class ClientBoundDiscardCardPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.pos = int(data[0])

    def handle(self):
        l.game.removeCardFile(self.pos)
    
# interaction packet
class ClientBoundChoseToShowPacket(ClientBoundPacket):
    def handle(self):
        l.game.showCard()

class ClientBoundChoseToPlayPacket(ClientBoundPacket):
    def handle(self):
        pass

def getClientBoundPacket(data:bytes) -> list[ClientBoundPacket]:
    print("client : clientboundget :",data)
    result = []
    list = utils.unparse(data,True)
    for id,decode in list:
        packet = clientBoundPacketList[id]
        if issubclass(packet,ClientBoundDataPacket):
            result.append(packet(decode))
        else :
            result.append(packet())
    return result
    
clientBoundPacketList = [
    ClientBoundMessagePacket,
    ClientBoundPlayerListPacket,
    ClientBoundGameStartPacket,
    ClientBoundColorsPacket,
    ClientBoundGameEndPacket,
    ClientBoundGameHandPacket,
    ClientBoundShowCardPacket,
    ClientBoundPlayCardPacket,
    ClientBoundSetPlayerPtsPacket,
    ClientBoundAddCardPtsInfluPacket,
    ClientBoundDiscardCardPacket,
    ClientBoundChoseToPlayPacket,
    ClientBoundChoseToShowPacket
]

utils.clientBoundList = [issubclass(packet,ClientBoundDataPacket) for packet in clientBoundPacketList]
