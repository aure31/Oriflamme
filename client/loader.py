from classes import Bouton, TextInput, Texte
from network import Network
import pygame as p


p.init()
p.mixer.init()
click = p.mixer.Sound("client/assets/musiques/click.mp3")

p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600

#Images/Elements
background = p.image.load("client/assets/background/new_bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
connexion = Texte("Connexion...",950, 750, (255,255,255), None, 30, "client/assets/Algerian.ttf")
fleche = p.image.load("client/assets/sens.png")

caracteres = [" ", "/", "@", "~", "#"]

#Global Variables
error = None
menu = None
reseau : Network = None
server = None
joueur = None
is_running = True