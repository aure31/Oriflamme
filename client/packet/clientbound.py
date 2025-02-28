
import loader as l

#client_bound server -> client
#server_bound client -> server

class ClientBoundPacket:
    def get_id(self):
        return clientboundPacketList.index(self.__class__)
    
    def handle(self):
        pass

class ClientBoundDataPacket(ClientBoundPacket):
    def __init__(self,data:str):
        self.data = data.split("&;")

class ClientBoundReceiveMessagePacket(ClientBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.message = self.data[0]

    def handle(self):
        l.chat.addMessage(self.message)

def getClientBoundPacket(data:bytes) -> ClientBoundPacket:
    id = data[0]
    print(id)
    packet = clientboundPacketList[id]
    decode = data[1:].decode("utf-8")
    if len(data) > 1 :
       return packet(decode)
    else :
        return packet()
    
clientboundPacketList : list[ClientBoundPacket.__class__] = [ClientBoundReceiveMessagePacket]