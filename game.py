from joueur import Joueur

states={}

class game:
    def __init__(self,players:list):
        self.file_influance = []
        self.players = players
        self.state = "start"

    def start_game(self):
        for e in self.players : 

    def add_end(self,card):
        self.file_influance.append(card)
    
    def add_start(self,card):
        self.file_influance.insert(0,card)

    def end_turn(self):
        self.state = "end"
