from classes import Chat
import pygame as p

p.init()
p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600
bg_menus = p.image.load("client/assets/background/new_bg_lobby.png").convert()
bg_game = p.image.load("client/assets/background/new_bg_game.png").convert()
background = p.transform.scale(bg_menus, (screen_width, screen_height))
caracteres = [" ", "/", "@", "~", "#"]
chat = Chat()

#Global Variables
error = None
menu = None
reseau = None
server = None
joueur = None
is_running = True