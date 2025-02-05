import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
import enum
import classes as t
import server.server as s



p.init()
p.mixer.init()
click = p.mixer.Sound("client/assets/musiques/click.mp3")

p.display.set_caption('Oriflamme')
window = p.display.set_mode((0,0), p.FULLSCREEN)
screen_width, screen_height = window.get_size()
r = screen_width//1600
background = p.image.load("client/assets/background/bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
join = t.Bouton("client/assets/boutons/join.png", "client/assets/boutons/join_touched.png")
new_game = t.Bouton("client/assets/boutons/new_game.png", "client/assets/boutons/new_game_touched.png")
settings = t.Bouton("client/assets/boutons/settings.png", "client/assets/boutons/settings_touched.png")
credits = t.Bouton("client/assets/boutons/credits.png", "client/assets/boutons/credits_touched.png")
quitter = t.Bouton("client/assets/boutons/quit.png", "client/assets/boutons/quit_touched.png")
back = t.Bouton("client/assets/boutons/back.png", "client/assets/boutons/back_touched.png")
launch = t.Bouton("client/assets/boutons/launch.png", "client/assets/boutons/launch_touched.png")
create = t.Bouton("client/assets/boutons/new.png", "client/assets/boutons/new_touched.png")
ask_ip_join = t.TextInput()
ask_port_join = t.TextInput()
demande_ip = t.Texte("Entrez l'adresse IP du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
demande_port = t.Texte("Entrez le port du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
nouv_port = t.Texte("Entrez le port du serveur", (255,0,0), None, 45, "client/assets/Algerian.ttf")
entry_error = t.Texte("Les infos entrées ne sont pas valides", (255,255,255), None, 30)
server_error = t.Texte("Impossible de trouver ce serveur", (255,255,255), None, 30)
fleche = p.image.load("client/assets/sens.png")
chat_ = t.Chat()
entree_chat = t.TextInput()

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
    error = None
    chat = False
    menu = Menu.ACUEIL
    playing = False
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
                if event.key == p.K_t:
                    if not entree_chat.active:
                        chat = not chat
                if (event.key == p.K_KP_ENTER or event.key == p.K_RETURN) and chat :
                    chat_.envoyer(entree_chat.get_text())
                    entree_chat.clear()
            ask_ip_join.handle_event(event)
            ask_port_join.handle_event(event)
            entree_chat.handle_event(event)
        
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
                if t.is_valid_ip(ask_ip_join.get_text()) and t.is_port(ask_port_join.get_text()):
                    error = "server"
                    #menu = Menu.ATTENTE
                else:
                    error = "values"
            if error == "values":
                entry_error.affiche(window, 900, 750)
            if error == "server":
                server_error.affiche(window, 950, 750)
        
        if menu == Menu.SERVER:
            chat_.envoyer("/Serveur ouvert")
            menu = Menu.ATTENTE
            #s.start_server()
        
        if menu == Menu.ATTENTE:
            if chat:
                chat_.affiche(window)
                entree_chat.draw(0, 860, window)
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
    p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")
    p.mixer.music.set_volume(0.3)
    p.mixer.music.play(-1)
    main()
