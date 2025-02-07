import socket
from threading import *
import sys 
from packet.clientbound import *
from packet.serverbound import *

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address

server_alive = False
server_thread:list[int] = []

class Client:
    def __init__(self,conn:socket.socket,ip:socket._RetAddress):
        self.ip = ip
        self.conn = conn

    def send(self,packet:ClientBoundPacket):
        packet.send(self.conn)

    def sendRecv(self,packet:ClientBoundPacket) -> ServerBoundPacket:
        self.conn.sendall(data)
        data = self.conn.recv(2048)
        id = reply[0]
        reply = data[1:].decode("utf-8")
        return 
        

class Server :
    def __init__(self,port:int):
        self.port = port
        self.ip = get_ip_address()
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadlist = []
        try:
            self.soket.bind((self.ip, port))
        except socket.error as e:
            str(e)
        self.soket.listen(5)
        self.threadlist.append(Thread(name="connlistener",target=self.connectionListener))


    def connectionListener(self):
        while True:
            print("En attente de nouvelle connexion...")
            conn, addr = self.soket.accept()
            print("Connecté à : ", addr)
            
    def connection(conn:socket.socket,ip:socket._RetAddress):
        client = Client(conn,ip)
        client.sendRecv()

    def paketListener(self,player):

        

def start_server():
    global server_alive
    if server_alive:
        print("Server already running")
        return
    server = get_ip_address()
    port = 5555
    game = g.Game()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    
   
    server_alive = True
   
    stop_server()

def stop_server():
    global server_alive
    server_alive = False

def threaded_client(conn:socket.socket):
    conn.send(str.encode("Connecté"))

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                pass
            if reply == "quit":
                break
            else:
                print("Recu : ", reply)
                conn.sendall(str.encode(reply+" has join the game"))
        except:
            print("server : pas de données")
            #break
    
    print("server : Connexion perdue")
    conn.close()







def test():
    print("test")

def stop_server():
    server_alive = False


