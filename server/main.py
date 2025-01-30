
from server.game import Game
import time
 

def main():
    print("main")
    
    is_running = True
    game_begin = True
    game_playing = False
    game_over = False
    game = Game()
    game.join_player("j1")
    game.join_player("j2")
    game.join_player("j3")
    print("start")
    game.start_game()

if __name__ == "__main__":
    main()