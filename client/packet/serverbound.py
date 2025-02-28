import socket

#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def send(self,conn:socket.socket):
        conn.send(serverBoundPacketList.index(self.__class__))

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,*data):
        self.data = "&;".join(data)

    def send(self, conn):
        packet = bytearray(len(self.data)+1)
        packet[0] = serverBoundPacketList.index(self.__class__)
        packet[1:] = self.data.encode("utf-8")
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
    id = data[0]
    packet = serverBoundPacketList[id]
    if issubclass(packet,ServerBoundDataPacket):
       return packet(data)
    else :
        return packet()

serverBoundPacketList = [ServerBoundPseudoPacket,ServerBoundMessagePacket]
