import loader as l
import utils
import joueur as j
import pygame as p
import game as g

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
        playerlist = []
        playernames = []
        for data in self.data:
            joueur = j.Joueur.decode(data)
            playerlist.append(joueur)
            playernames.append(joueur.nom)
        g.Game.game.joueurs = playerlist
        l.menu.getElement("playerList").setText(playernames)
        print("client : playerlist get :",l.menu.getElement("playerList").elements)

class ClientBoundGameStartPacket(ClientBoundPacket):
    def handle(self):
        l.background = p.transform.scale(l.bg_game, (l.screen_width, l.screen_height))

class ClientBoundGameEndPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.winner = data[0]

    def handle(self):
        pass

# game packet
class ClientBoundGameHandPacket(ClientBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.card = data

    def handle(self):
        pass

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
    ClientBoundGameEndPacket,
    ClientBoundGameHandPacket,
    ClientBoundShowCardPacket,
    ClientBoundPlayCardPacket,
    ClientBoundChoseToShowPacket,
    ClientBoundChoseToPlayPacket
]
