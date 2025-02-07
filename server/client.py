import socket
from .packet.clientbound import ClientBoundPacket
from .packet.serverbound import ServerBoundPacket,getServerBoundPacket

class Client:
    def __init__(self,conn:socket.socket,ip,id:int):
        self.ip = ip
        self.conn = conn
        self.id = id

    def send(self,packet:ClientBoundPacket):
        packet.send(self.conn)

    def sendRecv(self,packet:ClientBoundPacket) -> ServerBoundPacket:
        packet.send(self.conn)
        return getServerBoundPacket(self.conn.recv(2048))