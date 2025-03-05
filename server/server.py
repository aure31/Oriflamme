import socket
import threading as th
from .packet.clientbound import *
from .packet.serverbound import *
from .Joueur import Joueur
from .game import Game
from .client import Client
        

class Server :
    used_ports = []
    def __init__(self, port:int =5555, ip:str = "127.0.0.1"):
        self.port = port if port not in Server.used_ports else 5555+len(Server.used_ports)
        self.ip = ip
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadlist : list[th.Thread] = []
        self.lastpid = 0
        self.stopevent = th.Event()
        try:
            self.soket.bind((self.ip, port))
        except socket.error as e:
            print(str(e))
        self.soket.listen(5)
        self.game = Game()
        thread = th.Thread(name="connlistener",target=self.connectionListener)
        thread.start()
        self.threadlist.append(thread)  


    def connectionListener(self):
        while not self.stopevent.is_set():
            try:
                print("Server : En attente de nouvelle connexion...")
                conn, addr = self.soket.accept()
                print("Server : Connecté à : ", addr)
                self.connection(conn,addr)
            except:
                print("Server : Erreur de connexion")
            
    def connection(self,conn:socket.socket,ip):
        try:
            client = Client(conn,ip,self.lastpid,self)
            self.lastpid += 1
            packet : ServerBoundPseudoPacket = client.sendRecv(ClientBoundIdPacket(client.id))
            player = Joueur(packet.name,client)
            self.game.join_player(player)
            self.threadlist.append(client.thread)
            client.thread.start()
        except Exception as e:
            print("Server : Erreur creation", e)

    def broadcast(self,packet:ClientBoundPacket,ignored:list[int] = []):
        for player in self.game.players:
            if player.client.id not in ignored:
                player.client.send(packet)
                print("broadcast : sent packet to player :",player.client.id)
    
    def stop(self):
        print("stop")
        self.soket.close()
        self.stopevent.set()
        for t in self.threadlist:
            t.join()
        self.threadlist = []
        print("Server stopped")


