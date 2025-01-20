import pygame as p

class Types:
    def __init__(self, nom, capacite, img_recto):
        self.nom = nom
        self.img_recto = img_recto
        self.capa = capacite

class Carte(p.sprite.Sprite):
    def __init__(self, couleur, type):
        self.couleur = couleur
        self.type = type
        self.img = type