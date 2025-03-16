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
        self.server = server
        self.stopevent = self.server.stopevent
        

    def send(self,packet:ClientBoundPacket):
        packet.send(self.conn)

    def sendRecv(self,packet:ClientBoundPacket) -> ServerBoundPacket:
        print("packet : sending",flush=True)
        packet.send(self.conn)
        return getServerBoundPacket(self.conn.recv(2048))
    
    def paketListener(self):
        try:
            while not self.stopevent.is_set():
                try:
                    print("server packet : listening player :", self.id)
                    data = self.conn.recv(2048)
                    if not data:
                        print(f"server packet : connection closed {self.id}")
                        break
                    
                    packet = getServerBoundPacket(data)
                    print("packet : handeled", packet.get_id())
                    packet.handle(self)
                except ConnectionResetError:
                    print(f"server packet : connection reset by client {self.id}")
                    break
                except Exception as e:
                    print(f"packet : error handling: {e}")
        finally:
            try:
                self.server.game.left_player(self.id)
                self.conn.close()
            except:
                pass
