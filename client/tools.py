import pygame
import math
import os
WHITE = (255,255,255)
pygame.init()
pygame.mixer.init()
#all class for graphique elements
      
class TextInput:
    def __init__(self, x, y, screen):
        self.rect = pygame.Rect(x, y, 500, 40)  # Taille fixe de 500x40
        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
        self.border_color = (200, 200, 200)  # Couleur de bordure grise
        self.active_border_color = (0, 0, 0)  # Couleur de bordure noire quand active
        self.text = ''
        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
        self.font = pygame.font.Font(None, 32)
        self.screen = screen
        self.active = False

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
                else:
                    self.text += event.unicode

    def clear(self):
        self.text = ''

    def get_last_valid_text(self):
        return self.last_valid_text

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # Change la couleur de la bordure en fonction de l'état actif
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(self.screen, border_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class Bouton:
    def __init__(self, image1, image2):
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.rect = self.image1.get_rect()  # Initialiser le rectangle sans position

    def affiche(self, surface, x, y):
        self.rect.topleft = (x, y)  # Mettre à jour la position du bouton
        # Vérifie si le curseur est sur le bouton
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.image2, self.rect.topleft)
        else:
            surface.blit(self.image1, self.rect.topleft)

    def est_clique(self):
        # Vérifie si le bouton est cliqué
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
    
class Texte:
    def __init__(self, texte, couleur=(0, 0, 0), bg_color=None, police="Arial", taille=32):
        self.texte = texte
        self.couleur = couleur
        self.bg_color = bg_color  # Couleur de fond par défaut à None
        self.font = pygame.font.Font(pygame.font.match_font(police), taille)  # Utiliser Arial par défaut

    def affiche(self, surface, x, y):
        # Rendre le texte
        text_surface = self.font.render(self.texte, True, self.couleur, self.bg_color)
        # Afficher le texte à la position (x, y)
        surface.blit(text_surface, (x, y))

#class TextInput:
#    def __init__(self, screen):
#        self.bg_color = (255, 255, 255)  # Couleur de fond blanche
#        self.border_color = (200, 200, 200)  # Couleur de bordure grise
#        self.active_border_color = (0, 0, 0)  # Couleur de bordure noire quand active
#        self.text = ''
#        self.last_valid_text = ''  # Attribut pour stocker le dernier texte validé
#        self.font = pygame.font.Font(None, 32)
#        self.screen = screen
#        self.active = False
#        self.width = 500
#        self.height = 40

#    def handle_event(self, event):
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            if self.rect.collidepoint(event.pos):
#                self.active = True
#            else:
#                self.active = False

#        if event.type == pygame.KEYDOWN:
#            if self.active:
#                if event.key == pygame.K_RETURN:
#                    print(f'Texte validé : {self.text}')
#                    self.last_valid_text = self.text
#                    self.active = False  # Désactiver le champ de texte
#                elif event.key == pygame.K_BACKSPACE:
#                    self.text = self.text[:-1]
#                else:
#                    self.text += event.unicode

#    def clear(self):
#        self.text = ''

#    def get_last_valid_text(self):
#        return self.last_valid_text

#    def draw(self, x, y):
        # Met à jour la position du rectangle
#        self.rect = pygame.Rect(x, y, self.width, self.height)
        
#        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # Change la couleur de la bordure en fonction de l'état actif
#        border_color = self.active_border_color if self.active else self.border_color
#        pygame.draw.rect(self.screen, border_color, self.rect, 2)
#        text_surface = self.font.render(self.text, True, (0, 0, 0))
#        self.screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
