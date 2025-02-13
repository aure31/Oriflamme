
import loader as l

#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverboundPacketList.index(self.__class__)
    
    def handle(self):
        pass

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,data:str):
        self.data = data.split("&;")

class ClientBoundReceiveMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.message = self.data[0]

    def handle(self):
        l.chat.addMessage(self.message)

def getClientBoundPacket(data:bytes) -> ServerBoundPacket:
    id = data[0]
    print(id)
    packet = serverboundPacketList[id]
    decode = data[1:].decode("utf-8")
    if len(data) > 1 :
       return packet(decode)
    else :
        return packet()
    
serverboundPacketList : list[ServerBoundPacket.__class__] = [ClientBoundReceiveMessagePacket]