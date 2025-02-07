from classes import Bouton, TextInput, Texte
import pygame as p


p.init()
p.mixer.init()
click = p.mixer.Sound("client/assets/musiques/click.mp3")

p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600

background = p.image.load("client/assets/background/new_bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
join =Bouton("client/assets/new_button/join.png", "client/assets/new_button/join_touched.png")
new_game =Bouton("client/assets/new_button/new_game.png", "client/assets/new_button/new_game_touched.png")
settings =Bouton("client/assets/new_button/settings.png", "client/assets/new_button/settings_touched.png")
credits =Bouton("client/assets/new_button/credits.png", "client/assets/new_button/credits_touched.png")
quitter =Bouton("client/assets/new_button/quit.png", "client/assets/new_button/quit_touched.png")
back =Bouton("client/assets/new_button/back.png", "client/assets/new_button/back_touched.png")
launch =Bouton("client/assets/new_button/launch.png", "client/assets/new_button/launch_touched.png")
create =Bouton("client/assets/new_button/new.png", "client/assets/new_button/new_touched.png")
ask_ip_join =TextInput()
ask_port_join =TextInput()
name = TextInput()
pseudo = Texte("Votre nom :", (254, 215, 32), None, 50, "client/assets/Algerian.ttf")
demande_ip =Texte("Entrez l'adresse IP du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
demande_port =Texte("Entrez le port du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
nouv_port =Texte("Entrez le port du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
entry_error =Texte("Les infos entrées ne sont pas valides", (255,255,255), None, 30)
server_error =Texte("Impossible de trouver ce serveur", (255,255,255), None, 30)
pseudo_error = Texte("Entrez un pseudo", (255,0,0), None, 30)
space_error = Texte("Caractère invalide détecté", (255, 0, 0), None, 30)
connexion = Texte("Connexion...", (255,255,255), None, 30, "client/assets/Algerian.ttf")
fleche = p.image.load("client/assets/sens.png")