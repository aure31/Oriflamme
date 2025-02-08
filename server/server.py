import socket
import threading as th
import sys 
import os
from .packet.clientbound import *
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
            str(e)
        self.soket.listen(5)
        self.game = Game()
        thread =th.Thread(name="connlistener",target=self.connectionListener)
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
                break
            
    def connection(self,conn:socket.socket,ip):
        client = Client(conn,ip,self.lastpid)
        self.lastpid += 1
        packet : ServerBoundPseudoPacket = client.sendRecv(ClientBoundIdPacket(client.id))
        player = Joueur(packet.name,client)
        self.game.join_player(player)
        paketlst = th.Thread(name="player"+str(player.id),target=self.paketListener,args=(player,))
        paketlst.start()
        self.threadlist.append(paketlst)

    def paketListener(self,player:Joueur):
        while not self.stopevent.is_set():
            data = player.client.conn.recv(2048)
            if not data:
                break
            packet = getServerBoundPacket(data)
            if packet.get_id() == 0:
                print("packet 0")
            else:
                print("packet : ",packet.get_id())
    
    def stop(self):
        print("stop")
        self.soket.close()
        self.stopevent.set()
        for t in self.threadlist:
            t.join()
        print("Server stopped")


