import pygame
import socket

class TextInput:
    def __init__(self):
        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
        self.border_color = (200, 200, 200)  # Couleur de bordure grise
        self.active_border_color = (0, 0, 0)  # Couleur de bordure noire quand active
        self.text = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.width = 500
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Initialiser self.rect

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(f'Texte validé : {self.text}')
                    self.last_valid_text = self.text
                    self.active = False  # Désactiver le champ de texte
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.last_valid_text = self.text  # Mettre à jour le dernier texte validé après suppression
                else:
                    self.text += event.unicode
                    self.last_valid_text = self.text  # Mettre à jour le dernier texte validé

    def clear(self):
        self.text = ''
        self.last_valid_text = ''  # Réinitialiser le dernier texte validé

    def get_text(self):
        return self.last_valid_text

    def draw(self, x, y, surface):
        self.rect.topleft = (x, y)  # Mettre à jour la position de self.rect
        pygame.draw.rect(surface, self.bg_color, self.rect)
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(surface, border_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))



class Bouton:
    pressed = False

    def __init__(self, image1, image2):
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.rect = self.image1.get_rect()  # Initialiser le rectangle sans position

    def affiche(self, surface, x, y):
        self.rect.topleft = (x, y)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.image2, self.rect.topleft)
        else:
            surface.blit(self.image1, self.rect.topleft)

    def est_clique(self):
        from main import click
        retour = pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and not Bouton.pressed 
        Bouton.presse(retour)
        if retour:
            click.play()
        return retour
    
    def presse(retour):
        if not pygame.mouse.get_pressed()[0]:
            Bouton.pressed = False
        elif retour : 
            Bouton.pressed = True 
    
class Texte:
    def __init__(self, texte, couleur=(0, 0, 0), bg_color=None, taille=32, police = "client/assets/arial.ttf"):
        self.texte = texte
        self.couleur = couleur
        self.bg_color = bg_color
        self.font = pygame.font.Font(police, taille)

    def affiche(self, surface, x, y):
        # Rendre le texte
        text_surface = self.font.render(self.texte, True, self.couleur, self.bg_color)
        # Afficher le texte à la position (x, y)
        surface.blit(text_surface, (x, y))

class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

def is_valid_ip(ip_str):
    parts = ip_str.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def is_port(num_str):
    return num_str.isdigit() and len(num_str) == 5