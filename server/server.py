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

def start_server():
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
            reply = data.decode("utf-8")

            if not data:
                print("Déconnecté")
                break
            else:
                print("Reçu : ", reply)
                print("Envoi : ", reply)
                conn.sendall(str.encode(reply))
            print("boucle")
        except:
            break
    
    print("Connexion perdue")
    conn.close()


def test():
    print("test")

