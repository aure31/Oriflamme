
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
from server.game import Game

p.init()

p.display.set_caption('Oriflamme')

window = p.display.set_mode((0,0), p.FULLSCREEN)
screen_width, screen_height = window.get_size()
background = p.image.load("../assets/bg_lobby.png").convert
background_image = p.transform.scale(background, (screen_width, screen_height))

def main():
    game = Game()
    clock = p.time.Clock()
    while is_running:
            
        for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
            if event.type == p.KEYDOWN:
                event.key 

        window.blit(background, (0, 0))
        p.display.update()

if __name__ == "__main__":
    main()
