import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
import enum
from classes import *
from network import Network, is_valid_ip, is_port
import server.server as s
import server.joueur as j
from _thread import *



p.init()
p.mixer.init()
click = p.mixer.Sound("client/assets/musiques/click.mp3")

p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600
background = p.image.load("client/assets/background/new_bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
join =Bouton("client/assets/new_button/join_button.png", "client/assets/new_button/hover_join_button.png")
new_game =Bouton("client/assets/boutons/new_game.png", "client/assets/boutons/new_game_touched.png")
settings =Bouton("client/assets/boutons/settings.png", "client/assets/boutons/settings_touched.png")
credits =Bouton("client/assets/boutons/credits.png", "client/assets/boutons/credits_touched.png")
quitter =Bouton("client/assets/boutons/quit.png", "client/assets/boutons/quit_touched.png")
back =Bouton("client/assets/boutons/back.png", "client/assets/boutons/back_touched.png")
launch =Bouton("client/assets/boutons/launch.png", "client/assets/boutons/launch_touched.png")
create =Bouton("client/assets/boutons/new.png", "client/assets/boutons/new_touched.png")
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
connexion = Texte("Connexion...", (255,255,255), None, 30, "client/assets/Algerian.ttf")
fleche = p.image.load("client/assets/sens.png")

class Menu(enum.Enum):
    ACCUEIL = 0
    REJOINDRE = 1
    JEU = 2
    ATTENTE = 3
    PARAMETRE = 4
    CREDIT = 5
    

def main():
    is_running = True
    error = None
    chat = False
    menu = Menu.ACCUEIL
    playing = False
    clock = p.time.Clock()
    network = None
    while is_running:
        window.blit(background_image, (0, 0))
        mouse_pos = p.mouse.get_pos()
        for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    is_running = False
            ask_ip_join.handle_event(event)
            ask_port_join.handle_event(event)
            name.handle_event(event)
        
        match menu:

            case Menu.ACCUEIL:
                name.draw(170, 500, window)
                pseudo.affiche(window, 170, 420)
                join.affiche(window, 1000, 100)
                new_game.affiche(window, 1000, 250)
                settings.affiche(window, 1000, 400)
                credits.affiche(window, 1000, 550)
                quitter.affiche(window, 1000, 700)
                if join.est_clique():
                    if name.get_text() == "":
                        error = 'pseudo'
                    else:
                        error = None
                        menu = Menu.REJOINDRE
                if new_game.est_clique():
                    if name.get_text() == "":
                        error = 'pseudo'
                    else:
                        error = None
                        start_new_thread(s.start_server,())
                        joueur = j.Joueur(name.get_text())
                        reseau = Network(s.get_ip_address(), 5555)
                        reseau.send(joueur.get_name())
                        menu = Menu.ATTENTE
                if settings.est_clique():
                    error = None
                    menu = Menu.PARAMETRE
                if credits.est_clique():
                    error = None
                    menu = Menu.CREDIT
                if quitter.est_clique():
                    is_running = False

            case Menu.REJOINDRE:
                join.affiche(window, 950, 600)
                back.affiche(window, 25, 25)
                demande_ip.affiche(window, 800, 240)
                demande_port.affiche(window, 800, 440)
                ask_ip_join.draw(900, 300, window)
                ask_port_join.draw(900, 500, window)
                window.blit(fleche, (790, 295))
                window.blit(fleche, (790, 495))
                if back.est_clique():
                    error = None
                    menu = Menu.ACCUEIL
                if join.est_clique():
                    if is_valid_ip(ask_ip_join.get_text()) and is_port(ask_port_join.get_text()):
                        error = None
                        connexion.affiche(window, 950, 750)
                        try:
                            reseau = Network(ask_ip_join.get_text(), int(ask_port_join.get_text()))
                            joueur = j.Joueur(name.get_text())
                            reseau.send(joueur.get_name())
                            menu = Menu.ATTENTE
                        except:
                            print("client : Connexion échouée")
                            error = "server"
                    else:
                        error = "values" 

            case Menu.ATTENTE:
                Texte("IP du serveur : "+str(reseau.server), (255, 255, 255), None, 32).affiche(window, 1150, 10)
                Texte("Port du serveur : "+str(reseau.port), (255, 255, 255), None, 32).affiche(window, 1150, 50)
                back.affiche(window, 25, 25)
                if back.est_clique():
                    reseau.send("quit")
                    menu = Menu.ACCUEIL
                #reseau.send("nothing")
                if joueur.id == 1:
                    launch.affiche(window, 950, 600)
                

            case Menu.PARAMETRE:
                back.affiche(window, 25, 25) 
                if back.est_clique():
                    menu = Menu.ACCUEIL

            case Menu.JEU:
                pass

            case Menu.CREDIT:
                menu = Menu.ACCUEIL

        if error == "values":
            entry_error.affiche(window, 900, 750)
        if error == "server":
            server_error.affiche(window, 950, 750)
        if error == 'pseudo':
            pseudo_error.affiche(window, 170, 550)

        p.display.update()
        

if __name__ == "__main__":
    p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")
    p.mixer.music.set_volume(0.3)
    p.mixer.music.play(-1)
    main()
