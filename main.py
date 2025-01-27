import pygame as p
from game import Game
import time

#p.init()


#p.display.set_caption('Oriflamme')

#window_surface = p.display.set_mode((800, 600))


background = p.Surface((0,0), p.FULLSCREEN)

background.fill(p.Color('#000000'))
 

def main():
    clock = p.time.Clock()
    is_running = True
    game_begin = True
    game_playing = False
    game_over = False
    game = Game()
    game.join_player("j1")
    game.join_player("j2")
    game.join_player("j3")
    while is_running:
        time.sleep(2)
        game.start_game()
                
        '''for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
            if event.type == p.KEYDOWN:
                event.key 
        '''
        if game_begin:
            pass

        if game_playing:
            pass

        if game_over:
            pass

        #window_surface.blit(background, (0, 0))
        #p.display.update()

if __name__ == "main":
    main()