from .joueur import Joueur
from .cartes import Carte,full_deck,colors
import random
import packet.clientbound as cb
import threading as th

states={}


class Game:
    def __init__(self,server):
        self.server = server
        self.file_influence :list[list[Carte]] = []
        self.players:list[Joueur] = []
        self.state = "waiting"
        self.event = th.Event()
        self.first_player = -1
        self.colors = colors.copy()
        self.tour = 0

    def random_color(self):
        print(" ".join(self.color))
        return self.color.pop(random.randint(0,len(self.color)-1))

    def join_player(self,joueur:Joueur):
        if self.state == "waiting":
            self.players.append(joueur)
            self.server.broadcast(cb.ClientBoundPlayerListPacket(self.players))
            print(f"{joueur.nom} à rejoint la partie.")

    def start_game(self):
        for p in self.players :
            self.gen_deck(p)
        self.first_player = random.randint(0,len(self.players))
        self.state="start"
        print("Début de la partie")
        self.phase_un()        

    def add_card(self,idPlayer:int,card:Carte,slot:int):
        index = 0
        if slot == -1:
            self.file_influence.append([card])
            index = len(self.file_influence)-1
        elif slot == -2:
            self.file_influence.insert(0,[card])
            index = 0
        elif slot in range(len(self.file_influence)) and self.file_influence[slot][0].idPlayer == idPlayer:
            self.file_influence[slot].append(card)
            index = slot
        else:
            return False
        card.pos = index
        return True
        
    def get_top_cards(self):
        result = []
        for lst in self.file_influence:
            result.append(lst[-1])
        return result
    
    def get_card(self,index) -> Carte :
        return self.file_influence[index][-1]
    
    def phase_un(self):
        self.tour +=1
        for p in self.players:
            print("C'est au tour de "+p.nom+" de jouer !")
            p.client.send(cb.ClientBoundGameHandPacket(p.cartes))
            self.event.wait()
        self.phase_deux()
            
 
    #phase a la fin du tours
    def phase_deux(self):
        for lst in self.file_influence:
            card = lst[-1]
            if card.shown:
                card.capacite(self)
                continue
            #retourne ou non la carte
            player = self.get_player(card.idPlayer)
            act = player.action()
            if act:
                card.shown = True
                card.capacite(self)
                player.ptsinflu += card.ptsinflu
            else :
                card.ptsinflu+=1
        if self.tour == 6:
            self.end_partie()
        else:
            print("----- Fin du tour " +str(self.tour) + "-----")
            self.placement()

    def end_partie(self):
        print("end")
            
    def get_file_size(self):
        return len(self.file_influence)

    def end_turn(self):
        self.state = "end"

    def get_player(self,idPlayer) -> Joueur:
        return self.players[idPlayer]

    def discard(self, cardPos : int):
        #print(cardPos)
        sous_lst=len(self.file_influence[cardPos])
        card = None
        if sous_lst == 1:
            card = self.file_influence.pop(cardPos)[0]
        else :
            card = self.file_influence[cardPos].pop()
        player = self.get_player(card.idPlayer)
        player.defausse.append(card)
        if(card.type.id == 8): Carte.type.onDeath(Game.get_player(card.idPlayer), Game, Carte, card)

    def gen_deck(self,player:Joueur):
        out = full_deck(player)
        defausse = []
        for i in range(3):
            defausse.append(out.pop(random.randint(0,len(out)-1)))
        player.cartes = out
        player.defausse = defausse


