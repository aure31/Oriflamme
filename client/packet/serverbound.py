import socket
import enum

#ClientBound server -> client
#ServerBound client -> server

class ServerBoundPacket:
    def send(self,conn:socket.socket):
        pass

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,data:str):
        self.data = data

class ServerBoundPseudoPacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.name = data

    def send(self,conn:socket.socket):
        packet = bytearray(len(self.name)+1)
        packet[0] = serverBoundPacketList.index(self.__class__)
        packet[1:] = self.name.encode("utf-8")
        conn.send(packet)
    
    
def getClientBoundPacket(id:int,data:str = "") -> ServerBoundPacket:
    id = data[0]
    packet = serverBoundPacketList[id]
    if issubclass(packet,ServerBoundDataPacket):
       return packet(data)
    else :
        return packet()

serverBoundPacketList = [ServerBoundPseudoPacket]
