import socket
import enum
import utils

#ClientBound server -> client
#ServerBound client -> server

class ClientBoundPacket:
    def get_id(self):
        return clientBoundPacketList.index(self.__class__)
    
    def send(self,conn:socket.socket):
        conn.send(clientBoundPacketList.index(self.__class__))

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,*data:str):
        self.data = data

    def send(self, conn):
        packet = utils.parser()
        conn.send(packet)

class ClientBoundIdPacket(ClientBoundPacket):
    def __init__(self,id:int):
        self.id = id

    def send(self,conn:socket.socket):
        conn.send(bytes([self.id]))

class ClientBoundMessagePacket(ClientBoundDataPacket):
    def __init__(self, message:str):
        super().__init__(message)

class clientBoundPlayerJoinPacket(ClientBoundDataPacket):
    def __init__(self, name:str,color:str):
        super().__init__(name)

class CLientBoundGameStartPacket(ClientBoundPacket):
    pass

class ClientBoundGameEndPacket(ClientBoundDataPacket):
    def __init__(self, winner:str):
        super().__init__(winner)
    
# game packet
class ClientBoundGameHandPacket(ClientBoundDataPacket):
    def __init__(self,card:list[str]):
        super().__init__(card)
        self.card = card

class ClientBoundShowCardPacket(ClientBoundDataPacket):
    def __init__(self,id:int, card:str,player:str):
        super().__init__(id,card,player)
        self.id = id
        self.card = card
        self.player = player

class ClientBoundPlayCardPacket(ClientBoundDataPacket):
    def __init__(self,id:int, pos:int, card:str, player:str):
        super().__init__(id,pos,card,player)
        self.id = id
        self.pos = pos
        self.card = card
        self.player = player

# interaction packet
class ClientBoundChoseToShowPacket(ClientBoundPacket):
    pass

class ClientBoundChoseToPlayPacket(ClientBoundPacket):
    pass
    
    
def getClientBoundPacket(id:int,data:str = "") -> ClientBoundPacket:
    id = data[0]
    packet = clientBoundPacketList[id]
    if issubclass(packet,ClientBoundDataPacket):
       return packet(data)
    else :
        return packet()

clientBoundPacketList = [ClientBoundMessagePacket,clientBoundPlayerJoinPacket,CLientBoundGameStartPacket,ClientBoundGameEndPacket,ClientBoundGameHandPacket,ClientBoundShowCardPacket,ClientBoundPlayCardPacket,ClientBoundChoseToShowPacket,ClientBoundChoseToPlayPacket]
