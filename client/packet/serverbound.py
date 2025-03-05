import socket
import utils

#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverBoundPacketList.index(self.__class__)

    def send(self,conn:socket.socket):
        conn.send(serverBoundPacketList.index(self.__class__))

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,*data):
        self.data = data

    def send(self, conn):
        packet = utils.parser(self.get_id(),self.data)
        conn.send(packet)

class ServerBoundPseudoPacket(ServerBoundDataPacket):
    def __init__(self,pseudo:str):
        super().__init__(pseudo)
        self.name = pseudo

class ServerBoundMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.message = data
    
    
def getServerBoundPacket(id:int,data:str = "") -> ServerBoundPacket:
    print("client : serverboundget :",data)
    id = data[0]
    packet = serverBoundPacketList[id]
    if issubclass(packet,ServerBoundDataPacket):
       return packet(data)
    else :
        return packet()

serverBoundPacketList = [ServerBoundPseudoPacket,ServerBoundMessagePacket]
