import socket
import threading as th
import packet.clientbound as cb
from .packet.serverbound import *
from .joueur import Joueur
from .game import Game
from .client import Client
        

class Server :
    used_ports = []
    def __init__(self, port:int =5555, ip:str = "localhost"):
        self.port = port if port not in Server.used_ports else 5555+len(Server.used_ports)
        self.ip = ip
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
            except Exception as e:
                print("Server : Erreur de connexion :",e)
            
    def connection(self,conn:socket.socket,ip):
        try:
            client = Client(conn,ip,self.lastpid,self)
            self.lastpid += 1
            packet : ServerBoundPseudoPacket = client.sendRecv(cb.ClientBoundIdPacket(client.id))
            player = Joueur(packet.name,client)
            self.game.join_player(player)
            self.threadlist.append(client.thread)
            client.thread.start()
        except Exception as e:
            print("Server : Erreur creation", e)

    def broadcast(self,packet:cb.ClientBoundPacket,ignored:list[int] = []):
        for player in self.game.players:
            if player.client.id not in ignored:
                player.client.send(packet)
                print("broadcast : sent packet to player :",player.client.id)
    
    def stop(self):
        
        # Vérifier si le socket est encore valide et connecté
        try:
            # Vérifie si le socket est connecté en essayant de récupérer son état
            self.soket.getpeername()
            self.soket.shutdown(socket.SHUT_RDWR)
        except (OSError, socket.error):
            # Ignore les erreurs si le socket n'est pas connecté
            print("Server : Socket not connected")
        finally:
            self.soket.close()
        self.stopevent.set()
        for t in self.threadlist:
            t.join()
        self.threadlist = []
        print("Server stopped")


