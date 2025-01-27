import socket
from _thread import *
import sys 

server = "10.0.1.22"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("En attente de connexion...")

def threaded_client(conn):
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
        except:
            break
    
    print("Connexion perdue")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connecté à : ", addr)

    start_new_thread(threaded_client, (conn,))