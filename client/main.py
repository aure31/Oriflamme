import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame as p
from server.game import Game

p.init()
p.mixer.init()  # Initialize the mixer
p.mixer.music.load("client/assets/fond_sonore.mp3")  # Load the music file
p.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
p.mixer.music.play(-1)  # Play the music in a loop

p.display.set_caption('Oriflamme')

window = p.display.set_mode((0,0), p.FULLSCREEN)
screen_width, screen_height = window.get_size()
background = p.image.load("client/assets/bg_lobby.png").convert()
background_image = p.transform.scale(background, (screen_width, screen_height))

def main():
    is_running = True
    game = Game()
    clock = p.time.Clock()
    while is_running:
            
        for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
            if event.type == p.KEYDOWN:
                event.key 

        window.blit(background_image, (0, 0))  # Use the scaled background image
        p.display.update()

if __name__ == "__main__":
    main()
