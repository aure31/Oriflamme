import pygame as p

class Joueur:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
        self.cartes = []
        self.defausse = []
        self.ptsinflu = 1