import socket
from .packet.clientbound import ClientBoundPacket
from .packet.serverbound import ServerBoundPacket,getServerBoundPacket
import threading as th

class Client:
    def __init__(self,conn:socket.socket,ip,id:int,server):
        self.ip = ip
        self.conn = conn
        self.id = id
        self.thread = th.Thread(name="client"+str(self.id),target=self.paketListener)
        self.thread.start()
        self.server = server
        self.stopevent = server.stopevent

    def send(self,packet:ClientBoundPacket):
        packet.send(self.conn)

    def sendRecv(self,packet:ClientBoundPacket) -> ServerBoundPacket:
        packet.send(self.conn)
        return getServerBoundPacket(self.conn.recv(2048))
    
    def paketListener(self):
        while not self.stopevent.is_set():
            data = self.conn.recv(2048)
            if not data:
                break
            packet = getServerBoundPacket(data)
            packet.handle(self)
            if packet.get_id() == 0:
                print("packet 0")
            else:
                print("packet : ",packet.get_id())