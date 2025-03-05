from network import Network
from packet.serverbound import ServerBoundPseudoPacket

class Joueur:
    def __init__(self, nom:str, network:Network):
        self.nom = nom
        self.network = network
        network.send(ServerBoundPseudoPacket(nom))
        self.couleur = None
        self.deck = []
        self.defausse = []
        self.ptsinflu = 1