import pygame as p

class Types:
    def __init__(self, nom, capacite, img_recto):
        self.nom = nom
        self.img_recto = img_recto
        self.capa = capacite

class Carte(p.sprite.Sprite):
    def __init__(self, type):
        self.couleur = None
        self.type = type
        self.img = type
        self.idPlayer = -1
    
    def set_player(self,joueur):
        self.idPlayer = joueur.id
        self.couleur = joueur.couleur
        return self
    