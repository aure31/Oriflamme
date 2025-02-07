import socket

#client_bound server -> client
#server_bound client -> server
class packet:
    def send(self,conn:socket.socket):
        pass

    def decode(code:bytes):
        return code.decode()

class server_pseudo_packet:

    def send(self,conn:socket.socket):
        conn.send(self.code.encode())


class client_pseudo_packet:
    def __init__(self,code):
        self.code = code
    
    def get_pseudo(self):
        return self.code
    
    def get_lvl(self):
        return 0
    
    
def get_packet(code):
    return packet()