import enum
from client.network import Network, is_port
import loader as l
import error as e
import server.server as s
from classes import Element, Bouton, TextInput, Texte
import pygame
from groupelement import DynamicTextList, GroupElement
import packet.serverbound as sb


class Menu:

    def __init__(self, name):
        self.name = name
        self.elements = {}

    def addElement(self, name: str, element: Element | GroupElement):
        element.addMenu(self)
        self.elements[name] = element
        return self

    def affiche(self):
        for element in self.elements.values():
            element.affiche(l.window)

    def getElement(self, name: str) -> Element:
        return self.elements[name]
    
    def isAffiche(self):
        return l.menu == self


class AttenteMenu(Menu):

    def __init__(self):
        super().__init__("Attente")

    def init(self):
        self.getElement("ip").set_text("IP du serveur : " +
                                       str(l.reseau.server))
        self.getElement("port").set_text("Port du serveur : " +
                                         str(l.reseau.port))
    
    def addPlayer(self,player:str):
        self.getElement("playerList").addElement(Texte(player,1150, 100+len(self.getElement("playerList").elements)*30, (255, 255, 255)))

#------- Utilis Menu Elements -----------
class BackBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/back.png",
                         "client/assets/new_button/back_touched.png",
                         pygame.Vector2(10, 10))

    def onClique(self):
        l.menu = MenuList.ACCUEIL.value
        l.error = None


#------- Accueil Menu Elements -----------
class JoinBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/join.png",
                         "client/assets/new_button/join_touched.png",
                         pygame.Vector2(900, 100))

    def onClique(self):
        name = self.menus[0].getElement("name")
        erreur = e.pseudo_error(name.get_text())
        if erreur != None:
            l.error = erreur
        else:
            l.error = None
            l.menu = MenuList.REJOINDRE.value


class NewGameBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/new_game.png",
                         "client/assets/new_button/new_game_touched.png",
                         pygame.Vector2(900, 250))

    def onClique(self):
        name: TextInput = self.menus[0].getElement("name")
        error = None
        erreur = e.pseudo_error(name.get_text())
        if erreur != None:
            error = erreur
        else:
            l.error = None
            l.server = s.Server()
            # Add a small delay to ensure server is ready
            import time
            time.sleep(0.1)  # 100ms delay
            try:
                l.reseau = Network(l.server.ip, l.server.port, name.get_text())
                l.menu = MenuList.ATTENTE.value
                l.menu.init()
            except ConnectionRefusedError:
                error = e.ErrorList.SERVER
                if l.server:
                    l.server.stop()
                    l.server = None

        l.error = error


class SettingsBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/settings.png",
                         "client/assets/new_button/settings_touched.png",
                         pygame.Vector2(900, 400))

    def onClique(self):
        l.error = None
        l.menu = MenuList.PARAMETRE.value


class CreditsBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/credits.png",
                         "client/assets/new_button/credits_touched.png",
                         pygame.Vector2(900, 550))

    def onClique(self):
        l.error = None
        l.menu = MenuList.CREDIT.value


class QuitterBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/quit.png",
                         "client/assets/new_button/quit_touched.png",
                         pygame.Vector2(900, 700))

    def onClique(self):
        l.is_running = False

class MusicBoutton(Bouton):
    def __init__(self):
        super().__init__("client/assets/boutons/on.png","client/assets/on_touched.png", pygame.Vector2(900, 300))
        self.active = True

#------- Rejoindre Menu Elements -----------
class RejoindreJoinBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/join.png",
                         "client/assets/new_button/join_touched.png",
                         pygame.Vector2(875, 600))

    def onClique(self):
        ask_ip_join: TextInput = self.menus[0].getElement("ask_ip_join")
        ask_port_join: TextInput = self.menus[0].getElement("ask_port_join")
        if  is_port(ask_port_join.get_text()):
            l.error = None
            try:
                name: TextInput = MenuList.ACCUEIL.value.getElement("name")
                l.reseau = Network(ask_ip_join.get_text(),
                                   int(ask_port_join.get_text()),
                                   name.get_text())
                l.menu = MenuList.ATTENTE.value
                l.menu.init()
            except:
                print("client : Connexion échouée")
                l.error = e.ErrorList.SERVER
        else:
            l.error = e.ErrorList.VALUE


#------- Attente Menu Elements -----------


class AttenteLaunchBoutton(Bouton):

    def __init__(self):
        super().__init__("client/assets/new_button/launch.png",
                         "client/assets/new_button/launch_touched.png",
                         pygame.Vector2(950, 700),
                         condition=lambda: l.reseau and l.reseau.id == 0)

    def onClique(self):
        sb.ServerBoundGameStartPacket().send(l.reseau.conn)


class AttenteBackBoutton(BackBoutton):

    def __init__(self):
        super().__init__()

    def onClique(self):
        print("client : Retour")
        l.reseau.disconect()
        print("disconect")
        if l.server is not None:
            print("server : Fermeture du serveur")
            print("server : " + str(l.server.ip) + ":" + str(l.server.port))
            l.server.stop()
            l.server = None
        l.reseau = None
        l.menu = MenuList.ACCUEIL.value

#------- Jeu Menu Elements -----------

#------- MenuList ------------

class MenuList(enum.Enum):
    ACCUEIL = Menu("Accueil")\
            .addElement("name",TextInput(170, 500))\
            .addElement("pseudo",Texte("Votre nom :",170, 420, (254, 215, 32), None, 50, "client/assets/Algerian.ttf"))\
            .addElement("join",JoinBoutton())\
            .addElement("new_game",NewGameBoutton())\
            .addElement("settings",SettingsBoutton())\
            .addElement("credits",CreditsBoutton())\
            .addElement("quitter",QuitterBoutton())
    REJOINDRE = Menu("Rejoindre")\
            .addElement("demande_ip",Texte("Entrez l'adresse IP du serveur",800, 240, (255,0,0), None, 45, "client/assets/Algerian.ttf"))\
            .addElement("demande_port",Texte("Entrez le port du serveur",800, 440, (255,0,0), None, 45, "client/assets/Algerian.ttf"))\
            .addElement("ask_ip_join",TextInput(900, 300))\
            .addElement("ask_port_join",TextInput(900, 500))\
            .addElement("join",RejoindreJoinBoutton())\
            .addElement("back",BackBoutton())
    ATTENTE = AttenteMenu()\
            .addElement("back",AttenteBackBoutton())\
            .addElement("ip",Texte("IP du serveur : ",1150, 10, (255, 255, 255), None, 32))\
            .addElement("port",Texte("Port du serveur : ",1150, 50, (255, 255, 255), None, 32))\
            .addElement("launch",AttenteLaunchBoutton())\
            .addElement("player",Texte("Joueurs :",1150, 90, (255, 255, 255), None, 32))\
            .addElement("playerList", DynamicTextList((1150, 120), 30))\
            .addElement("chat", l.chat)
    JEU = Menu("Jeu")\
        .addElement("chat", l.chat)
    PARAMETRE = Menu("Parametre")\
        .addElement("back",BackBoutton())\
        .addElement("Musique",Texte("Musique : ", 850, 200, (0,0,0), None, 65, "client/assets/Algerian.ttf"))\
        .addElement("On", Bouton("client/assets/boutons/on.png", "client/assets/boutons/on_touched.png", pygame.Vector2(1175, 190)))
    CREDIT = Menu("Credit")\
        .addElement("back",BackBoutton())
