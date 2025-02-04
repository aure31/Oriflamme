import socket

class packet:
    def send(self,conn:socket.socket):
        pass

    def decode(code:bytes):
        return code.decode()

class pseudo_packet:
    def __init__(self,code:str):
        self.code = code

    def send(self,conn:socket.socket):
        conn.send(self.code.encode())
    
    
def get_packet(code):
    return packet()