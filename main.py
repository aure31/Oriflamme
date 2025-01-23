import pygame as p
import game

p.init()


p.display.set_caption('Oriflamme')

window_surface = p.display.set_mode((800, 600))


background = p.Surface((0,0), p.FULLSCREEN)

background.fill(p.Color('#000000'))
 

def main():
    clock = p.time.Clock()
    is_running = True
    while is_running:
        clock.tick()
        for event in p.event.get():
            if event.type == p.QUIT:
                is_running = False
        



        window_surface.blit(background, (0, 0))
        p.display.update()

if __name__ == "main":
    main()