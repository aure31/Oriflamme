import socket
import server.game as g
from _thread import *
import sys 

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

def start_server():
    global server_alive
    if server_alive:
        print("Server already running")
        return
    server = get_ip_address()
    port = 5555
    game = g.Game()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(5)
   
    server_alive = True
    while server_alive:
        print("En attente de nouvelle connexion...")
        conn, addr = s.accept()
        print("Connecté à : ", addr)
        server_thread.append(start_new_thread(threaded_client, (conn,)))
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


