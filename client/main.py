import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
from server.game import Game

p.init()
p.mixer.init()  # Initialize the mixer
p.mixer.music.load("client/assets/musiques/fond_sonore.mp3")  # Load the music file
p.mixer.music.set_volume(0.3)  # Set volume (0.0 to 1.0)
p.mixer.music.play(-1)  # Play the music in a loop

p.display.set_caption('Oriflamme')

window = p.display.set_mode((0,0), p.FULLSCREEN)
screen_width, screen_height = window.get_size()
background = p.image.load("client/assets/background/bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))
join = p.image.load("client/assets/boutons/join.png")#.convert_alpha()
join_touched = p.image.load("client/assets/boutons/join_touched.png")
new_game = p.image.load("client/assets/boutons/new_game.png")#.convert_alpha()
new_game_touched = p.image.load("client/assets/boutons/new_game_touched.png")
settings = p.image.load("client/assets/boutons/settings.png")
settings_touched = p.image.load("client/assets/boutons/settings_touched.png")
credits = p.image.load("client/assets/boutons/credits.png")
credits_touched = p.image.load("client/assets/boutons/credits_touched.png")
quitter = p.image.load("client/assets/boutons/quit.png")
quitter_touched = p.image.load("client/assets/boutons/quit_touched.png")

def main():
    is_running = True
    lobby_1 = True
    lobby_2 = False
    lobby_3 = False
    lobby_4 = False
    sett = False
    cred = False
    playing = False
    game = Game()
    clock = p.time.Clock()
    while is_running:
        mouse_pos = p.mouse.get_pos()
        for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    is_running = False
        
        if lobby_1:
            window.blit(background_image, (0, 0))
            window.blit(join, (1000, 100))
            window.blit(new_game, (1000, 250))
            window.blit(settings, (1000, 400))
            window.blit(credits, (1000, 550))
            window.blit(quitter, (1000, 700))
            if join.get_rect(topleft=(1000, 100)).collidepoint(mouse_pos):
                window.blit(join_touched, (1000, 100))
                if p.mouse.get_pressed()[0]:
                    lobby_1 = False
                    lobby_2 = True 
            if new_game.get_rect(topleft=(1000, 250)).collidepoint(mouse_pos):
                window.blit(new_game_touched, (1000, 250))
                if p.mouse.get_pressed()[0]:
                    lobby_1 = False
                    lobby_3 = True
            if settings.get_rect(topleft=(1000, 400)).collidepoint(mouse_pos):
                window.blit(settings_touched, (1000, 400))
                if p.mouse.get_pressed()[0]:
                    lobby_1 = False
                    sett = True
            if credits.get_rect(topleft=(1000, 550)).collidepoint(mouse_pos):
                window.blit(credits_touched, (1000, 550))
                if p.mouse.get_pressed()[0]:
                    lobby_1 = False
                    cred = True
            if quitter.get_rect(topleft=(1000, 700)).collidepoint(mouse_pos):
                window.blit(quitter_touched, (1000, 700))
                if p.mouse.get_pressed()[0]:
                    is_running = False
        
        if lobby_2:
            window.blit(background_image, (0, 0))
        
        if lobby_3:
            window.blit(background_image, (0, 0))
        
        if lobby_4:
            window.blit(background_image, (0, 0))

        if sett:
            window.blit(background_image, (0, 0))

        if playing:
            pass

        if cred:
            cred = False
            lobby_1 = True
            #background = p.image.load("client/assets/bg_credits.png").convert()
            #background_image = p.transform.scale(background, (screen_width, screen_height))
        p.display.update()

if __name__ == "__main__":
    main()
