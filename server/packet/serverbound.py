import utils.utils as utils
import server.packet.clientbound as cb
import threading as th


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
        print(data)
        self.name = data[0]

class ServerBoundMessagePacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.message = data[0]

    def handle(self, client):
        print("server : message get :",self.message, flush=True)
        client.server.broadcast(cb.ClientBoundMessagePacket(self.message),[client.id])
    
class ServerBoundGameStartPacket(ServerBoundPacket):
    def handle(self, client):
        print("server : game start get")
        thread = th.Thread(name="game",target=client.server.game.start_game)
        client.server.broadcast(cb.ClientBoundGameStartPacket())
        client.server.startTread(thread)


class ServerBoundPlayCardPacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.pos = int(data[1])

    def handle(self, client):
        player = client.server.game.get_player(client.id)
        # TODO gere les operation
        client.server.game.event.set()
        client.server.broadcast(cb.ClientBoundPlayCardPacket(player.cartes[self.id].type.id,self.pos,player.id),[client.id])
        client.server.game.add_card(client.id,player.cartes[self.id],self.pos)
        player.cartes.pop(self.id)
        print("server : play card get :",self.card, flush=True)

class ServerBoundShowCardPacket(ServerBoundDataPacket):
    def __init__(self,data:list[str]):
        super().__init__(data)
        self.id = int(data[0])
        self.state = bool(int(data[1]))

    def handle(self, client):
        client.server.game.show_card(self.id,self.state)
        client.server.game.event.set()


def getServerBoundPacket(data:bytes) -> list[ServerBoundPacket]:
    print("server : serverboundget :",data)
    result = []
    list = utils.unparse(data,False)
    for id,decode in list:
        packet = serverBoundPacketList[id]
        if issubclass(packet,ServerBoundDataPacket):
            result.append(packet(decode))
        else :
            result.append(packet())
    return result
    
serverBoundPacketList = [
    ServerBoundPseudoPacket,
    ServerBoundMessagePacket,
    ServerBoundGameStartPacket,
    ServerBoundPlayCardPacket,
    ServerBoundShowCardPacket
]