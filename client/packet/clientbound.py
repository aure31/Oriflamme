import socket

#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverboundPacketList.index(self.__class__)

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,data:str):
        self.data = data.split(";")

class ClientBoundReceiveMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.sender = self.data[0]
        self.message = self.data[1]

def getServerBoundPacket(data:bytes) -> ServerBoundPacket:
    id = data[0]
    print(id)
    packet = serverboundPacketList[id]
    decode = data[1:].decode("utf-8")
    if len(data) > 1 :
       return packet(decode)
    else :
        return packet()
    
serverboundPacketList : list[ServerBoundPacket.__class__] = [ClientBoundReceiveMessagePacket]