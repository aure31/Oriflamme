import enum
from classes import Texte

class Error:
    def __init__(self, code, message, x , y):
        self.code = code
        self.message = message
        self.x = x
        self.y = y
        self.text_display = Texte(message,x,y, (255,0,0), None, 30)
    
    def affiche(self,window):
        self.text_display.affiche(window)

class ErrorList(enum.Enum):
    VALUE = Error(0, "Les infos entrées ne sont pas valides", 900, 750)
    SERVER = Error(1, "Impossible de trouver ce serveur", 950, 750)
    PSEUDO = Error(2, "Entrez un pseudo", 170, 550)
    SPACE = Error(3, "Caractère invalide détecté", 170, 550) 
    

def errorHandler(error: ErrorList,window) -> int:
    error.value.affiche(window)
    return error.value.code