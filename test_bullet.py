import pygame
from pygame.sprite import Sprite

class T_Bullet(Sprite):
    ''' Una clase para gestionar las balas disparadas desde la nave '''

    def __init__(self, ai_game):
        ''' Crea un objeto para la bala en la posición actual de la nave '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Crea un rectangulo para la bala en (0, 0) y luego establece la posición corecta
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Guarda la posición de la nbala como valor decimal
        self.y = float(self.rect.y)


    def update(self):
        ''' Mueve la bala hacia arriba por la pantalla '''
        # Actualiza la posición decimal de la bala
        self.y -= self.settings.bullet_speed
        # Actualiza la posiciób del rectangulo
        self.rect.y = self.y
     
    def draw_bullet(self):
        ''' Dibuja la bala en la pantalla'''
        pygame.draw.rect(self.screen, self.color, self.rect)
