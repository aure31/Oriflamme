import socket


#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:
    def get_id(self):
        return serverboundPacketList.index(self.__class__)
    
    def handle(self,client):
        pass

class ServerBoundDataPacket(ServerBoundPacket):
    def __init__(self,data:str):
        self.data = data.split("&;")

class ServerBoundPseudoPacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.name = data

class ServerBoundMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:str):
        super().__init__(data)
        self.message = data

    def handle(self, client):
        print("server : message get :",self.message, flush=True)
        import server.packet.clientbound as cp
        client.server.broadcast(cp.ClientBoundMessagePacket(self.message),[client.id])
    
def getServerBoundPacket(data:bytes) -> ServerBoundPacket:
    print(data)
    id = data[0]
    #print(id)
    packet = serverboundPacketList[id]
    decode = data[1:].decode("utf-8")
    if len(data) > 1 :
       return packet(decode)
    else :
        return packet()
    
serverboundPacketList : list[ServerBoundPacket.__class__] = [ServerBoundPseudoPacket,ServerBoundMessagePacket]