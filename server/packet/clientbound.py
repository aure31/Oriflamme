import socket
import utils.utils as utils

#ClientBound server -> client
#ServerBound client -> server

class ClientBoundPacket:
    def get_id(self):
        return clientBoundPacketList.index(self.__class__)
    
    def send(self,conn:socket.socket):
        conn.send(bytes([clientBoundPacketList.index(self.__class__)]))

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,*data:str,datas:list[str] = None ):
        if datas is not None:
            self.data = datas
        else:
            self.data = data

    def send(self, conn):
        packet = utils.parser(self.get_id(),self.data)
        conn.send(packet)

class ClientBoundDataListPacket(ClientBoundDataPacket):
    def __init__(self,datas:list):
        endode_datas = []
        for data in datas:
            endode_datas.append(data.encode())
        super().__init__(datas=endode_datas)

class ClientBoundIdPacket(ClientBoundPacket):
    def __init__(self,id:int):
        self.id = id

    def send(self,conn:socket.socket):
        conn.send(bytes([self.id]))

class ClientBoundMessagePacket(ClientBoundDataPacket):
    def __init__(self, message:str):
        super().__init__(message)

class ClientBoundPlayerListPacket(ClientBoundDataListPacket):
    def __init__(self, datas:list):
        super().__init__(datas)

class ClientBoundGameStartPacket(ClientBoundPacket):
    pass

class ClientBoundColorsPacket(ClientBoundDataPacket):  # Changé de ClientBoundDataListPacket à ClientBoundDataPacket
    def __init__(self, datas: list[tuple[int, str]]):
        # Convertir directement en strings, sans encoder
        formatted_data = [str(data[0]) + data[1] for data in datas]
        super().__init__(*formatted_data)  # Utiliser *formatted_data au lieu de formatted_data comme liste

# game packet
class ClientBoundGameEndPacket(ClientBoundDataPacket):
    def __init__(self, winner:str):
        super().__init__(winner)

class ClientBoundGameHandPacket(ClientBoundDataListPacket):
    def __init__(self,card:list):
        super().__init__(card)
        self.card = card

class ClientBoundShowCardPacket(ClientBoundDataPacket):
    def __init__(self,id:int,player:str):
        super().__init__(id,player)
        self.id = id
        self.player = player

class ClientBoundSetPlayerPtsPacket(ClientBoundDataPacket):
    def __init__(self,pts:int,player:str):
        super().__init__(pts,player)
        self.pts = pts
        self.player = player

class ClientBoundAddCardPtsInfluPacket(ClientBoundDataPacket):
    def __init__(self,pts:int,pos:int):
        super().__init__(pts,pos)
        self.pts = pts
        self.pos = pos

class ClientBoundDiscardCardPacket(ClientBoundDataPacket):
    def __init__(self,pos:int):
        super().__init__(pos)
        self.pos = pos

class ClientBoundPlayCardPacket(ClientBoundDataPacket):
    def __init__(self,id:int, pos:int, card:str, player:str):
        super().__init__(id,pos,card,player)
        self.card_id = id
        self.pos = pos
        self.playerid = player

# interaction packet
class ClientBoundChoseToPlayPacket(ClientBoundPacket):
    pass

class ClientBoundChoseToShowPacket(ClientBoundPacket):
    pass    
    
def getClientBoundPacket(id:int,data:str = "") -> ClientBoundPacket:
    print("client : clientboundget :",data)
    id = data[0]
    packet = clientBoundPacketList[id]
    if issubclass(packet,ClientBoundDataPacket):
       return packet(data)
    else :
        return packet()

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
