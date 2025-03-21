import socket
import threading as th
from .packet import clientbound as cb
from .packet.serverbound import *
from .joueur import Joueur
from .game import Game
from .client import Client

def get_local_ip():
    #ON NE TOUCHE PAS
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class Server:
    used_ports = []
    def __init__(self, port:int =5555, ip:str = None):
        #ON NE TOUCHE PAS
        self.port = port if port not in Server.used_ports else 5555+len(Server.used_ports)
        self.ip = ip if ip else get_local_ip()
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadlist : list[th.Thread] = []
        self.lastpid = 0
        self.stopevent = th.Event()
        try:
            self.soket.bind((self.ip, port))
        except socket.error as e:
            print("server :error binding :",e)
        self.soket.listen(5)
        self.game = Game(self)
        self.connectionthread = th.Thread(name="connlistener",target=self.connectionListener)
        self.connectionthread.start()

    def startTread(self,thread:th.Thread):
        self.threadlist.append(thread)
        thread.start()

    def connectionListener(self):
        while not self.stopevent.is_set():
            try:
                print("Server : En attente de nouvelle connexion...")
                conn, addr = self.soket.accept()
                print("Server : Connecté à : ", addr)
                self.connection(conn,addr)
            except Exception as e:
                print("Server : Erreur de connexion :",e)
            
    def connection(self,conn:socket.socket,ip):
        try:
            client = Client(conn,ip,self.lastpid,self)
            self.lastpid += 1
            packet : ServerBoundPseudoPacket = client.sendRecv(cb.ClientBoundIdPacket(client.id))[0]
            player = Joueur(packet.name,client)
            self.game.join_player(player)
            self.threadlist.append(client.thread)
            client.thread.start()
        except Exception as e:
            print("Server : Erreur creation", e)

    def broadcast(self,packet:cb.ClientBoundPacket,ignored:list[int] = []):
        for player in self.game.players.values():
            if player.client.id not in ignored:
                player.client.send(packet)
                print("broadcast : sent packet to player :",player.client.id)
    
    def stop(self):
        try :
            # DO NOT TUCHE PLEASE
            self.stopevent.set()
            self.game.stop()
            if self.soket:
                self.soket.close()
            for thread in self.threadlist:
                if thread.is_alive():
                    thread.join()
            self.connectionthread.join()
            self.threadlist = []
            print("Server stopped")
        except Exception as e:
            print("Server : Erreur de fermeture :",e)