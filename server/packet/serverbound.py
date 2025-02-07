import socket

#client_bound server -> client
#server_bound client -> server

class ServerBoundPacket:

    def __init__(self):
        self.value = None

    def __init__(self,code:bytes):
        self.value = ServerBoundPacket.decode(code)

    def getServerBoundPacket():
        pass

    def decode(code:bytes):
        return code.decode()
    
def getServerBoundPacket(data:bytes) -> ServerBoundPacket:
    id = data[0]
    packet = serverboundPacketList[id]
    if len(data) > 1 :
       return packet.
    else :
        return packet.__init__()
    
serverboundPacketList : list[ServerBoundPacket.__class__] = []