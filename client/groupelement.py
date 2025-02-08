import enum
import loader as l
from classes import Element,Bouton,TextInput,Texte, Chat
import pygame
import error as e
import server.server as s
import Joueur as j
from network import Network, is_valid_ip, is_port

class GroupElement:
    def __init__(self, name):
        self.name = name
        self.elements = {}

    def affiche(self):
        for element in self.elements.values():
            element.affiche(l.window)

