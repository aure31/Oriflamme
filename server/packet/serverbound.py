import socket
import utils


#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverBoundPacketList.index(self.__class__)
    
    def handle(self,client):
        pass

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,data:list[str]):
        self.data = data
        

class ServerBoundPseudoPacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.name = data

class ServerBoundMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.message = data[0]

    def handle(self, client):
        print("server : message get :",self.message, flush=True)
        import server.packet.clientbound as cp
        client.server.broadcast(cp.ClientBoundMessagePacket(self.message),[client.id])
    
class ServerBoundGameStartPacket(ServerBoundPacket):
    
    def handle(self, client):
        print("server : game start get")
        import server.packet.clientbound as cp
        client.server.broadcast(cp.ClientBoundGameStartPacket(),[client.id])


class ServerBoundPlayCardPacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.pos = int(data[1])
        self.card = data[2]
        self.player = data[3]

    def handle(self, client):
        print("server : play card get :",self.card, flush=True)

class ServerBoundShowCardPacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.card = data[1]
        self.player = data[2]

    def handle(self, client):
        print("server : show card get :",self.card, flush=True)

def getServerBoundPacket(data:bytes) -> ServerBoundPacket:
    print("server : serverboundget :",data)
    id,decode = utils.unparse(data)
    packet = serverBoundPacketList[id]
    if issubclass(packet,ServerBoundDataPacket) :
       return packet(decode)
    else :
        return packet()
    
serverBoundPacketList = [
    ServerBoundPseudoPacket,
    ServerBoundMessagePacket,
    ServerBoundGameStartPacket,
    ServerBoundPlayCardPacket,
    ServerBoundShowCardPacket
]