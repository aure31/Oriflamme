import socket
import utils


#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverboundPacketList.index(self.__class__)
    
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
        client.server.broadcast(cp.CLientBoundGameStartPacket(),[client.id])


def getServerBoundPacket(data:bytes) -> ServerBoundPacket:
    print("server : serverboundget :",data)
    id,decode = utils.unparse(data)
    packet = serverboundPacketList[id]
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