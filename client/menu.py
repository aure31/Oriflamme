import enum
from loader import *

class Accueil:

    def __init__(self):
        self.name = "Accueil"

    def affiche():
        name.draw(170, 500, window)
        pseudo.affiche(window, 170, 420)
        join.affiche(window, 900, 100)
        new_game.affiche(window, 900, 250)
        settings.affiche(window, 900, 400)
        credits.affiche(window, 900, 550)
        quitter.affiche(window, 900, 700)
    
    def on_clique():
        if join.est_clique():
            if name.get_text() == "":
                error = 'pseudo'
            elif " " in name.get_text():
                error = "space"
            else:
                error = None
                menu = MenuList.REJOINDRE
        if new_game.est_clique():
            if name.get_text() == "":
                error = 'pseudo'
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


class MenuList(enum.Enum):
    ACCUEIL = Accueil()
    REJOINDRE = 1
    JEU = 2
    ATTENTE = 3
    PARAMETRE = 4
    CREDIT = 5