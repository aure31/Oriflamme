import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
import Joueur as j
from menu import MenuList
from classes import EventHandler
import loader as l
from loader import window,background_image
from error import errorHandler
import server.server as s

    
def main():
    l.menu = MenuList.ACCUEIL.value
    clock = p.time.Clock()
    while l.is_running:
        clock.tick(60)
        window.blit(background_image, (0, 0))
        for event in p.event.get():
            if event.type == p.QUIT:
                stop_game()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    stop_game()
            TextInput.handle_event_all(event)

        l.menu.affiche()
        if l.error:
            errorHandler(l.error,l.window)
        p.display.update()
        
def stop_game():
    l.is_running = False
    l.reseau.disconect()
    l.reseau = None
    p.quit()
    sys.exit()

if __name__ == "__main__":
    # p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")
    # p.mixer.music.set_volume(0.3)
    # p.mixer.music.play(-1)
    main()
