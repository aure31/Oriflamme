import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
import enum
#from server.game import Game
import client.classes as t

p.init()
p.mixer.init()
p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")
p.mixer.music.set_volume(0.3)
p.mixer.music.play(-1)

p.display.set_caption('Oriflamme')

window = p.display.set_mode((0,0), p.FULLSCREEN)
screen_width, screen_height = window.get_size()
background = p.image.load("client/assets/background/bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
join = t.Bouton("client/assets/boutons/join.png", "client/assets/boutons/join_touched.png")
new_game = t.Bouton("client/assets/boutons/new_game.png", "client/assets/boutons/new_game_touched.png")
settings = t.Bouton("client/assets/boutons/settings.png", "client/assets/boutons/settings_touched.png")
credits = t.Bouton("client/assets/boutons/credits.png", "client/assets/boutons/credits_touched.png")
quitter = t.Bouton("client/assets/boutons/quit.png", "client/assets/boutons/quit_touched.png")
back = t.Bouton("client/assets/boutons/back.png", "client/assets/boutons/back_touched.png")
ask_port_create = t.TextInput() # (900, 200)
ask_ip_join = t.TextInput() # (900, 300)
ask_port_join = t.TextInput() # (900, 500)
demande_ip = t.Texte("Entrez l'adresse IP du serveur", (255,0,0), None, "client/assets/Algerian.ttf", 45)
demande_port = t.Texte("Entrez le port du serveur", (255,0,0), None, "client/assets/Algerian.ttf", 45)
fleche = p.image.load("client/assets/sens.png")

class Menu(enum.Enum):
    ACUEIL = 0
    REJOINDRE = 1
    SERVER = 2
    ATTENTE = 3
    PARAMETRE = 4
    CREDIT = 5
    JEU = 6

def main():
    is_running = True
    menu = Menu.ACUEIL
    playing = False
    #game = Game()
    clock = p.time.Clock()
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
            ask_port_create.handle_event(event)
        
        if menu == Menu.ACUEIL:
            join.affiche(window, 1000, 100)
            new_game.affiche(window, 1000, 250)
            settings.affiche(window, 1000, 400)
            credits.affiche(window, 1000, 550)
            quitter.affiche(window, 1000, 700)
            if join.est_clique():
                menu = Menu.REJOINDRE
            if new_game.est_clique():
                menu = Menu.SERVER
            if settings.est_clique():
                menu = Menu.PARAMETRE
            if credits.est_clique():
                menu = Menu.CREDIT
            if quitter.est_clique():
                is_running = False
        
        if menu == Menu.REJOINDRE:
            join.affiche(window, 950, 600)
            back.affiche(window, 25, 25)
            demande_ip.affiche(window, 800, 240)
            demande_port.affiche(window, 800, 440)
            ask_ip_join.draw(900, 300, window)
            ask_port_join.draw(900, 500, window)
            window.blit(fleche, (790, 295))
            window.blit(fleche, (790, 495))
            if back.est_clique():
                menu = Menu.ACUEIL
            if join.est_clique():
                #serveur = t.Network(ask_ip_join.get_last_valid_text(), int(ask_port_join.get_last_valid_text()))
                menu = Menu.ATTENTE
        
        if menu == Menu.SERVER:
            back.affiche(window, 25, 25)
            if back.est_clique():
                menu = Menu.ACUEIL
        
        if menu == Menu.ATTENTE:
            back.affiche(window, 25, 25)
            if back.est_clique():
                menu = Menu.ACUEIL

        if menu == Menu.PARAMETRE:
            back.affiche(window, 25, 25) 
            if back.est_clique():
                menu = Menu.ACUEIL

        if menu == Menu.JEU:
            pass

        if menu == Menu.CREDIT:
            menu = Menu.ACUEIL

        p.display.update()
        

if __name__ == "__main__":
    main()
