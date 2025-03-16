import socket
import threading as th
from packet.serverbound import ServerBoundPacket,ServerBoundPseudoPacket

class Network:
    def __init__(self, ip, port,name):
        self.name = name
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.stop_event = th.Event()
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print("client : id : "+str(self.id))
        from game import Game
        Game(self.id,self.name)
        self.thread = th.Thread(name="clientpacketlistner",target=self.packetListener)
        self.thread.start()
        self.send(ServerBoundPseudoPacket(name))

    def connect(self):
        print("client : Connexion à "+self.server)
        try:
            self.conn.settimeout(10)  # 10 second timeout
            self.conn.connect(self.addr)
            self.conn.settimeout(None)  # Reset to blocking mode
            print("client : Connexion réussie")
            return self.conn.recv(2048)[0]
        except socket.timeout:
            print("client : Timeout de connexion")
            raise
        except ConnectionRefusedError as e:
            print("client : Connexion refusée :",str(e))
            raise
        except Exception as e:
            print("client : Erreur de connexion inconue:", str(e))
            raise
    
    def packetListener(self):
        from packet.clientbound import getClientBoundPacket
        while not self.stop_event.is_set():
            try:
                data = self.conn.recv(2048)
                if not data:
                    self.disconect()
                    break
                
                packets = getClientBoundPacket(data)
                for packet in packets:
                    packet.handle()
            except socket.timeout as e :
                print("client : Timeout de réception de paquet", e)
                self.disconect()
                break
            except Exception as e:
                print("client : Erreur de réception de paquet", e)
                if not data :
                    print("client : data :",data)
            

    def send(self, packet:ServerBoundPacket):
        packet.send(self.conn)

    def sendRecv(self, data):
        self.send(data)
        return self.conn.recv(2048)

    def disconect(self):
        try:
            # Envoyer un message de déconnexion si possible
            from packet.serverbound import ServerBoundMessagePacket
            self.send(ServerBoundMessagePacket(f"@{self.name} a quitté la partie"))
        except:
            pass
        
        self.stop_event.set()
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
        except:
            pass
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
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
