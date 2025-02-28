import socket
import enum

#ClientBound server -> client
#ServerBound client -> server

class ClientBoundPacket:
    def get_id(self):
        return clientBoundPacketList.index(self.__class__)
    
    def send(self,conn:socket.socket):
        conn.send(clientBoundPacketList.index(self.__class__))

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,*data):
        self.data = "&;".join(data)

    def send(self, conn):
        packet = bytearray(len(self.data)+1)
        packet[0] = clientBoundPacketList.index(self.__class__)
        packet[1:] = self.data.encode("utf-8")
        conn.send(packet)

class ClientBoundIdPacket(ClientBoundPacket):
    def __init__(self,id:int):
        self.id = id

    def send(self,conn:socket.socket):
        conn.send(bytes([self.id]))

class ClientBoundMessagePacket(ClientBoundDataPacket):
    def __init__(self, message:str):
        super().__init__(message)
    
    
def getClientBoundPacket(id:int,data:str = "") -> ClientBoundPacket:
    id = data[0]
    packet = clientBoundPacketList[id]
    if issubclass(packet,ClientBoundDataPacket):
       return packet(data)
    else :
        return packet()

clientBoundPacketList = [ClientBoundMessagePacket]
