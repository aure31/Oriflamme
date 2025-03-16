from classes import Chat
import pygame as p

p.init()
p.display.set_caption('Oriflamme')
window = p.display.set_mode((1600,900))
screen_width, screen_height = window.get_size()
r = screen_width//1600
bg_menus = p.transform.scale(p.image.load("client/assets/background/new_bg_lobby.png").convert(), (screen_width, screen_height))
bg_game = p.transform.scale(p.image.load("client/assets/background/new_bg_game.png").convert(), (screen_width, screen_height))
chat = Chat()

#Global Variables
error = None
menu = None
reseau = None
server = None
joueur = None
is_running = True
game = None
background = bg_menus

mots_bannis = [
    "con", "conne", "cons", "connes", "connard", "connarde", "connards", "connasses",
    "enculé", "enculée", "enculés", "enculées", "salope", "salopes", "pute", "putes",
    "fdp", "ntm", "nique", "niquer", "niqué", "niquée", "niqués", "niquées", 
    "ta mère", "tm", "tg", "ta gueule", "ferme ta gueule", "débile", "débiles",
    "abruti", "abrutie", "abrutis", "abruties", "crétin", "crétine", "crétins", "crétines",
    "idiot", "idiote", "idiots", "idiotes", "imbécile", "imbéciles", "merde", "merdes",
    "bordel", "bordels", "chiant", "chiante", "chiants", "chiantes", 
    "casse-couilles", "casse burnes", "pétasse", "pétasses",
    "gouine", "gouines", "pd", "tapette", "tapettes", "enculer", "enculés", "enculée",
    "bâtard", "bâtarde", "bâtards", "bâtardes", "sous-merde", "raclure", "raclures", "salaud", "salauds",
    "ducon", "duconne", "mongol", "mongole", "mongols", "mongoles",
    "autiste", "autistes", "schizo", "schizophrène", "schizophrènes", "dégénéré", "dégénérée", "dégénérés", "dégénérées",
    "gros", "grosse", "gros lard", "grosse vache", "gros tas", "moche", "moches",
    "nul", "nulle", "nuls", "nulles", "suce", "sucer", "suceur", "suceuse", "suceurs", "suceuses",
    "branleur", "branleuse", "branleurs", "branleuses", "branler", "branlé", "branlée", "branlés", "branlées",
    "foutre", "se foutre", "foutre la merde", "nique ta mère", "suicide", "suicider", "suicidé", "suicidée", "suicidés", "suicidées",
    "meurs", "mourir", "crève", "crèves", "crever", "tuer", "tue", "tué", "tuée", "tués", "tuées", "assassiner", "assassiné",
    "viol", "violer", "violé", "violée", "violés", "violées", "violeur", "violeuse", "violeurs", "violeuses",
    "pédophile", "pédophilie", "pédophiles", "harcèlement", "harceler", "harcelé", "harcelée", "harcelés", "harcelées",
    "menace", "menacer", "menacé", "menacée", "menacés", "menacées",
    "sale", "sales", "sale con", "sale connard", "sale connasse", "sale pute", "sale enculé",
    "clochard", "clocharde", "clochards", "clochardes", "prostituée", "prostituées",
    "anus", "trouduc", "trou du cul", "trous du cul"
]
