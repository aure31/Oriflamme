import socket
import enum

#ClientBound server -> client
#ServerBound client -> server

class ClientBoundPacket:
    def send(self,conn:socket.socket):
        pass

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,data:str):
        self.data = data

class ClientBoundIdPacket(ClientBoundPacket):
    def __init__(self,id:int):
        self.id = id

    def send(self,conn:socket.socket):
        conn.send(bytes([clientBoundPacketList.index(self.__class__),self.id]))
    
    
def getClientBoundPacket(id:int,data:str = "") -> ClientBoundPacket:
    id = data[0]
    packet = clientBoundPacketList[id]
    if issubclass(packet,ClientBoundDataPacket):
       return packet(data)
    else :
        return packet()

clientBoundPacketList = [ClientBoundIdPacket]
