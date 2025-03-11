from classes import Chat
import pygame as p

p.init()
p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600
bg_menus = p.transform.scale(p.image.load("client/assets/background/new_bg_lobby.png").convert(), (screen_width, screen_height))
bg_game = p.transform.scale(p.image.load("client/assets/background/new_bg_game.png").convert(), (screen_width, screen_height))
chat = Chat()

#Global Variables
error = None
menu = None
reseau = None
server = None
joueur = None
is_running = True
game = None
background = bg_menus

gm = mots_bannis = [
    "con", "connard", "connasse", "enculé", "salope", "pute", "fdp", "ntm",
    "ta mère", "tg", "débile", "abruti", "crétin", "idiot", "imbécile",
    "merde", "bordel", "chiant", "casse-couilles", "pétasse", "gouine",
    "pd", "tapette", "enculer", "bâtard", "sous-merde", "raclure", "salaud",
    "ducon", "duconne", "mongol", "autiste", "schizo", "dégénéré", "gros",
    "moche", "nul", "suce", "branleur", "branleuse", "foutre", "nique", 
    "suicide", "meurs", "crève", "tuer", "viol", "pédophile", "harcèlement",
    "menace", "sale ", "clochard", "prostituée", " anus", "trouduc"
]
