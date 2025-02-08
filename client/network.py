import socket
import threading as th
from packet.serverbound import ServerBoundPacket,ServerBoundPseudoPacket

class Network:
    def __init__(self, ip, port,name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.stop_event = th.Event()
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()
        self.thread = th.Thread(name="clientpacketlistner",target=self.packetListener)
        self.thread.start()
        self.data = None
        self.send(ServerBoundPseudoPacket(name))

    def connect(self):
        print("client : Connexion à "+self.server)
        print("client : addresse "+str(self.addr))
        self.client.connect(self.addr)
        print("client : Connexion réussie")
        return self.client.recv(2048)[0]
    
    def packetListener(self):
        while not self.stop_event.is_set():
            print("client : stop_event : "+str(self.stop_event.is_set()))
            try:
                self.data = self.client.recv(2048).decode()
            except:
                break

    def send(self, packet:ServerBoundPacket):
        packet.send(self.client)

    def sendRecv(self, data):
        self.send(data)
        return self.packetListener()

    def disconect(self):
        self.client.close()
        self.stop_event.set()
        self.thread.join()
        print("client : Déconnexion")



def is_valid_ip(ip_str):
    parts = ip_str.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def is_port(num_str):
    return num_str.isdigit() and 0 <= int(num_str) <= 65535