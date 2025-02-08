import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
from network import Network, is_valid_ip, is_port
import Joueur as j
from menu import *
from loader import *
from error import errorHandler,ErrorList
import server.server as s


caracteres = [" ", "/", "@", "~", "#"]
    
def main():
    is_running = True
    error = None
    chat = False
    menu = MenuList.ACCUEIL
    playing = False
    clock = p.time.Clock()
    network = None
    server = None
    while is_running:
        window.blit(background_image, (0, 0))
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
            case MenuList.ACCUEIL:
                name.draw(170, 500, window)
                pseudo.affiche(window, 170, 420)
                join.affiche(window, 900, 100)
                new_game.affiche(window, 900, 250)
                settings.affiche(window, 900, 400)
                credits.affiche(window, 900, 550)
                quitter.affiche(window, 900, 700)
                if join.est_clique():
                    if name.get_text() == "":
                        error = ErrorList.PSEUDO
                    elif " " in name.get_text():
                        error = ErrorList.SPACE
                    else:
                        error = None
                        menu = MenuList.REJOINDRE
                if new_game.est_clique():
                    if name.get_text() == "":
                        error = ErrorList.PSEUDO
                    else:
                        error = None
                        server = s.Server()
                        reseau = Network(server.ip, server.port)
                        reseau.send(name.get_text())
                        menu = MenuList.ATTENTE
                if settings.est_clique():
                    error = None
                    menu = MenuList.PARAMETRE
                if credits.est_clique():
                    error = None
                    menu = MenuList.CREDIT
                if quitter.est_clique():
                    is_running = False

            case MenuList.REJOINDRE:
                join.affiche(window, 875, 600)
                back.affiche(window, 10, 10)
                demande_ip.affiche(window, 800, 240)
                demande_port.affiche(window, 800, 440)
                ask_ip_join.draw(900, 300, window)
                ask_port_join.draw(900, 500, window)
                window.blit(fleche, (790, 295))
                window.blit(fleche, (790, 495))
                if back.est_clique():
                    error = None
                    menu = MenuList.ACCUEIL
                if join.est_clique():
                    if is_valid_ip(ask_ip_join.get_text()) and is_port(ask_port_join.get_text()):
                        error = None
                        connexion.affiche(window, 950, 750)
                        try:
                            reseau = Network(ask_ip_join.get_text(), int(ask_port_join.get_text()))
                            joueur = j.Joueur(name.get_text())
                            reseau.send(joueur.get_name())
                            menu = MenuList.ATTENTE
                        except:
                            print("client : Connexion échouée")
                            error = ErrorList.SERVER
                    else:
                        error = ErrorList.VALUE

            case MenuList.ATTENTE:
                Texte("IP du serveur : "+str(reseau.server), (255, 255, 255), None, 32).affiche(window, 1150, 10)
                Texte("Port du serveur : "+str(reseau.port), (255, 255, 255), None, 32).affiche(window, 1150, 50)
                back.affiche(window, 10, 10)
                if back.est_clique():
                    reseau.send("quit")
                    menu = MenuList.ACCUEIL
                #reseau.send("nothing")
                if joueur.id == 1:
                    launch.affiche(window, 950, 600)
                

            case MenuList.PARAMETRE:
                back.affiche(window, 10, 10) 
                if back.est_clique():
                    menu = MenuList.ACCUEIL

            case MenuList.JEU:
                pass

            case MenuList.CREDIT:
                menu = MenuList.ACCUEIL

        #errorHandler(error)
        p.display.update()
        

if __name__ == "__main__":
    p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")
    p.mixer.music.set_volume(0.3)
    p.mixer.music.play(-1)
    main()
