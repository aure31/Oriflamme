import socket
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

server_alive = True
list_joueurs = []






def start_server():
    global server_alive
    if not server_alive:
        print("Server already running")
        return
    server = get_ip_address()
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(5)
    print("En attente de connexion...")
    server_alive = True
    while server_alive:
        conn, addr = s.accept()
        print("Connecté à : ", addr)
        start_new_thread(threaded_client, (conn,))






def threaded_client(conn:socket.socket):
    conn.send(str.encode("Connecté"))

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            print(1)
            reply = data.decode("utf-8")
            print(2)
            print(data, reply)
            print(3)

            if not data:
                pass
            if reply == "quit":
                break
            else:
                conn.sendall(str.encode(reply+" has join the game"))
        except:
            print("pas de données")
            #break
    
    print("Connexion perdue")
    conn.close()







def test():
    print("test")

def stop_server():
    server_alive = False


