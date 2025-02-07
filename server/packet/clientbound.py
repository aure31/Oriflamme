import socket
import enum

#ClientBound server -> client
#ServerBound client -> server

class ClientBoundPacket:
    def send(self,conn:socket.socket):
        pass


class ClientBoundPseudoPacket(ClientBoundPacket):
    def send(self,conn:socket.socket):
        conn.send(clientBoundPacketList.index(self.__class__))
    
    
def getClientBoundPacket(code) -> ClientBoundPacket:
    # Utilise l'index (code) pour récupérer la classe correspondante dans clientBoundPacketList
    packet_class = clientBoundPacketList[code]
    # Instancie et retourne un nouvel objet de cette classe
    return packet_class()

clientBoundPacketList = [ClientBoundPseudoPacket]
